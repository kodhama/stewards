// Where skills go and how they get there. Each harness has a skills folder
// per scope; each installed skill folder carries a marker naming its tool;
// a skill is replaced by two renames through a stage folder beside the
// skills folder, so a reader of the skill path sees the old copy, nothing for
// one rename, or the new copy, never half of one. The copy it replaces moves
// to prev/, one generation per harness and skill.

import { randomBytes } from "node:crypto";
import {
  chmodSync,
  copyFileSync,
  lstatSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  readlinkSync,
  realpathSync,
  renameSync,
  rmSync,
  rmdirSync,
  statSync,
  symlinkSync,
  writeFileSync,
} from "node:fs";
import { dirname, join, sep } from "node:path";

import { claudeHome, heldRunLocks, homeOf, isRecord, jsonText, keepAlive, sha256, stateHome, writeAtomic } from "./lock.mjs";
import { MARKER, NAME } from "./manifest.mjs";

/** @typedef {"claude" | "codex"} Harness */

/**
 * The paths one scope works on: its lock, the run lock beside it, each
 * harness's skills folder, and the prev/ slot for each harness and skill.
 * @typedef {{
 *   readonly lock: string,
 *   readonly runLock: string,
 *   readonly skills: (harness: Harness) => string,
 *   readonly prev: (harness: Harness, skill: string) => string,
 * }} Places
 */

export const HARNESSES = /** @type {const} */ (["claude", "codex"]);

const STAGE = ".kodhama-stage";

/**
 * The paths for a scope. User scope uses the harness homes from the
 * environment; project scope uses the repo at `root`, with its prev/ slots
 * keyed by the repo's real path so two projects never share one.
 * @param {"user" | "project"} scope
 * @param {NodeJS.ProcessEnv} env
 * @param {string | undefined} root the project's git root, at project scope
 * @returns {Places}
 */
export const places = (scope, env, root) => {
  const home = homeOf(env);
  const state = stateHome(env);
  if (scope === "project") {
    if (root === undefined) throw new Error("project scope needs a repo root");
    const key = sha256(realpathSync(root)).slice(0, 12);
    return {
      lock: join(root, ".kodhama", "cli", "lock.json"),
      runLock: join(root, ".kodhama", "cli", "run.lock"),
      skills: (harness) => join(root, harness === "claude" ? ".claude" : ".agents", "skills"),
      prev: (harness, skill) => join(state, "prev", "projects", key, harness, skill),
    };
  }
  return {
    lock: join(state, "lock.json"),
    runLock: join(state, "run.lock"),
    skills: (harness) =>
      harness === "claude"
        ? join(claudeHome(env), "skills")
        : join(home, ".agents", "skills"),
    prev: (harness, skill) => join(state, "prev", harness, skill),
  };
};

/**
 * Effect: each folder kodhama writes into at project scope that resolves,
 * through a symlink, outside the repo, so a repo cannot steer a write
 * elsewhere. One that does not exist yet is made inside it.
 * @param {string} root the repo's real path
 * @returns {readonly string[]}
 */
export const outsideRoot = (root) =>
  [".claude", ".agents"]
    .flatMap((harness) => [harness, join(harness, "skills"), join(harness, STAGE)])
    .concat([".kodhama", join(".kodhama", "cli")])
    .map((rel) => join(root, rel))
    .filter((path) => {
      if (!present(path)) return false;
      try {
        const real = realpathSync(path);
        return real !== root && !real.startsWith(root + sep);
      } catch {
        return true;
      }
    });

/**
 * Effect: whether anything, even a broken symlink, is at a path.
 * @param {string} path
 */
export const present = (path) => {
  try {
    lstatSync(path);
    return true;
  } catch {
    return false;
  }
};

/**
 * Effect: the real path of a folder, through any symlink, or the path as
 * given when it does not resolve, so two harnesses whose skills folders are
 * one folder can be told apart from two that are not.
 * @param {string} path
 */
export const realOf = (path) => {
  try {
    return realpathSync(path);
  } catch {
    return path;
  }
};

/**
 * Effect: the marker in a skill folder, or `undefined` when there is none
 * or it is not a JSON object.
 * @param {string} dir
 * @returns {Record<string, unknown> | undefined}
 */
export const readMarker = (dir) => {
  try {
    const value = JSON.parse(readFileSync(join(dir, MARKER), "utf8"));
    return isRecord(value) ? value : undefined;
  } catch {
    return undefined;
  }
};

/**
 * Effect: who a target path belongs to, as far as `tool` is concerned:
 * nothing is there, a folder marked as the tool's, or something it must not
 * touch, with why.
 * @param {string} path
 * @param {string} tool
 * @returns {{ readonly state: "absent" | "ours" } | { readonly state: "theirs", readonly why: string }}
 */
export const ownerOf = (path, tool) => {
  if (!present(path)) return { state: "absent" };
  if (!lstatSync(path).isDirectory()) return { state: "theirs", why: "is not a folder" };
  const marker = readMarker(path);
  if (marker === undefined) return { state: "theirs", why: "has no kodhama marker" };
  if (marker.tool !== tool) return { state: "theirs", why: `is marked as ${String(marker.tool)}'s` };
  return { state: "ours" };
};

/**
 * Effect: writes a skill folder's marker.
 * @param {string} dir
 * @param {{ readonly tool: string, readonly skill: string, readonly tag: string, readonly commit: string }} marker
 */
export const writeMarker = (dir, marker) => writeAtomic(join(dir, MARKER), jsonText(marker));

/**
 * Effect: copies a tree as it is, folders, files and symlinks, for a move
 * between filesystems.
 * @param {string} from
 * @param {string} to
 */
const copyTree = (from, to) => {
  const stat = lstatSync(from);
  if (stat.isSymbolicLink()) symlinkSync(readlinkSync(from), to);
  else if (stat.isDirectory()) {
    mkdirSync(to);
    for (const name of readdirSync(from)) copyTree(join(from, name), join(to, name));
    chmodSync(to, stat.mode & 0o7777);
  } else {
    copyFileSync(from, to);
    chmodSync(to, stat.mode & 0o777);
  }
};

/**
 * Effect: moves a folder to `to`, replacing what is there, by rename, or by
 * copy and delete when the two sit on different filesystems.
 * @param {string} from
 * @param {string} to
 */
export const moveTo = (from, to) => {
  rmSync(to, { recursive: true, force: true });
  mkdirSync(dirname(to), { recursive: true });
  try {
    renameSync(from, to);
  } catch (error) {
    if (/** @type {NodeJS.ErrnoException} */ (error).code !== "EXDEV") throw error;
    copyTree(from, to);
    // Renamed aside before it is deleted, so a crash mid-delete leaves a
    // `.moved` leftover that recovery deletes, never a half copy it would
    // move over the full one.
    renameSync(from, `${from}.moved`);
    rmSync(`${from}.moved`, { recursive: true, force: true });
  }
};

/**
 * Effect: a harness's stage folder for a skills folder: beside the folder it
 * really is, through any symlink, so its renames never cross filesystems,
 * and its own, so two harnesses' skills folders in one parent never share
 * one. A stage that is a symlink or a file is refused before anything is
 * written through it.
 * @param {string} skills
 * @param {Harness} harness
 */
const stageOf = (skills, harness) => {
  let parent;
  try {
    parent = dirname(realpathSync(skills));
  } catch {
    parent = dirname(skills);
  }
  const stage = join(parent, STAGE, harness);
  for (const dir of [dirname(stage), stage]) {
    if (present(dir) && !lstatSync(dir).isDirectory()) {
      throw new Error(`${dir} is not a real folder, so kodhama will not write through it. Move it aside, then run kodhama again.`);
    }
  }
  return stage;
};

/**
 * Effect: deletes a folder if it is empty.
 * @param {string} dir
 */
const pruneEmpty = (dir) => {
  if (present(dir) && readdirSync(dir).length === 0) rmdirSync(dir);
};

/**
 * Effect: finishes what a crashed run left in a skills folder's stage. A
 * `<skill>.old` goes back into place when the live path is empty, or to
 * prev/ when it is not; only then are half-built new copies deleted.
 * @param {string} skills the skills folder
 * @param {Harness} harness
 * @param {(skill: string) => string} prev the prev/ slot for a skill
 * @returns {readonly string[]} a line per folder put back or moved
 */
export const recover = (skills, harness, prev) => {
  keepAlive();
  const stage = stageOf(skills, harness);
  if (!present(stage)) return [];
  const lines = [];
  for (const name of readdirSync(stage).sort()) {
    const skill = name.slice(0, -".old".length);
    if (!name.endsWith(".old") || !NAME.test(skill)) continue;
    const live = join(skills, skill);
    if (present(live)) {
      moveTo(join(stage, name), prev(skill));
      lines.push(`Moved ${join(stage, name)}, left by an interrupted run, to ${prev(skill)}.`);
    } else {
      mkdirSync(skills, { recursive: true });
      renameSync(join(stage, name), live);
      lines.push(`Put ${live} back from ${join(stage, name)}, left by an interrupted run.`);
    }
  }
  for (const name of readdirSync(stage)) rmSync(join(stage, name), { recursive: true, force: true });
  pruneEmpty(stage);
  pruneEmpty(dirname(stage));
  return lines;
};

/**
 * Effect: builds a skill's new copy in the stage and swaps it in: the live
 * folder, if any, is renamed aside, the new copy renamed into place, and the
 * old copy moved to prev/.
 * @param {string} skills the skills folder
 * @param {Harness} harness
 * @param {string} skill
 * @param {(dir: string) => void} build writes the new copy into `dir`
 * @param {string} prev the skill's prev/ slot
 * @returns {boolean} whether an old copy went to prev/
 */
export const swapIn = (skills, harness, skill, build, prev) => {
  keepAlive();
  const stage = stageOf(skills, harness);
  const fresh = join(stage, skill);
  const old = join(stage, `${skill}.old`);
  const live = join(skills, skill);
  mkdirSync(stage, { recursive: true });
  rmSync(fresh, { recursive: true, force: true });
  build(fresh);
  mkdirSync(skills, { recursive: true });
  const replaced = present(live);
  if (replaced) renameSync(live, old);
  renameSync(fresh, live);
  if (replaced) moveTo(old, prev);
  pruneEmpty(stage);
  pruneEmpty(dirname(stage));
  return replaced;
};

// A run lock older than this is taken to be left by a run that died.
const STALE_MS = 10 * 60 * 1000;

// The file in a run lock naming the run that holds it.
const OWNER = "owner";

/**
 * Effect: the token of the run holding a run lock, if it can be read.
 * @param {string} path
 */
const tokenOf = (path) => {
  try {
    return readFileSync(join(path, OWNER), "utf8");
  } catch {
    return undefined;
  }
};

/**
 * Effect: makes the run lock with exclusive create and writes our token
 * into it, or reports that it exists.
 * @param {string} path
 * @param {string} token
 */
const claim = (path, token) => {
  try {
    mkdirSync(path);
  } catch (error) {
    if (/** @type {NodeJS.ErrnoException} */ (error).code === "EEXIST") return false;
    throw error;
  }
  writeFileSync(join(path, OWNER), token);
  return true;
};

/**
 * Effect: takes the run lock, or reports it held. A stale one is taken over
 * by renaming it aside, which only one claimant can win; a claimant that
 * finds it renamed a fresh lock instead puts it back and backs off.
 * @param {string} path
 * @param {string} token
 */
const takeRunLock = (path, token) => {
  if (claim(path, token)) return true;
  let stat;
  try {
    stat = statSync(path);
  } catch {
    return claim(path, token);
  }
  if (Date.now() - stat.mtimeMs <= STALE_MS) return false;
  const seen = tokenOf(path);
  const aside = `${path}.stale-${randomBytes(6).toString("hex")}`;
  try {
    renameSync(path, aside);
  } catch {
    return false;
  }
  if (tokenOf(aside) !== seen) {
    try {
      renameSync(aside, path);
    } catch {
      // Whoever holds it now made a fresh one; theirs stands.
    }
    return false;
  }
  rmSync(aside, { recursive: true, force: true });
  return claim(path, token);
};

/** @type {Set<() => void>} */
const releases = new Set();
let trapped = false;

/**
 * Effect: on SIGINT or SIGTERM, releases every run lock still held, once,
 * and exits 130 or 143. Recovery finishes any swap the signal cut short.
 */
const trapSignals = () => {
  if (trapped) return;
  trapped = true;
  for (const [signal, code] of /** @type {const} */ ([["SIGINT", 130], ["SIGTERM", 143]])) {
    process.once(signal, () => {
      for (const release of releases) release();
      process.exit(code);
    });
  }
};

/**
 * Effect: runs `run` while holding the scope's run lock, so two runs never
 * recover the same stage or rewrite the same lock at once. The run lock is
 * released however `run` ends, but only while it still holds our token, and
 * folders made only to hold it are deleted again when they are left empty.
 * @template T
 * @param {string} path
 * @param {() => T} run
 * @returns {T | { readonly code: 1, readonly lines: readonly string[] }}
 */
export const withRunLock = (path, run) => {
  const made = mkdirSync(dirname(path), { recursive: true });
  const token = `${process.pid} ${randomBytes(8).toString("hex")}\n`;
  const release = () => {
    if (tokenOf(path) === token) rmSync(path, { recursive: true, force: true });
  };
  try {
    if (!takeRunLock(path, token)) {
      return {
        code: 1,
        lines: [`another kodhama run holds ${path}. If none is running, delete it; it also goes stale after 10 minutes.`],
      };
    }
    trapSignals();
    releases.add(release);
    heldRunLocks.add(path);
    try {
      return run();
    } finally {
      heldRunLocks.delete(path);
      releases.delete(release);
      release();
    }
  } finally {
    for (let dir = dirname(path); made !== undefined && dir.startsWith(made); dir = dirname(dir)) {
      if (readdirSync(dir).length > 0) break;
      rmdirSync(dir);
    }
  }
};
