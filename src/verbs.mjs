// The four verbs. Each reads the lock first and writes it last; install and
// update fetch and validate before touching any skills folder; check never
// fetches or writes; remove never deletes a skill folder, only moves it to
// prev/. Every writing verb first finishes what a crashed run left staged.

import { join } from "node:path";

import { copyFiles, withTool } from "./fetch.mjs";
import { diffTree, hashTree, readLock, writeLock } from "./lock.mjs";
import { HARNESSES, moveTo, ownerOf, readMarker, recover, swapIn, writeMarker } from "./targets.mjs";

/** @typedef {import("./cli.mjs").Outcome} Outcome */
/** @typedef {import("./lock.mjs").Entry} Entry */
/** @typedef {import("./lock.mjs").Lock} Lock */
/** @typedef {import("./targets.mjs").Harness} Harness */
/** @typedef {import("./targets.mjs").Places} Places */
/** @typedef {import("./fetch.mjs").Fetched} Fetched */

/**
 * What a verb runs with: the environment, and the paths of its scope.
 * @typedef {{ readonly env: NodeJS.ProcessEnv, readonly where: Places }} Context
 */

/**
 * @param {readonly string[]} lines
 * @returns {Outcome}
 */
const refuse = (lines) => ({ code: 1, lines });

/**
 * Effect: recovers every harness's stage in the scope.
 * @param {Places} where
 */
const recoverAll = (where) =>
  HARNESSES.flatMap((harness) => recover(where.skills(harness), (skill) => where.prev(harness, skill)));

/**
 * Effect: a line per target folder that would be written and is not the
 * tool's to replace.
 * @param {Places} where
 * @param {string} tool
 * @param {readonly Harness[]} harnesses
 * @param {readonly string[]} skills
 */
const preflight = (where, tool, harnesses, skills) =>
  harnesses.flatMap((harness) =>
    skills.flatMap((skill) => {
      const path = join(where.skills(harness), skill);
      const owner = ownerOf(path, tool);
      return owner.state === "theirs" ? [`${path} ${owner.why}.`] : [];
    }),
  );

/**
 * Lines naming each file of a skill folder that differs from the lock, and
 * where the copy holding the difference now is.
 * @param {string} live the folder as it was
 * @param {import("./lock.mjs").SkillHashes} locked
 * @param {string} prev where it went
 */
const handEdits = (live, locked, prev) =>
  diffTree(locked, hashTree(live)).map(
    ({ kind, file }) => `${kind} ${join(live, file)}; the copy with it is in ${prev}.`,
  );

/**
 * Effect: copies every fetched skill into each harness, marked, through the
 * stage; old copies go to prev/. Returns the lock's record of the skills.
 * @param {Places} where
 * @param {Fetched} fetched
 * @param {readonly Harness[]} harnesses
 */
const placeSkills = (where, fetched, harnesses) => {
  for (const harness of harnesses) {
    for (const skill of fetched.skills) {
      swapIn(
        where.skills(harness),
        skill.name,
        (dir) => {
          copyFiles(skill.dir, dir, skill.files);
          writeMarker(dir, { tool: fetched.tool, skill: skill.name, tag: fetched.tag, commit: fetched.commit });
        },
        where.prev(harness, skill.name),
      );
    }
  }
  return Object.fromEntries(fetched.skills.map((skill) => [skill.name, hashTree(skill.dir)]));
};

/**
 * Effect: a line per way an installed tool differs from its lock entry.
 * @param {Places} where
 * @param {string} tool
 * @param {Entry} entry
 */
const problems = (where, tool, entry) =>
  entry.harnesses.flatMap((harness) =>
    Object.entries(entry.skills).flatMap(([skill, locked]) => {
      const path = join(where.skills(harness), skill);
      const marker = readMarker(path);
      const owner = ownerOf(path, tool);
      if (owner.state === "absent") return [`missing ${path}`];
      if (marker === undefined) return [`unmarked ${path}`];
      const differs =
        marker.tool !== tool || marker.skill !== skill || marker.tag !== entry.tag || marker.commit !== entry.commit;
      return [
        ...(differs ? [`marker differs ${path}`] : []),
        ...diffTree(locked, hashTree(path)).map(({ kind, file }) => `${kind} ${join(path, file)}`),
      ];
    }),
  );

/**
 * Effect: `install <tool>[#<tag>]`.
 * @param {{ readonly tool: string, readonly tag: string | undefined, readonly harnesses: readonly Harness[] }} asked
 * @param {Context} context
 * @returns {Outcome}
 */
export const install = ({ tool, tag, harnesses }, { env, where }) => {
  const read = readLock(where.lock);
  if ("error" in read) return refuse([read.error]);
  const entry = read.lock.tools[tool];

  const done = withTool(tool, tag, { env }, (fetched) => {
    const recovered = recoverAll(where);
    if (entry !== undefined && entry.tag !== fetched.tag) {
      return refuse([
        ...recovered,
        `${tool} is installed at ${entry.tag}. To move it to ${fetched.tag}, run kodhama update ${tool}#${fetched.tag}.`,
      ]);
    }
    const adding = harnesses.filter((harness) => !entry?.harnesses.includes(harness));
    if (entry !== undefined && adding.length === 0) {
      const found = problems(where, tool, entry);
      return found.length === 0
        ? { code: 0, lines: [...recovered, `${tool} ${entry.tag} is already installed for ${entry.harnesses.join(", ")}.`] }
        : refuse([
            ...recovered,
            ...found,
            `${tool} ${entry.tag} is installed but differs from its lock. kodhama remove ${tool} moves it to prev/, and install puts it back fresh.`,
          ]);
    }
    const blocked = preflight(where, tool, adding, fetched.skills.map((skill) => skill.name));
    if (blocked.length > 0) {
      return refuse([...recovered, ...blocked, `kodhama installs only into empty paths or folders marked as ${tool}'s, so it wrote nothing.`]);
    }

    const skills = placeSkills(where, fetched, adding);
    const all = HARNESSES.filter((harness) => adding.includes(harness) || entry?.harnesses.includes(harness));
    writeLock(where.lock, {
      lock: 1,
      tools: {
        ...read.lock.tools,
        [tool]: { tag: fetched.tag, commit: fetched.commit, source: fetched.source, harnesses: all, skills },
      },
    });
    return {
      code: 0,
      lines: [
        ...recovered,
        `Installed ${tool} ${fetched.tag} (${fetched.commit}) for ${adding.join(", ")}: ${fetched.skills.map((skill) => skill.name).join(", ")}.`,
      ],
    };
  });
  return "error" in done ? refuse([done.error]) : done.value;
};

/**
 * Effect: `update <tool>[#<tag>]`, on the harnesses in the lock and from the
 * lock's source.
 * @param {{ readonly tool: string, readonly tag: string | undefined }} asked
 * @param {Context} context
 * @returns {Outcome}
 */
export const update = ({ tool, tag }, { env, where }) => {
  const read = readLock(where.lock);
  if ("error" in read) return refuse([read.error]);
  const entry = read.lock.tools[tool];
  if (entry === undefined) return refuse([`${tool} is not installed here; kodhama install ${tool} installs it.`]);

  const done = withTool(tool, tag, { env, source: entry.source }, (fetched) => {
    const recovered = recoverAll(where);
    if (fetched.tag === entry.tag && fetched.commit === entry.commit) {
      return { code: 0, lines: [...recovered, `${tool} is already at ${entry.tag}.`] };
    }
    const names = fetched.skills.map((skill) => skill.name);
    const blocked = preflight(where, tool, entry.harnesses, names);
    if (blocked.length > 0) {
      return refuse([...recovered, ...blocked, `kodhama replaces only folders marked as ${tool}'s, so it wrote nothing.`]);
    }

    // Hand edits are read before the swap moves each old copy to prev/.
    const edits = entry.harnesses.flatMap((harness) =>
      names.flatMap((skill) => {
        const live = join(where.skills(harness), skill);
        const locked = entry.skills[skill];
        return locked !== undefined && ownerOf(live, tool).state === "ours"
          ? handEdits(live, locked, where.prev(harness, skill))
          : [];
      }),
    );
    const skills = placeSkills(where, fetched, entry.harnesses);
    const dropped = Object.keys(entry.skills)
      .filter((skill) => !names.includes(skill))
      .flatMap((skill) => moveOut(where, tool, entry, entry.harnesses, skill));
    writeLock(where.lock, {
      lock: 1,
      tools: { ...read.lock.tools, [tool]: { ...entry, tag: fetched.tag, commit: fetched.commit, skills } },
    });
    return {
      code: 0,
      lines: [...recovered, `Updated ${tool} from ${entry.tag} to ${fetched.tag} (${fetched.commit}).`, ...edits, ...dropped],
    };
  });
  return "error" in done ? refuse([done.error]) : done.value;
};

/**
 * Effect: moves one skill's folders out to prev/ in each harness, where the
 * folder is marked as the tool's, naming hand edits and each folder left
 * alone.
 * @param {Places} where
 * @param {string} tool
 * @param {Entry} entry
 * @param {readonly Harness[]} harnesses
 * @param {string} skill
 */
const moveOut = (where, tool, entry, harnesses, skill) =>
  harnesses.flatMap((harness) => {
    const live = join(where.skills(harness), skill);
    const prev = where.prev(harness, skill);
    const owner = ownerOf(live, tool);
    if (owner.state === "absent") return [];
    if (owner.state === "theirs") return [`Left ${live} alone: it ${owner.why}.`];
    const edits = handEdits(live, entry.skills[skill] ?? {}, prev);
    moveTo(live, prev);
    return [`Moved ${live} to ${prev}.`, ...edits];
  });

/**
 * Effect: `check [<tool>]`. Reads only the lock and the skills folders.
 * @param {{ readonly tool: string | undefined }} asked
 * @param {Context} context
 * @returns {Outcome}
 */
export const check = ({ tool }, { where }) => {
  const read = readLock(where.lock);
  if ("error" in read) return refuse([read.error]);
  const { tools } = read.lock;
  if (tool !== undefined && tools[tool] === undefined) return refuse([`${tool} is not installed here.`]);
  const names = tool === undefined ? Object.keys(tools).sort() : [tool];
  if (names.length === 0) return { code: 0, lines: ["kodhama has nothing installed here."] };
  const found = names.flatMap((name) => problems(where, name, tools[name]));
  return found.length > 0
    ? refuse(found)
    : {
        code: 0,
        lines: names.map((name) => `${name} ${tools[name].tag} is intact for ${tools[name].harnesses.join(", ")}.`),
      };
};

/**
 * Effect: `remove <tool>`, for the harnesses asked that the lock has.
 * @param {{ readonly tool: string, readonly harnesses: readonly Harness[] }} asked
 * @param {Context} context
 * @returns {Outcome}
 */
export const remove = ({ tool, harnesses }, { where }) => {
  const read = readLock(where.lock);
  if ("error" in read) return refuse([read.error]);
  const entry = read.lock.tools[tool];
  if (entry === undefined) return refuse([`${tool} is not installed here.`]);
  const leaving = entry.harnesses.filter((harness) => harnesses.includes(harness));
  if (leaving.length === 0) return refuse([`${tool} is not installed for ${harnesses.join(", ")} here.`]);

  const recovered = recoverAll(where);
  const lines = Object.keys(entry.skills).flatMap((skill) => moveOut(where, tool, entry, leaving, skill));
  const staying = entry.harnesses.filter((harness) => !leaving.includes(harness));
  const { [tool]: _gone, ...others } = read.lock.tools;
  writeLock(where.lock, {
    lock: 1,
    tools: staying.length === 0 ? others : { ...others, [tool]: { ...entry, harnesses: staying } },
  });
  return { code: 0, lines: [...recovered, ...lines, `Removed ${tool} for ${leaving.join(", ")}.`] };
};
