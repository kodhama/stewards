// The command line: which verb was asked for, on which tool, tag, scope and
// harnesses, and running it. Nothing here prompts, so a command run with no
// terminal completes or refuses on its own.

import { realpathSync } from "node:fs";

import { git } from "./fetch.mjs";
import { NAME } from "./manifest.mjs";
import { HARNESSES, outsideRoot, places } from "./targets.mjs";
import { check, install, remove, update } from "./verbs.mjs";

/**
 * What a command ends with: its exit code and the lines it prints.
 * @typedef {{ readonly code: number, readonly lines: readonly string[] }} Outcome
 */

/**
 * A command line as kodhama reads it, or why it cannot.
 * @typedef {{
 *   readonly command: "install" | "update" | "check" | "remove",
 *   readonly tool: string | undefined,
 *   readonly tag: string | undefined,
 *   readonly scope: "user" | "project",
 *   readonly harnesses: readonly ("claude" | "codex")[],
 *   readonly migrate: boolean,
 * } | { readonly error: string }} Parsed
 */

const USAGE = [
  "Usage: kodhama <command> [options]",
  "",
  "  install <tool>[#<tag>]  copy a tool's skills into the harnesses' skills folders",
  "  update <tool>[#<tag>]   move installed skills to a tag, the newest by default",
  "  check [<tool>]          compare installed skills with the lock, offline",
  "  remove <tool>           move a tool's installed skills out to prev/",
  "",
  "  --scope user|project    the user's folders, or this git repo's (default user)",
  "  --harness claude|codex  install and remove: one harness; repeat for both (default both)",
  "  --migrate               install: first take the tool's plugin enables out of user settings",
].join("\n");

// A tag as git might name one. It never starts with "-", so git cannot read
// it as an option, and never holds "..", which git refuses in a ref anyway.
const TAG = /^(?!.*\.\.)[A-Za-z0-9][A-Za-z0-9._+/-]*$/;

const SCOPES = /** @type {const} */ (["user", "project"]);

/**
 * Each verb's flags, and whether it needs a tool, may take one, or may name a
 * tag on it, as the verb table says.
 */
const VERBS = /** @type {const} */ ({
  install: { flags: ["--scope", "--harness", "--migrate"], tool: "required", tag: true },
  update: { flags: ["--scope"], tool: "required", tag: true },
  check: { flags: ["--scope"], tool: "optional", tag: false },
  remove: { flags: ["--scope", "--harness"], tool: "required", tag: false },
});

/**
 * @param {string} word
 * @returns {word is keyof typeof VERBS}
 */
const isVerb = (word) => Object.hasOwn(VERBS, word);

/**
 * `<tool>[#<tag>]` split, with a tag that starts with a digit read as its
 * `v` tag, so `grove#0.3.0` asks for `v0.3.0`.
 * @param {string} word
 * @returns {{ readonly tool: string, readonly tag: string | undefined } | { readonly error: string }}
 */
const toolSpec = (word) => {
  const hash = word.indexOf("#");
  const tool = hash === -1 ? word : word.slice(0, hash);
  if (!NAME.test(tool)) {
    return {
      error: `${tool} is not a tool name. Tool names are lowercase letters, digits and "-", starting with a letter.`,
    };
  }
  if (hash === -1) return { tool, tag: undefined };
  const tag = word.slice(hash + 1);
  if (!TAG.test(tag)) return { error: `${JSON.stringify(tag)} is not a tag.` };
  return { tool, tag: /^\d/.test(tag) ? `v${tag}` : tag };
};

/**
 * The command a command line asks for.
 * @param {readonly string[]} args the words after the program's name
 * @returns {Parsed}
 */
export const parseArgs = (args) => {
  const [command, ...rest] = args;
  if (command === undefined) return { error: "No command given." };
  if (command === "uninstall") {
    return { error: "Unknown command: uninstall. To take a tool's skills back out, use remove." };
  }
  if (!isVerb(command)) return { error: `Unknown command: ${command}.` };
  const verb = VERBS[command];

  /** @type {string[]} */
  const words = [];
  /** @type {Map<string, string[]>} */
  const given = new Map();
  for (let at = 0; at < rest.length; at += 1) {
    const arg = rest[at];
    if (!arg.startsWith("-")) {
      words.push(arg);
      continue;
    }
    const equals = arg.indexOf("=");
    const flag = equals === -1 ? arg : arg.slice(0, equals);
    if (!(/** @type {readonly string[]} */ (verb.flags).includes(flag))) {
      return { error: `${command} does not take ${flag}.` };
    }
    if (flag === "--migrate") {
      if (equals !== -1) return { error: "--migrate takes no value." };
      given.set(flag, []);
      continue;
    }
    const value = equals === -1 ? rest[(at += 1)] : arg.slice(equals + 1);
    if (value === undefined || value === "") return { error: `${flag} needs a value.` };
    given.set(flag, [...(given.get(flag) ?? []), value]);
  }

  if (words.length > 1) return { error: `${command} takes one tool; got ${words.join(" ")}.` };
  if (words.length === 0 && verb.tool === "required") {
    return { error: `${command} needs a tool to work on.` };
  }
  const spec = words.length === 0 ? { tool: undefined, tag: undefined } : toolSpec(words[0]);
  if ("error" in spec) return spec;
  if (spec.tag !== undefined && !verb.tag) {
    return { error: `${command} works on what is installed, so it takes no #<tag>.` };
  }

  const scopes = given.get("--scope") ?? ["user"];
  if (scopes.length > 1) return { error: "--scope is given more than once." };
  const scope = SCOPES.find((known) => known === scopes[0]);
  if (scope === undefined) return { error: `--scope is user or project, not ${scopes[0]}.` };

  const named = given.get("--harness") ?? HARNESSES;
  const unknown = named.filter((name) => !HARNESSES.some((known) => known === name));
  if (unknown.length > 0) {
    return { error: `--harness is claude or codex, not ${unknown.join(", ")}.` };
  }

  return {
    command,
    tool: spec.tool,
    tag: spec.tag,
    scope,
    harnesses: HARNESSES.filter((harness) => named.includes(harness)),
    migrate: given.has("--migrate"),
  };
};

/**
 * Effect: the real path of the git repo that holds `cwd`, or `undefined`
 * when there is none.
 * @param {string} cwd
 * @param {NodeJS.ProcessEnv} env
 */
const repoRoot = (cwd, env) => {
  const found = git(["rev-parse", "--show-toplevel"], env, cwd);
  return found.ok ? realpathSync(found.out.trim()) : undefined;
};

/**
 * Effect: runs a command line. `cwd` is where project scope looks for its
 * git repo, and `env` is where the harness homes and the tool source come
 * from.
 * @param {readonly string[]} args the words after the program's name
 * @param {string} cwd
 * @param {NodeJS.ProcessEnv} [env]
 * @returns {Promise<Outcome>}
 */
export const run = async (args, cwd, env = process.env) => {
  const parsed = parseArgs(args);
  if ("error" in parsed) return { code: 2, lines: [parsed.error, "", USAGE] };
  const root = parsed.scope === "project" ? repoRoot(cwd, env) : undefined;
  if (parsed.scope === "project" && root === undefined) {
    return { code: 1, lines: [`${cwd} is not inside a git repo. Project scope installs into one.`] };
  }
  const context = { env, scope: parsed.scope, root, where: places(parsed.scope, env, root) };
  const { command, tool } = parsed;
  if (command === "check") return check(parsed, context);
  // Every verb but check needs a tool, which the parser has made sure of.
  if (tool === undefined) throw new Error(`${command} needs a tool`);
  const outside = root === undefined ? [] : outsideRoot(root);
  if (outside.length > 0) {
    return {
      code: 1,
      lines: [...outside.map((path) => `${path} resolves outside ${root}.`), "At project scope kodhama writes only inside the repo, so it wrote nothing."],
    };
  }
  if (command === "install") return install({ ...parsed, tool }, context);
  if (command === "update") return update({ ...parsed, tool }, context);
  return remove({ ...parsed, tool }, context);
};
