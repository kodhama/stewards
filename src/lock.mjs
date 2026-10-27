// The lock: one JSON file per scope recording, for each installed tool, its
// tag, commit and source, the harnesses it is installed for, and a sha256
// and exec bit for every file of every skill. It is written keys sorted,
// 2-space indented, through a temp file and a rename, and deleted once its
// last tool goes.

import { createHash } from "node:crypto";
import {
  chmodSync,
  existsSync,
  lstatSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  renameSync,
  rmSync,
  utimesSync,
  writeFileSync,
} from "node:fs";
import { homedir } from "node:os";
import { dirname, join } from "node:path";

import { MARKER, NAME } from "./manifest.mjs";

/**
 * One file as the lock records it.
 * @typedef {{ readonly sha256: string, readonly exec: boolean }} FileHash
 */

/**
 * A skill's files, by path relative to its folder, `/`-separated.
 * @typedef {Readonly<Record<string, FileHash>>} SkillHashes
 */

/**
 * @typedef {{
 *   readonly tag: string,
 *   readonly commit: string,
 *   readonly source: string,
 *   readonly harnesses: readonly ("claude" | "codex")[],
 *   readonly skills: Readonly<Record<string, SkillHashes>>,
 * }} Entry
 */

/** @typedef {{ readonly lock: 1, readonly tools: Readonly<Record<string, Entry>> }} Lock */

/**
 * The home folder as the environment gives it.
 * @param {NodeJS.ProcessEnv} env
 */
export const homeOf = (env) => env.HOME || homedir();

/**
 * Claude's config folder: `$CLAUDE_CONFIG_DIR`, or `~/.claude`.
 * @param {NodeJS.ProcessEnv} env
 */
export const claudeHome = (env) => env.CLAUDE_CONFIG_DIR || join(homeOf(env), ".claude");

/**
 * Where kodhama keeps its user-level state: `$XDG_DATA_HOME/kodhama`.
 * @param {NodeJS.ProcessEnv} env
 */
export const stateHome = (env) =>
  join(env.XDG_DATA_HOME || join(homeOf(env), ".local", "share"), "kodhama");

/** @param {string | Buffer} bytes */
export const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");

/**
 * @param {unknown} value
 * @returns {unknown}
 */
const sortKeys = (value) => {
  if (Array.isArray(value)) return value.map(sortKeys);
  if (typeof value !== "object" || value === null) return value;
  const record = /** @type {Record<string, unknown>} */ (value);
  return Object.fromEntries(
    Object.keys(record)
      .sort()
      .map((key) => [key, sortKeys(record[key])]),
  );
};

/**
 * JSON as kodhama writes it: keys sorted, 2-space indent, trailing newline.
 * @param {unknown} value
 */
export const jsonText = (value) => `${JSON.stringify(sortKeys(value), null, 2)}\n`;

/**
 * Effect: writes a file through a temp file beside it and a rename, so a
 * reader sees the old text or the new, never half of one. `mode`, when
 * given, is the new file's permission bits.
 * @param {string} path
 * @param {string} text
 * @param {number} [mode]
 */
export const writeAtomic = (path, text, mode) => {
  mkdirSync(dirname(path), { recursive: true });
  const temp = `${path}.kodhama-${process.pid}-${Date.now()}.tmp`;
  // Created with the target's mode, so a private file is never readable by
  // others, even for a moment; the chmod then undoes any umask narrowing.
  writeFileSync(temp, text, { flag: "wx", mode: mode ?? 0o666 });
  if (mode !== undefined) chmodSync(temp, mode);
  renameSync(temp, path);
};

/**
 * @param {unknown} value
 * @returns {value is Record<string, unknown>}
 */
export const isRecord = (value) =>
  typeof value === "object" && value !== null && !Array.isArray(value);

/**
 * A source git can only read as a repo, never as an option.
 * @param {string} source
 */
export const isSource = (source) => /^(https|file):\/\//.test(source);

/**
 * A file's path in a skill folder as kodhama records it: relative,
 * `/`-separated, and never stepping out of the folder.
 * @param {string} rel
 */
const isInside = (rel) =>
  rel !== "" && !rel.startsWith("/") && !rel.includes("\\") && !rel.split("/").includes("..");

/**
 * @param {unknown} value
 * @returns {value is Entry}
 */
const isEntry = (value) =>
  isRecord(value) &&
  typeof value.tag === "string" &&
  typeof value.commit === "string" &&
  typeof value.source === "string" &&
  isSource(value.source) &&
  Array.isArray(value.harnesses) &&
  value.harnesses.every((harness) => harness === "claude" || harness === "codex") &&
  isRecord(value.skills) &&
  Object.entries(value.skills).every(
    ([skill, files]) =>
      NAME.test(skill) &&
      isRecord(files) &&
      Object.entries(files).every(
        ([rel, file]) =>
          isInside(rel) && isRecord(file) && typeof file.sha256 === "string" && typeof file.exec === "boolean",
      ),
  );

/**
 * Effect: the lock at `path`, empty when there is none, or why it cannot be
 * trusted. A lock kodhama did not write is refused, never guessed at.
 * @param {string} path
 * @returns {{ readonly lock: Lock } | { readonly error: string }}
 */
export const readLock = (path) => {
  if (!existsSync(path)) return { lock: { lock: 1, tools: {} } };
  /** @type {unknown} */
  let value;
  try {
    value = JSON.parse(readFileSync(path, "utf8"));
  } catch {
    value = undefined;
  }
  return isRecord(value) && value.lock === 1 && isRecord(value.tools) &&
    Object.entries(value.tools).every(([tool, entry]) => NAME.test(tool) && isEntry(entry))
    ? { lock: /** @type {Lock} */ (value) }
    : { error: `${path} is not a lock this kodhama can read. Move it aside to start over.` };
};

/** The file in a run lock naming the run that holds it. */
export const RUN_LOCK_OWNER = "owner";

/**
 * The run locks this process holds, each with the token it wrote. Each is
 * checked and touched before every phase of a run (each git call of the
 * fetch, recovery, each swap, the lock write), so a long run never looks
 * stale to another, and a run that lost its lock stops before it writes.
 * @type {Map<string, string>}
 */
export const heldRunLocks = new Map();

/**
 * Effect: checks that every run lock this process holds still names it,
 * and marks each, and its owner file, as alive now. A lock another run took
 * over stops this one.
 */
export const keepAlive = () => {
  const now = new Date();
  for (const [path, token] of heldRunLocks) {
    let owner;
    try {
      owner = readFileSync(join(path, RUN_LOCK_OWNER), "utf8");
    } catch {
      owner = undefined;
    }
    if (owner !== token) {
      throw new Error(`another kodhama run took over ${path} while this one ran, so this one stopped here. Run kodhama again once no other run is going.`);
    }
    // The owner file too: a run taking over a stale lock renames the folder
    // aside, which may change the folder's own time but never the file's, so
    // the file's time tells it whether the lock was refreshed meanwhile.
    utimesSync(join(path, RUN_LOCK_OWNER), now, now);
    utimesSync(path, now, now);
  }
};

/**
 * Effect: writes the lock, or deletes it when it holds no tool.
 * @param {string} path
 * @param {Lock} lock
 */
export const writeLock = (path, lock) => {
  keepAlive();
  if (Object.keys(lock.tools).length === 0) rmSync(path, { force: true });
  else writeAtomic(path, jsonText(lock));
};

/**
 * Effect: a hash of every file under a skill folder, the marker left out.
 * A symlink or other special file someone put there gets a hash no file
 * can have, so it shows as changed rather than being followed.
 * @param {string} dir
 * @returns {SkillHashes}
 */
export const hashTree = (dir) => {
  /** @type {Record<string, FileHash>} */
  const found = {};
  /** @param {string} rel */
  const walk = (rel) => {
    for (const name of readdirSync(join(dir, rel)).sort()) {
      const path = rel === "" ? name : `${rel}/${name}`;
      if (path === MARKER) continue;
      const stat = lstatSync(join(dir, path));
      if (stat.isDirectory()) walk(path);
      else if (stat.isFile()) {
        found[path] = { sha256: sha256(readFileSync(join(dir, path))), exec: (stat.mode & 0o111) !== 0 };
      } else found[path] = { sha256: "not a regular file", exec: false };
    }
  };
  walk("");
  return found;
};

/**
 * How a skill folder differs from what the lock recorded, one entry per
 * file, in path order.
 * @param {SkillHashes} locked
 * @param {SkillHashes} found
 * @returns {readonly { readonly kind: "hand-edited" | "added" | "deleted" | "exec changed", readonly file: string }[]}
 */
export const diffTree = (locked, found) =>
  [...new Set([...Object.keys(locked), ...Object.keys(found)])].sort().flatMap((file) => {
    const was = locked[file];
    const now = found[file];
    if (was === undefined) return [{ kind: /** @type {const} */ ("added"), file }];
    if (now === undefined) return [{ kind: /** @type {const} */ ("deleted"), file }];
    if (was.sha256 !== now.sha256) return [{ kind: /** @type {const} */ ("hand-edited"), file }];
    if (was.exec !== now.exec) return [{ kind: /** @type {const} */ ("exec changed"), file }];
    return [];
  });
