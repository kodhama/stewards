// Fetching a tool: finding its tag on its repo, cloning that tag into a
// fresh temp folder, and reading what it offers through `kodhama.json`. The
// clone is always deleted afterwards, and nothing outside it is written, so a
// missing tag, a tool with no tags or a bad manifest leaves no trace. Copying
// a skill out keeps its bytes and exec bit and takes regular files only.

import { execFileSync } from "node:child_process";
import {
  chmodSync,
  constants,
  copyFileSync,
  lstatSync,
  mkdirSync,
  mkdtempSync,
  readdirSync,
  rmSync,
  statSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";

import { isSource } from "./lock.mjs";
import { MARKER, readManifest } from "./manifest.mjs";

const GIT_TIMEOUT_MS = 5 * 60 * 1000;

// A stable release tag. Numbers carry no leading zero, as semver has it.
const STABLE = /^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/;

/**
 * One skill in a fetched tool: its name, its folder in the clone, and its
 * files relative to that folder, in order.
 * @typedef {{ readonly name: string, readonly dir: string, readonly files: readonly string[] }} Skill
 */

/**
 * A tool fetched at a tag. `commit` is the clone's HEAD, the tag's commit
 * rather than the tag object. The skill folders exist only while the
 * callback given to `withTool` runs.
 * @typedef {{
 *   readonly tool: string,
 *   readonly tag: string,
 *   readonly commit: string,
 *   readonly source: string,
 *   readonly skills: readonly Skill[],
 * }} Fetched
 */

/**
 * Where a tool's repo is: GitHub, or with `KODHAMA_TOOL_SOURCE` set, the
 * repo of that name in that folder. The `file://` form makes git honour
 * `--depth`, which it ignores on a plain-path clone.
 * @param {string} tool
 * @param {NodeJS.ProcessEnv} env
 * @returns {string}
 */
export const toolSource = (tool, env) =>
  env.KODHAMA_TOOL_SOURCE
    ? `file://${resolve(env.KODHAMA_TOOL_SOURCE, tool)}`
    : `https://github.com/kodhama/${tool}.git`;

/**
 * Whether one version is higher than another, comparing major, minor and
 * patch as numbers.
 * @param {readonly number[]} a
 * @param {readonly number[]} b
 */
const isNewer = (a, b) => {
  const at = a.findIndex((part, index) => part !== b[index]);
  return at !== -1 && a[at] > b[at];
};

/**
 * The tag to install: the one asked for, if the repo has it; otherwise the
 * highest stable `vX.Y.Z`, in numeric order, so `v0.10.0` beats `v0.9.0`.
 * Pre-releases and other tags count only when asked for by name.
 * @param {readonly string[]} tags
 * @param {string | undefined} wanted
 * @returns {string | undefined}
 */
export const pickTag = (tags, wanted) => {
  if (wanted !== undefined) return tags.includes(wanted) ? wanted : undefined;
  /** @type {{ tag: string, parts: number[] } | undefined} */
  let best;
  for (const tag of tags) {
    const match = STABLE.exec(tag);
    if (match === null) continue;
    const parts = match.slice(1).map(Number);
    if (best === undefined || isNewer(parts, best.parts)) best = { tag, parts };
  }
  return best?.tag;
};

/**
 * Effect: runs git, asking for nothing on the terminal, and returns what it
 * printed or why it failed.
 * @param {readonly string[]} args
 * @param {NodeJS.ProcessEnv} env
 * @param {string} [cwd]
 * @returns {{ readonly ok: true, readonly out: string } | { readonly ok: false, readonly out: string }}
 */
export const git = (args, env, cwd) => {
  try {
    return {
      ok: true,
      out: execFileSync("git", args, {
        cwd,
        encoding: "utf8",
        stdio: ["ignore", "pipe", "pipe"],
        timeout: GIT_TIMEOUT_MS,
        // An askpass program or ssh the user configured may still ask; the
        // time limit bounds it.
        env: { ...env, GIT_TERMINAL_PROMPT: "0" },
      }),
    };
  } catch (error) {
    const failed = /** @type {{ stderr?: unknown, message: string }} */ (error);
    const said = typeof failed.stderr === "string" && failed.stderr.trim() !== "" ? failed.stderr : failed.message;
    return { ok: false, out: said.replace(/\s*\n\s*/g, " ").trim() };
  }
};

/**
 * Effect: every file under a folder, relative and in order, or why the
 * folder cannot be copied: a symlink or any other file that is neither a
 * regular file nor a folder refuses the whole folder.
 * @param {string} dir
 * @param {string} [label] the folder's path as messages name it
 * @returns {{ readonly files: readonly string[] } | { readonly error: string }}
 */
export const listFiles = (dir, label = "") => {
  /** @type {string[]} */
  const files = [];
  /** @param {string} rel */
  const walk = (rel) => {
    for (const name of readdirSync(join(dir, rel)).sort()) {
      const path = join(rel, name);
      const stat = lstatSync(join(dir, path));
      if (stat.isSymbolicLink()) return `${join(label, path)} is a symlink; kodhama copies only regular files and folders.`;
      if (stat.isDirectory()) {
        const refused = walk(path);
        if (refused !== undefined) return refused;
      } else if (stat.isFile()) files.push(path);
      else return `${join(label, path)} is not a regular file or a folder.`;
    }
    return undefined;
  };
  const refused = walk("");
  return refused === undefined ? { files } : { error: refused };
};

/**
 * Effect: copies `files` from one folder into another, making folders as it
 * goes. Each copy has the source's bytes and permission bits, so a script's
 * exec bit survives. A file already at the destination is an error, not
 * overwritten.
 * @param {string} from
 * @param {string} to
 * @param {readonly string[]} files relative paths, as `listFiles` gives them
 */
export const copyFiles = (from, to, files) => {
  for (const rel of files) {
    const source = join(from, rel);
    const target = join(to, rel);
    mkdirSync(dirname(target), { recursive: true });
    copyFileSync(source, target, constants.COPYFILE_EXCL);
    chmodSync(target, statSync(source).mode & 0o777);
  }
};

/**
 * Effect: fetches a tool at a tag into a fresh temp folder, hands it to
 * `use`, and deletes the folder however `use` ends. Nothing is handed over,
 * and nothing is written outside the temp folder, unless the tag resolves,
 * the clone succeeds and the manifest and every skill folder validate.
 * @template T
 * @param {string} tool
 * @param {string | undefined} wanted the tag asked for, or none for the newest
 * @param {{ readonly env: NodeJS.ProcessEnv, readonly tmp?: string, readonly source?: string }} options
 *   `source` overrides where the repo is, as `update` does with the lock's
 * @param {(fetched: Fetched) => T} use
 * @returns {{ readonly value: T } | { readonly error: string }}
 */
export const withTool = (tool, wanted, { env, tmp = tmpdir(), source = toolSource(tool, env) }, use) => {
  if (!isSource(source)) return { error: `${tool}'s source ${source} is not an https:// or file:// URL.` };
  const listed = git(["ls-remote", "--tags", "--refs", "--", source], env);
  if (!listed.ok) return { error: `kodhama could not list the tags of ${tool} at ${source}: ${listed.out}` };
  const tags = listed.out
    .split("\n")
    .map((line) => line.split("\t")[1] ?? "")
    .filter((ref) => ref.startsWith("refs/tags/"))
    .map((ref) => ref.slice("refs/tags/".length));
  const tag = pickTag(tags, wanted);
  if (tag === undefined) {
    return {
      error:
        wanted === undefined
          ? `${tool} at ${source} has no vX.Y.Z tag to install.`
          : `${tool} at ${source} has no tag ${wanted}.`,
    };
  }

  const dir = mkdtempSync(join(tmp, `kodhama-${tool}-`));
  try {
    const cloned = git(
      ["-c", "advice.detachedHead=false", "clone", "--quiet", "--depth", "1", "--branch", tag, "--", source, dir],
      env,
    );
    if (!cloned.ok) return { error: `kodhama could not clone ${tool} at ${tag}: ${cloned.out}` };
    const head = git(["rev-parse", "HEAD"], env, dir);
    if (!head.ok) return { error: `kodhama could not read the commit of ${tool} at ${tag}: ${head.out}` };

    const read = readManifest(dir, tool);
    if ("error" in read) return read;
    /** @type {Skill[]} */
    const skills = [];
    for (const name of read.skills) {
      const skillDir = join(read.skillsDir, name);
      const listed = listFiles(skillDir, join(read.skillsPath, name));
      if ("error" in listed) return { error: `${tool}: ${listed.error}` };
      if (listed.files.includes(MARKER)) {
        return { error: `${tool}: ${join(read.skillsPath, name)} ships its own ${MARKER}, the file kodhama writes to mark a folder it installed.` };
      }
      skills.push({ name, dir: skillDir, files: listed.files });
    }
    return { value: use({ tool, tag, commit: head.out.trim(), source, skills }) };
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
};
