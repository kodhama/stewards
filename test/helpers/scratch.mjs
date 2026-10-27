// A whole machine in one temporary folder, for tests that run the program on
// real files: a home, a data home, Claude's and Codex's config folders, a
// folder of tool repos standing in for GitHub, and a temp folder. The
// environment is built from nothing, so no test can reach the real
// ~/.claude, ~/.codex, ~/.agents or ~/.local/share, and git runs with the
// user's and the system's config shut out.

import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import {
  chmodSync,
  mkdirSync,
  mkdtempSync,
  readdirSync,
  realpathSync,
  rmSync,
  symlinkSync,
  writeFileSync,
} from "node:fs";
import { devNull, tmpdir } from "node:os";
import { dirname, join, relative, sep } from "node:path";
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

/**
 * The default tool tree: two skills, one carrying an executable script.
 * @param {string} name
 * @returns {Record<string, string>}
 */
const toolTree = (name) => ({
  "kodhama.json": `${JSON.stringify({ name, skills: "skills" })}\n`,
  "README.md": `${name}\n`,
  "skills/alpha/SKILL.md": "---\nname: alpha\n---\nAlpha.\n",
  "skills/alpha/scripts/run.sh": "#!/bin/sh\necho alpha\n",
  "skills/beta/SKILL.md": "---\nname: beta\n---\nBeta.\n",
});

/**
 * Effect: every path under `root`, files and folders, relative and sorted.
 * @param {string} root
 * @returns {string[]}
 */
export const listTree = (root) =>
  readdirSync(root, { withFileTypes: true })
    .flatMap((entry) => {
      const path = join(root, entry.name);
      return entry.isDirectory() && !entry.isSymbolicLink()
        ? [entry.name, ...listTree(path).map((rel) => join(entry.name, rel))]
        : [entry.name];
    })
    .sort();

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
   * `v<version>` per version, in order. `change` replaces, deletes (`null`)
   * or adds files in the default tree, and adds symlinks, before the first
   * commit.
   * @param {string} name
   * @param {readonly string[]} versions
   * @param {{ readonly files?: Readonly<Record<string, string | null>>, readonly links?: Readonly<Record<string, string>> }} [change]
   * @returns {{ readonly path: string, readonly commit: (tag: string) => string }}
   */
  const fakeTool = (name, versions, change = {}) => {
    const path = join(at.source, name);
    mkdirSync(path);
    git(path, ["init", "-q", "-b", "main"]);
    const files = { ...toolTree(name), ...change.files };
    for (const [rel, text] of Object.entries(files)) {
      if (text === null) continue;
      mkdirSync(dirname(join(path, rel)), { recursive: true });
      writeFileSync(join(path, rel), text);
    }
    for (const [rel, target] of Object.entries(change.links ?? {})) {
      mkdirSync(dirname(join(path, rel)), { recursive: true });
      symlinkSync(target, join(path, rel));
    }
    // The script is executable on disk, so each later `git add` keeps the
    // bit, and in the index, for a filesystem git reads no modes from.
    const script = "skills/alpha/scripts/run.sh";
    if (files[script] !== null) chmodSync(join(path, script), 0o755);
    git(path, ["add", "-A"]);
    if (files[script] !== null) git(path, ["update-index", "--chmod=+x", script]);
    git(path, ["commit", "-q", "-m", "start"]);
    for (const version of versions) {
      writeFileSync(join(path, "VERSION"), `${version}\n`);
      git(path, ["add", "-A"]);
      git(path, ["commit", "-q", "-m", `release ${version}`]);
      git(path, ["tag", "-a", `v${version}`, "-m", `release ${version}`]);
    }
    return {
      path,
      commit: (tag) => git(path, ["rev-parse", `${tag}^{commit}`]).trim(),
    };
  };

  /**
   * Effect: runs the program with stdin closed and the scratch environment.
   * @param {readonly string[]} args
   * @param {{ readonly cwd?: string }} [options]
   */
  const kodhama = (args, { cwd = at.home } = {}) =>
    spawnSync(process.execPath, [BIN, ...args], {
      cwd,
      env,
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

  return {
    root,
    ...at,
    env,
    git,
    fakeTool,
    kodhama,
    written,
    /** @param {string} path */
    rel: (path) => relative(root, path),
  };
};
