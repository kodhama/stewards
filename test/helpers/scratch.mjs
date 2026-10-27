// A whole machine in one temporary folder, for tests that run the program on
// real files: a home, a data home, Claude's and Codex's config folders, a
// folder of tool repos standing in for GitHub, and a temp folder. The
// environment is built from nothing, so no test can reach the real
// ~/.claude, ~/.codex, ~/.agents or ~/.local/share, and git runs with the
// user's and the system's config shut out.

import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import {
  chmodSync,
  existsSync,
  lstatSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  readdirSync,
  readlinkSync,
  realpathSync,
  rmSync,
  symlinkSync,
  writeFileSync,
} from "node:fs";
import { devNull, tmpdir } from "node:os";
import { dirname, join, sep } from "node:path";
import { fileURLToPath } from "node:url";

// CI points this at the bin inside the extracted `npm pack` tarball, so the
// tests run what `npx github:` installs. The program itself never reads it.
const BIN =
  process.env.KODHAMA_BIN ??
  fileURLToPath(new URL("../../bin/kodhama.mjs", import.meta.url));

const FOLDERS = /** @type {const} */ ([
  "home",
  "data",
  "codex",
  "claude",
  "source",
  "tmp",
]);

const SCRIPT = "skills/alpha/scripts/run.sh";

/**
 * The default tool tree: two skills, one carrying an executable script.
 * @param {string} name
 * @returns {Record<string, string>}
 */
const toolTree = (name) => ({
  "kodhama.json": `${JSON.stringify({ name, skills: "skills" })}\n`,
  "README.md": `${name}\n`,
  "skills/alpha/SKILL.md": "---\nname: alpha\n---\nAlpha.\n",
  [SCRIPT]: "#!/bin/sh\necho alpha\n",
  "skills/beta/SKILL.md": "---\nname: beta\n---\nBeta.\n",
});

/**
 * Effect: writes files into a folder, making their folders; a `null` text
 * deletes the file.
 * @param {string} root
 * @param {Readonly<Record<string, string | null>>} files
 */
export const writeFiles = (root, files) => {
  for (const [rel, text] of Object.entries(files)) {
    if (text === null) {
      rmSync(join(root, rel), { force: true });
      continue;
    }
    mkdirSync(dirname(join(root, rel)), { recursive: true });
    writeFileSync(join(root, rel), text);
  }
};

/**
 * Effect: every path under `root`, files and folders, relative and sorted.
 * @param {string} root
 * @returns {string[]}
 */
const listTree = (root) =>
  readdirSync(root, { withFileTypes: true })
    .flatMap((entry) => {
      const path = join(root, entry.name);
      return entry.isDirectory() && !entry.isSymbolicLink()
        ? [entry.name, ...listTree(path).map((rel) => join(entry.name, rel))]
        : [entry.name];
    })
    .sort();

/**
 * @param {string} path
 * @returns {unknown}
 */
export const readJson = (path) => JSON.parse(readFileSync(path, "utf8"));

/** @param {string | Buffer} bytes */
export const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");

/**
 * Effect: a scratch machine, deleted when the test ends.
 * @param {import("node:test").TestContext} t
 */
export const scratch = (t) => {
  // The real path, so a path the program resolves and a path a test builds
  // agree on macOS, where the temp folder sits behind /var -> /private/var.
  const root = realpathSync(mkdtempSync(join(tmpdir(), "kodhama-test-")));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const at = Object.fromEntries(
    FOLDERS.map((folder) => [folder, join(root, folder)]),
  );
  for (const folder of FOLDERS) mkdirSync(at[folder]);

  const env = {
    PATH: process.env.PATH ?? "",
    HOME: at.home,
    XDG_DATA_HOME: at.data,
    CODEX_HOME: at.codex,
    CLAUDE_CONFIG_DIR: at.claude,
    KODHAMA_TOOL_SOURCE: at.source,
    TMPDIR: at.tmp,
    GIT_CONFIG_GLOBAL: devNull,
    GIT_CONFIG_NOSYSTEM: "1",
    GIT_TERMINAL_PROMPT: "0",
    // Git looks for a repo no higher than the root, so a repo the temp
    // folder happens to sit in cannot answer for a folder that has none.
    GIT_CEILING_DIRECTORIES: dirname(root),
    GIT_AUTHOR_NAME: "Fixture",
    GIT_AUTHOR_EMAIL: "fixture@example.invalid",
    GIT_COMMITTER_NAME: "Fixture",
    GIT_COMMITTER_EMAIL: "fixture@example.invalid",
  };
  for (const name of /** @type {const} */ ([
    "HOME",
    "XDG_DATA_HOME",
    "CODEX_HOME",
    "CLAUDE_CONFIG_DIR",
    "KODHAMA_TOOL_SOURCE",
    "TMPDIR",
  ])) {
    assert.ok(
      env[name].startsWith(root + sep),
      `${name} is ${env[name]}, outside the scratch root ${root}`,
    );
  }

  /**
   * Effect: runs git in a folder, with the scratch environment.
   * @param {string} cwd
   * @param {readonly string[]} args
   */
  const git = (cwd, args) =>
    execFileSync("git", args, { cwd, env, encoding: "utf8" });

  /**
   * Effect: a tool repo at `source/<name>`, one commit and one annotated tag
   * `v<version>` per version, in order. Each version rewrites alpha's
   * SKILL.md to name it, so two tags' copies differ. `change.files` replaces,
   * deletes (`null`) or adds files in the default tree and `change.links`
   * adds symlinks, before the first commit; `change.at[version]` changes
   * files in that version's commit.
   * @param {string} name
   * @param {readonly string[]} versions
   * @param {{
   *   readonly files?: Readonly<Record<string, string | null>>,
   *   readonly links?: Readonly<Record<string, string>>,
   *   readonly at?: Readonly<Record<string, Readonly<Record<string, string | null>>>>,
   * }} [change]
   * @returns {{ readonly path: string, readonly commit: (tag: string) => string }}
   */
  const fakeTool = (name, versions, change = {}) => {
    const path = join(at.source, name);
    mkdirSync(path);
    git(path, ["init", "-q", "-b", "main"]);
    writeFiles(path, { ...toolTree(name), ...change.files });
    for (const [rel, target] of Object.entries(change.links ?? {})) {
      mkdirSync(dirname(join(path, rel)), { recursive: true });
      symlinkSync(target, join(path, rel));
    }
    /** Effect: stages everything, with the script executable on disk, so
     * each `git add` keeps the bit, and in the index, for a filesystem git
     * reads no modes from. */
    const stage = () => {
      const script = existsSync(join(path, SCRIPT));
      if (script) chmodSync(join(path, SCRIPT), 0o755);
      git(path, ["add", "-A"]);
      if (script) git(path, ["update-index", "--chmod=+x", SCRIPT]);
    };
    stage();
    git(path, ["commit", "-q", "-m", "start"]);
    for (const version of versions) {
      writeFiles(path, {
        VERSION: `${version}\n`,
        ...(existsSync(join(path, "skills/alpha/SKILL.md"))
          ? { "skills/alpha/SKILL.md": `---\nname: alpha\n---\nAlpha ${version}.\n` }
          : {}),
        ...change.at?.[version],
      });
      stage();
      git(path, ["commit", "-q", "-m", `release ${version}`]);
      git(path, ["tag", "-a", `v${version}`, "-m", `release ${version}`]);
    }
    return {
      path,
      commit: (tag) => git(path, ["rev-parse", `${tag}^{commit}`]).trim(),
    };
  };

  /**
   * Effect: a git repo at `home/<name>` to install into at project scope.
   * @param {string} name
   */
  const project = (name) => {
    const path = join(at.home, name);
    mkdirSync(path);
    git(path, ["init", "-q", "-b", "main"]);
    return path;
  };

  /**
   * Effect: runs the program with stdin closed and the scratch environment,
   * with `env` laid over it.
   * @param {readonly string[]} args
   * @param {{ readonly cwd?: string, readonly env?: Readonly<Record<string, string>> }} [options]
   */
  const kodhama = (args, { cwd = at.home, env: over = {} } = {}) =>
    spawnSync(process.execPath, [BIN, ...args], {
      cwd,
      env: { ...env, ...over },
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"],
    });

  /**
   * Effect: every path the program could have written, which is everything
   * under the root but the tool repos, relative to the root.
   */
  const written = () =>
    listTree(root).filter(
      (rel) => rel !== "source" && !rel.startsWith(`source${sep}`),
    );

  /**
   * Effect: what the program could have changed: each written path, with a
   * file's bytes, mode and mtime and a symlink's target. Two equal states
   * mean nothing was written in between.
   */
  const state = () =>
    Object.fromEntries(
      written().map((rel) => {
        const path = join(root, rel);
        const stat = lstatSync(path);
        if (stat.isSymbolicLink()) return [rel, `link ${readlinkSync(path)}`];
        if (stat.isDirectory()) return [rel, "dir"];
        return [rel, `${stat.mode} ${stat.mtimeMs} ${sha256(readFileSync(path))}`];
      }),
    );

  return {
    root,
    ...at,
    claudeSkills: join(at.claude, "skills"),
    codexSkills: join(at.home, ".agents", "skills"),
    lock: join(at.data, "kodhama", "lock.json"),
    prev: join(at.data, "kodhama", "prev"),
    env,
    git,
    fakeTool,
    project,
    kodhama,
    written,
    state,
  };
};
