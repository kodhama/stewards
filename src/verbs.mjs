// The four verbs. Each reads the lock first and writes it last; install and
// update fetch and validate before touching any skills folder; check never
// fetches or writes; remove never deletes a skill folder, only moves it to
// prev/. Every writing verb first finishes what a crashed run left staged.

import { basename, join } from "node:path";

import { copyFiles, isNewer, toolSource, versionOf, withTool } from "./fetch.mjs";
import { diffTree, hashTree, readLock, writeLock } from "./lock.mjs";
import { applyMigration, findEnables, guardRefusal, planMigration } from "./migrate.mjs";
import { HARNESSES, moveToPrev, ownerOf, places, present, readMarker, realOf, recover, swapIn, withRunLock, writeMarker } from "./targets.mjs";

/** @typedef {import("./cli.mjs").Outcome} Outcome */
/** @typedef {import("./lock.mjs").Entry} Entry */
/** @typedef {import("./lock.mjs").Lock} Lock */
/** @typedef {import("./targets.mjs").Harness} Harness */
/** @typedef {import("./targets.mjs").Places} Places */
/** @typedef {import("./fetch.mjs").Fetched} Fetched */

/**
 * What a verb runs with: the environment, the scope and, at project scope,
 * the repo's root, and the paths of the scope.
 * @typedef {{
 *   readonly env: NodeJS.ProcessEnv,
 *   readonly scope: "user" | "project",
 *   readonly root: string | undefined,
 *   readonly where: Places,
 * }} Context
 */

/**
 * @param {readonly string[]} lines
 * @returns {Outcome}
 */
const refuse = (lines) => ({ code: 1, lines });

/**
 * What a printed command adds so it runs at the scope it was printed at.
 * @param {Context["scope"]} scope
 */
const scoped = (scope) => (scope === "project" ? " --scope project" : "");

/**
 * Effect: recovers the stage of each harness the run works on. Should one
 * step throw, the error carries the lines of the steps before it as
 * `lines`, which the program prints ahead of it.
 * @param {Places} where
 * @param {readonly Harness[]} harnesses
 */
const recoverAll = (where, harnesses) => {
  /** @type {string[]} */
  const lines = [];
  try {
    for (const harness of harnesses) recover(where.skills(harness), harness, (skill) => where.prev(harness, skill), lines);
  } catch (error) {
    throw Object.assign(error instanceof Error ? error : new Error(String(error)), { lines });
  }
  return lines;
};

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
const handEdits = (live, locked, prev) => editLines(live, diffTree(locked, hashTree(live)), prev);

/**
 * Lines naming each file of a skill folder that differs, and where the copy
 * holding the difference now is.
 * @param {string} live the folder as it was
 * @param {ReturnType<typeof diffTree>} diff
 * @param {string} where
 */
const editLines = (live, diff, where) =>
  diff.map(({ kind, file }) => `${kind} ${join(live, file)}; the copy with it is in ${where}.`);

/**
 * Effect: whether a skill folder already holds the fetched copy, marked at
 * its tag and commit, as an interrupted run leaves the folders it swapped.
 * @param {string} live
 * @param {Fetched} fetched
 * @param {string} skill
 */
const isPlaced = (live, fetched, skill) => {
  const marker = readMarker(live);
  return (
    marker?.tool === fetched.tool && marker.skill === skill && marker.tag === fetched.tag && marker.commit === fetched.commit
  );
};

/**
 * How far a run that places skills got, filled in as it goes, so a caller
 * can say so even when it fails: each `<harness>/<skill>` swapped, each
 * whose live folder was renamed into the stage, with where, and a line per
 * prev/ slot whose copy it replaced. A key in `aside` but not `swapped` is
 * a swap that stopped with its old copy still in the stage.
 * @typedef {{ readonly swapped: Set<string>, readonly aside: Map<string, string>, readonly notes: string[] }} Progress
 */

/** @returns {Progress} */
const progress = () => ({ swapped: new Set(), aside: new Map(), notes: [] });

/**
 * Effect: copies every fetched skill into each harness, marked, through the
 * stage; old copies go to prev/. A folder an interrupted run already swapped
 * is left as it is, so the prev/ copy it made, hand edits and all, is not
 * replaced by the new copy. Returns the lock's record of the skills.
 * @param {Places} where
 * @param {Fetched} fetched
 * @param {readonly Harness[]} harnesses
 * @param {Progress} [placed]
 */
const placeSkills = (where, fetched, harnesses, placed = progress()) => {
  for (const harness of harnesses) {
    for (const skill of fetched.skills) {
      if (isPlaced(join(where.skills(harness), skill.name), fetched, skill.name)) continue;
      swapIn(
        where.skills(harness),
        harness,
        skill.name,
        (dir) => {
          copyFiles(skill.dir, dir, skill.files);
          writeMarker(dir, { tool: fetched.tool, skill: skill.name, tag: fetched.tag, commit: fetched.commit });
        },
        where.prev(harness, skill.name),
        { report: (line) => placed.notes.push(line), aside: (old) => placed.aside.set(`${harness}/${skill.name}`, old) },
      );
      placed.swapped.add(`${harness}/${skill.name}`);
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
      if (!present(path)) return [`missing ${path}`];
      const marker = readMarker(path);
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
 * Effect: each skill folder of the tool, in the harnesses given, whose
 * marker names another tag or commit than the lock: what an update that
 * failed partway leaves. The copy it replaced, hand edits and all, is then
 * only in prev/, so moving anything else into that slot would lose it.
 * @param {Places} where
 * @param {string} tool
 * @param {Entry} entry
 * @param {readonly Harness[]} harnesses
 * @returns {readonly { readonly live: string, readonly prev: string, readonly tag: string, readonly commit: string }[]}
 */
const interrupted = (where, tool, entry, harnesses) => {
  // A folder two harnesses share was swapped once, by the first in lock
  // order, so only that harness's prev/ slot holds its old copy.
  /** @type {Map<string, Harness>} */
  const swapper = new Map();
  for (const harness of entry.harnesses) {
    for (const skill of Object.keys(entry.skills)) {
      const real = realOf(join(where.skills(harness), skill));
      if (!swapper.has(real)) swapper.set(real, harness);
    }
  }
  const seen = new Set();
  return harnesses.flatMap((harness) =>
    Object.keys(entry.skills).flatMap((skill) => {
      const live = join(where.skills(harness), skill);
      const real = realOf(live);
      if (seen.has(real)) return [];
      seen.add(real);
      if (ownerOf(live, tool).state !== "ours") return [];
      const marker = readMarker(live);
      return marker?.tag === entry.tag && marker.commit === entry.commit
        ? []
        : [{ live, prev: where.prev(swapper.get(real) ?? harness, skill), tag: String(marker?.tag), commit: String(marker?.commit) }];
    }),
  );
};

/**
 * Lines naming each folder an interrupted update left, where the copy it
 * replaced is, and the update that finishes it. When the tag that update
 * was moving to now names another commit, that update can no longer be
 * finished, so the way out by hand is printed in its place.
 * @param {string} tool
 * @param {string} at what `scoped` gives for the run's scope
 * @param {ReturnType<typeof interrupted>} found
 * @param {{ readonly tag: string, readonly commit: string }} [moved] the
 *   moved tag and the commit it names now
 */
const finishFirst = (tool, at, found, moved) => {
  const finishable = [...new Set(found.filter(({ tag }) => tag !== moved?.tag).map(({ tag }) => `kodhama update ${tool}#${tag}${at}`))];
  const stranded = found.filter(({ tag }) => tag === moved?.tag);
  return [
    ...found.map(
      ({ live, prev, tag }) =>
        `${live} is at ${tag}, left by an update that stopped partway; the copy it replaced, with any hand edits, is in ${prev}.`,
    ),
    ...(finishable.length > 0 ? [`Finish that update first: ${finishable.join(", or ")}.`] : []),
    ...(moved === undefined || stranded.length === 0
      ? []
      : [
          `${moved.tag} now points at ${moved.commit}, not ${stranded[0].commit}, so that update cannot be finished. The way out, by hand:`,
          "1. Copy each prev/ folder named above somewhere safe.",
          "2. Move each live folder named above out of its skills folder.",
          `3. Run kodhama remove ${tool}${at}, then kodhama install ${tool}${at}, then re-apply your edits from the copies.`,
          "A command that discards an interrupted update is tracked as KOD-25.",
        ]),
  ];
};

/**
 * Effect: takes the tool's enables and marketplace out of the user-level
 * files, after writing the receipt, and says what it did.
 * @param {string} tool
 * @param {NodeJS.ProcessEnv} env
 * @returns {{ readonly lines: readonly string[] } | { readonly error: string }}
 */
const migrateOut = (tool, env) => {
  const plan = planMigration(tool, env);
  if ("error" in plan) return { error: `${plan.error} --migrate changed nothing.` };
  if (plan.edits.length === 0) return { lines: [] };
  const receipt = applyMigration(tool, plan.edits, env);
  return {
    lines: [
      ...plan.edits.flatMap(({ path, removed }) => removed.map(({ key }) => `Took ${key} out of ${path}.`)),
      `The receipt, with each file as it was, is ${receipt}.`,
      // Claude's own plugin registry is not a documented file, so kodhama
      // leaves it to Claude's command.
      ...(plan.touchedClaude ? [`Next, run: claude plugin marketplace remove ${tool}`] : []),
    ],
  };
};

/**
 * Effect: `install <tool>[#<tag>]`, taking the tool's plugin enables out of
 * the user files first when `--migrate` asks.
 * @param {{ readonly tool: string, readonly tag: string | undefined, readonly harnesses: readonly Harness[], readonly migrate: boolean }} asked
 * @param {Context} context
 * @returns {Outcome}
 */
export const install = ({ tool, tag, harnesses, migrate }, { env, scope, root, where }) => {
  const at = scoped(scope);
  const blocked = guardRefusal(
    tool,
    findEnables(tool, scope, env, root),
    migrate,
    `Run kodhama install ${tool} --migrate${at} to take the user-level ones out, keeping a receipt, or turn them off by hand.`,
  );
  if (blocked !== undefined) return refuse(blocked);
  // --migrate edits user files, so at project scope it holds the user-scope
  // run lock too, user first.
  const runLocks = migrate && scope === "project" ? [places("user", env, undefined).runLock, where.runLock] : [where.runLock];
  return runLocks.reduceRight((inner, path) => () => withRunLock(path, inner), () => {
    const read = readLock(where.lock);
    if ("error" in read) return refuse([read.error]);
    const entry = read.lock.tools[tool];

    // With no tag named, an installed tool stays at its tag: install adds
    // harnesses, and moving to another tag is update's.
    const done = withTool(tool, tag ?? entry?.tag, { env }, (fetched) => {
      const recovered = recoverAll(where, harnesses);
      // An update that stopped partway is checked first, whatever install
      // was asked to do: adding a harness whose skills folder is one the
      // lock's harnesses already use would swap that update's copies back
      // and leave the prev/ copies it made open to the next update.
      const stuck = entry === undefined ? [] : interrupted(where, tool, entry, entry.harnesses);
      if (stuck.length > 0) return refuse([...recovered, ...finishFirst(tool, at, stuck)]);
      if (entry !== undefined && entry.tag !== fetched.tag) {
        return refuse([
          ...recovered,
          `${tool} is installed at ${entry.tag}. To move it to ${fetched.tag}, run kodhama update ${tool}#${fetched.tag}${at}.`,
        ]);
      }
      const adding = harnesses.filter((harness) => !entry?.harnesses.includes(harness));
      if (entry !== undefined && adding.length > 0 && entry.commit !== fetched.commit) {
        return refuse([
          ...recovered,
          `${tool} ${entry.tag} now points at ${fetched.commit}, not the ${entry.commit} installed. Run kodhama update ${tool}#${entry.tag}${at} first, so every harness gets the same copy.`,
        ]);
      }
      const occupied = preflight(where, tool, adding, fetched.skills.map((skill) => skill.name));
      if (occupied.length > 0) {
        return refuse([...recovered, ...occupied, `kodhama installs only into empty paths or folders marked as ${tool}'s, so it wrote nothing.`]);
      }
      const found = entry === undefined || adding.length > 0 ? [] : problems(where, tool, entry);
      if (entry !== undefined && found.length > 0) {
        return refuse([
          ...recovered,
          ...found,
          `${tool} ${entry.tag} is installed but differs from its lock. kodhama remove ${tool}${at} moves it to prev/, and install puts it back fresh.`,
        ]);
      }
      // What --migrate removes is every entry for the tool, enabled or not,
      // and its marketplace, not only the enables the guard stops on.
      const migrated = migrate ? migrateOut(tool, env) : { lines: [] };
      if ("error" in migrated) return refuse([...recovered, migrated.error]);
      if (entry !== undefined && adding.length === 0) {
        return {
          code: 0,
          lines: [...recovered, ...migrated.lines, `${tool} ${entry.tag} is already installed for ${entry.harnesses.join(", ")}.`],
        };
      }

      // A folder marked as the tool's at another tag, such as one a lost
      // lock no longer names, is replaced, and its copy goes to prev/. Its
      // tag is read now, before the swap. The lock's hashes are for the
      // lock's tag, never that one, so they cannot tell its hand edits.
      const olds = new Map(
        adding.flatMap((harness) =>
          fetched.skills.flatMap(({ name }) => {
            const live = join(where.skills(harness), name);
            const marker = ownerOf(live, tool).state === "ours" ? readMarker(live) : undefined;
            return marker === undefined || isPlaced(live, fetched, name)
              ? []
              : [[`${harness}/${name}`, `Moved ${live}, which was at ${String(marker.tag)} (${String(marker.commit)}), to ${where.prev(harness, name)}.`]];
          }),
        ),
      );
      const placed = progress();
      /** Lines for each old copy the swaps so far moved to prev/. */
      const movedOut = () => [...olds].filter(([key]) => placed.swapped.has(key) && placed.aside.has(key)).map(([, line]) => line);
      try {
        const skills = placeSkills(where, fetched, adding, placed);
        const all = HARNESSES.filter((harness) => adding.includes(harness) || entry?.harnesses.includes(harness));
        writeLock(where.lock, {
          lock: 1,
          tools: {
            ...read.lock.tools,
            [tool]: { tag: fetched.tag, commit: fetched.commit, source: fetched.source, harnesses: all, skills },
          },
        });
      } catch (error) {
        // What recovery moved, and the receipt when the configs are already
        // edited, must not be lost with the error.
        const why = error instanceof Error ? error.message : String(error);
        return refuse([
          ...recovered,
          ...migrated.lines,
          migrated.lines.length > 0 ? `kodhama stopped after --migrate: ${why}` : `kodhama stopped: ${why}`,
          ...movedOut(),
          // A swap that stopped after renaming the live folder aside.
          ...[...placed.aside].filter(([key]) => !placed.swapped.has(key)).map(([key, old]) => {
            const [harness, name] = /** @type {[Harness, string]} */ (key.split("/"));
            return `${join(where.skills(harness), name)}'s old copy is in ${old}; the next kodhama run moves it to ${where.prev(harness, name)}.`;
          }),
          ...placed.notes,
        ]);
      }
      return {
        code: 0,
        lines: [
          ...recovered,
          ...migrated.lines,
          `Installed ${tool} ${fetched.tag} (${fetched.commit}) for ${adding.join(", ")}: ${fetched.skills.map((skill) => skill.name).join(", ")}.`,
          ...movedOut(),
          ...placed.notes,
        ],
      };
    });
    return "error" in done ? refuse([done.error]) : done.value;
  })();
};

/**
 * Effect: `update <tool>[#<tag>]`, on the harnesses in the lock, from the
 * source install would use.
 * @param {{ readonly tool: string, readonly tag: string | undefined }} asked
 * @param {Context} context
 * @returns {Outcome}
 */
export const update = ({ tool, tag }, { env, scope, root, where }) => {
  const at = scoped(scope);
  const blocked = guardRefusal(
    tool,
    findEnables(tool, scope, env, root),
    false,
    `Turn them off, or take the user-level ones out with kodhama install ${tool} --migrate${at} at the installed tag, then update again.`,
  );
  if (blocked !== undefined) return refuse(blocked);
  return withRunLock(where.runLock, () => {
    const read = readLock(where.lock);
    if ("error" in read) return refuse([read.error]);
    const entry = read.lock.tools[tool];
    if (entry === undefined) return refuse([`${tool} is not installed here; kodhama install ${tool}${at} installs it.`]);
    // The lock's source is a record, not an instruction: a lock a repo
    // commits must not choose where the code comes from.
    const source = toolSource(tool, env);
    if (entry.source !== source) {
      return refuse([
        `The lock says ${tool} came from ${entry.source}, but kodhama fetches it from ${source}.`,
        `To move ${tool} to ${source}, run kodhama remove ${tool}${at}, then install it again.`,
      ]);
    }

    const done = withTool(tool, tag, { env }, (fetched) => {
      const installed = versionOf(entry.tag);
      const newest = versionOf(fetched.tag);
      if (tag === undefined && installed !== undefined && newest !== undefined && isNewer(installed, newest)) {
        return {
          code: 0,
          lines: [`${tool} stays at ${entry.tag}, which is newer than ${fetched.tag}, the newest stable tag. Name a tag to move to it.`],
        };
      }
      const recovered = recoverAll(where, entry.harnesses);
      // Only the update that stopped partway may go on: any other would
      // move a fresh copy over the prev/ copy holding the hand edits.
      const stuck = interrupted(where, tool, entry, entry.harnesses);
      const elsewhere = stuck.filter(({ tag, commit }) => tag !== fetched.tag || commit !== fetched.commit);
      if (elsewhere.length > 0) {
        return refuse([...recovered, ...finishFirst(tool, at, elsewhere, { tag: fetched.tag, commit: fetched.commit })]);
      }
      // A folder the interrupted update already swapped is skipped below, so
      // its prev/ copy is named now; a killed run never printed it. The
      // lock's hashes tell its hand edits only while its marker is the lock's.
      const finishing = stuck.flatMap(({ live, prev }) => {
        if (!present(prev)) return [];
        const skill = basename(live);
        const marker = readMarker(prev);
        const locked = marker?.tool === tool && marker.skill === skill && marker.tag === entry.tag && marker.commit === entry.commit;
        return [
          `${prev} holds the copy this update replaced${locked ? ` (${tool} ${entry.tag} per its marker)` : ""}; hand edits, if any, are there.`,
          ...(locked ? editLines(live, diffTree(entry.skills[skill], hashTree(prev)), prev) : []),
        ];
      });
      if (fetched.tag === entry.tag && fetched.commit === entry.commit) {
        return { code: 0, lines: [...recovered, `${tool} is already at ${entry.tag}.`] };
      }
      const names = fetched.skills.map((skill) => skill.name);
      const occupied = preflight(where, tool, entry.harnesses, names);
      if (occupied.length > 0) {
        return refuse([...recovered, ...occupied, `kodhama replaces only folders marked as ${tool}'s, so it wrote nothing.`]);
      }

      // Hand edits are read before the swap moves each old copy to prev/.
      // A folder two harnesses share is swapped once, by the first, so only
      // its prev/ slot is named.
      const seen = new Set();
      const edits = entry.harnesses.flatMap((harness) =>
        names.flatMap((skill) => {
          const live = join(where.skills(harness), skill);
          const locked = entry.skills[skill];
          const real = realOf(live);
          if (seen.has(real)) return [];
          seen.add(real);
          return locked !== undefined && ownerOf(live, tool).state === "ours" && !isPlaced(live, fetched, skill)
            ? [{ key: `${harness}/${skill}`, live, prev: where.prev(harness, skill), diff: diffTree(locked, hashTree(live)) }]
            : [];
        }),
      );
      const placed = progress();
      /** @type {string[]} */
      const dropped = [];
      try {
        const skills = placeSkills(where, fetched, entry.harnesses, placed);
        for (const skill of Object.keys(entry.skills).filter((skill) => !names.includes(skill))) {
          for (const harness of entry.harnesses) moveOut(where, tool, entry, harness, skill, dropped);
        }
        writeLock(where.lock, {
          lock: 1,
          tools: { ...read.lock.tools, [tool]: { ...entry, tag: fetched.tag, commit: fetched.commit, skills } },
        });
      } catch (error) {
        // The copies already swapped are in prev/, and the user must learn
        // where before anything else runs.
        return refuse([
          ...recovered,
          ...finishing,
          `kodhama stopped partway through updating ${tool} to ${fetched.tag}: ${error instanceof Error ? error.message : String(error)}`,
          ...edits.filter(({ key }) => placed.swapped.has(key)).flatMap(({ live, diff, prev }) => editLines(live, diff, prev)),
          // A swap that stopped after renaming the live folder aside left
          // the old copy in the stage, where the next run's recovery moves
          // it to prev/.
          ...edits
            .filter(({ key }) => placed.aside.has(key) && !placed.swapped.has(key))
            .flatMap(({ key, live, diff, prev }) => {
              const old = /** @type {string} */ (placed.aside.get(key));
              return [`${live}'s old copy is in ${old}; the next kodhama run moves it to ${prev}.`, ...editLines(live, diff, old)];
            }),
          ...placed.notes,
          ...dropped,
          `To finish, run kodhama update ${tool}#${fetched.tag}${at}.`,
        ]);
      }
      return {
        code: 0,
        lines: [
          ...recovered,
          `Updated ${tool} from ${entry.tag} to ${fetched.tag} (${fetched.commit}).`,
          ...finishing,
          ...edits.flatMap(({ live, diff, prev }) => editLines(live, diff, prev)),
          ...placed.notes,
          ...dropped,
        ],
      };
    });
    return "error" in done ? refuse([done.error]) : done.value;
  });
};

/**
 * Effect: moves one skill's folder out to prev/ in a harness, where the
 * folder is marked as the tool's, adding to `lines` as it goes: the prev/
 * copy it replaced, the move, and hand edits, or why it left the folder
 * alone.
 * @param {Places} where
 * @param {string} tool
 * @param {Entry} entry
 * @param {Harness} harness
 * @param {string} skill
 * @param {string[]} lines
 */
const moveOut = (where, tool, entry, harness, skill, lines) => {
  const live = join(where.skills(harness), skill);
  const prev = where.prev(harness, skill);
  const owner = ownerOf(live, tool);
  if (owner.state === "absent") return;
  if (owner.state === "theirs") {
    lines.push(`Left ${live} alone: it ${owner.why}.`);
    return;
  }
  const edits = handEdits(live, entry.skills[skill] ?? {}, prev);
  moveToPrev(where.skills(harness), harness, skill, prev, { report: (line) => lines.push(line) });
  lines.push(`Moved ${live} to ${prev}.`, ...edits);
};

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
export const remove = ({ tool, harnesses }, { scope, where }) =>
  withRunLock(where.runLock, () => {
    const at = scoped(scope);
    const read = readLock(where.lock);
    if ("error" in read) return refuse([read.error]);
    const entry = read.lock.tools[tool];
    if (entry === undefined) return refuse([`${tool} is not installed here.`]);
    const leaving = entry.harnesses.filter((harness) => harnesses.includes(harness));
    if (leaving.length === 0) return refuse([`${tool} is not installed for ${harnesses.join(", ")} here.`]);

    const recovered = recoverAll(where, leaving);
    const stuck = interrupted(where, tool, entry, leaving);
    if (stuck.length > 0) return refuse([...recovered, ...finishFirst(tool, at, stuck)]);
    const staying = entry.harnesses.filter((harness) => !leaving.includes(harness));
    // A skills folder a staying harness also resolves to is still in use:
    // the leaving harness only leaves the lock.
    const sharer = (/** @type {Harness} */ harness) =>
      staying.find((other) => realOf(where.skills(other)) === realOf(where.skills(harness)));
    // Each folder's lines are kept as it moves, so a failure on a later one
    // still names where the earlier ones, hand edits and all, went.
    /** @type {string[]} */
    const lines = [];
    try {
      for (const harness of leaving) {
        const other = sharer(harness);
        if (other !== undefined) {
          lines.push(`Left ${where.skills(harness)} as it is: it is the same folder as ${where.skills(other)}, which ${other} still uses.`);
          continue;
        }
        for (const skill of Object.keys(entry.skills)) moveOut(where, tool, entry, harness, skill, lines);
      }
      const { [tool]: _gone, ...others } = read.lock.tools;
      writeLock(where.lock, {
        lock: 1,
        tools: staying.length === 0 ? others : { ...others, [tool]: { ...entry, harnesses: staying } },
      });
    } catch (error) {
      return refuse([
        ...recovered,
        `kodhama stopped partway through removing ${tool}: ${error instanceof Error ? error.message : String(error)}`,
        ...lines,
        `To finish, run kodhama remove ${tool}${staying.length > 0 ? leaving.map((harness) => ` --harness ${harness}`).join("") : ""}${at} again.`,
      ]);
    }
    return { code: 0, lines: [...recovered, ...lines, `Removed ${tool} for ${leaving.join(", ")}.`] };
  });
