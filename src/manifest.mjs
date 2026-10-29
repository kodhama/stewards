// `kodhama.json`, the file at a tool's root that says what the CLI installs:
// `{"name": "<tool>", "skills": "<dir>"}`. Every child folder of the skills
// folder that holds a SKILL.md is one skill, named after its folder. A file
// that says anything else is refused, so a typo cannot pass silently.

import { existsSync, lstatSync, readFileSync, readdirSync, realpathSync } from "node:fs";
import { isAbsolute, join, resolve, sep } from "node:path";

/** Tool and skill names: lowercase, so always safe as one path segment. */
export const NAME = /^[a-z][a-z0-9-]*$/;

/**
 * A tag as git might name one. It never starts with "-", so git cannot read
 * it as an option, and never holds "..", which git refuses in a ref anyway.
 * The command line, the lock and the markers all hold to it, so a tag
 * kodhama prints in a command is one its own parser would accept.
 */
export const TAG = /^(?!.*\.\.)[A-Za-z0-9][A-Za-z0-9._+/-]*$/;

/** A commit as git names one: a SHA-1 or SHA-256 in lowercase hex. */
export const COMMIT = /^[0-9a-f]{40}(?:[0-9a-f]{24})?$/;

const MANIFEST = "kodhama.json";

/**
 * The file the CLI writes into each skill folder it installs, naming the tool
 * that owns it. A tool may not ship one, or its copy would pass as owned.
 */
export const MARKER = ".kodhama-skill.json";

const KEYS = ["name", "skills", "helper"];

/**
 * What a valid `kodhama.json` says.
 * @typedef {{ readonly name: string, readonly skills: string }} Manifest
 */

/**
 * A `kodhama.json` read for the tool asked for, or why it cannot be used.
 * @param {string} text
 * @param {string} tool
 * @returns {{ readonly manifest: Manifest } | { readonly error: string }}
 */
export const parseManifest = (text, tool) => {
  /** @type {unknown} */
  let value;
  try {
    value = JSON.parse(text);
  } catch (error) {
    return { error: `${MANIFEST} is not valid JSON: ${error instanceof Error ? error.message : String(error)}` };
  }
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    return { error: `${MANIFEST} is not a JSON object.` };
  }
  const record = /** @type {Record<string, unknown>} */ (value);
  const unknown = Object.keys(record).filter((key) => !KEYS.includes(key));
  if (unknown.length > 0) {
    return { error: `${MANIFEST} has unknown key ${unknown.join(", ")}; it takes name and skills.` };
  }
  // A minimum helper version arrives with a later CLI; until then a tool that
  // needs one is refused rather than half-installed.
  if ("helper" in record) return { error: `${MANIFEST} names a helper version, which needs a later kodhama tag than this one.` };
  const { name, skills } = record;
  if (typeof name !== "string" || !NAME.test(name)) {
    return { error: `${MANIFEST} needs a name of lowercase letters, digits and "-".` };
  }
  if (name !== tool) return { error: `${MANIFEST} names ${name}, not ${tool}.` };
  if (typeof skills !== "string" || skills === "") {
    return { error: `${MANIFEST} needs skills, the folder its skills are in.` };
  }
  if (isAbsolute(skills) || skills.includes("\\") || skills.split("/").includes("..")) {
    return { error: `${MANIFEST} skills is ${JSON.stringify(skills)}; it must be a relative path with no ".." in it.` };
  }
  return { manifest: { name, skills } };
};

/**
 * Effect: the skills a checked-out tool offers, read through its
 * `kodhama.json`: the skills folder's real path and each skill's name, in
 * order. The skills folder must resolve inside the checkout, through any
 * symlink, and each skill folder must be a real folder with a path-safe name.
 * @param {string} dir the tool's checkout
 * @param {string} tool
 * @returns {{ readonly skillsDir: string, readonly skillsPath: string, readonly skills: readonly string[] } | { readonly error: string }}
 */
export const readManifest = (dir, tool) => {
  const path = join(dir, MANIFEST);
  if (!existsSync(path)) return { error: `${tool} has no ${MANIFEST} at its root, so kodhama cannot install it.` };
  if (!lstatSync(path).isFile()) return { error: `${tool}'s ${MANIFEST} is not a regular file.` };
  const parsed = parseManifest(readFileSync(path, "utf8"), tool);
  if ("error" in parsed) return { error: `${tool}: ${parsed.error}` };

  const root = realpathSync(dir);
  const wanted = resolve(root, parsed.manifest.skills);
  if (!existsSync(wanted)) return { error: `${tool}'s skills folder ${parsed.manifest.skills} does not exist.` };
  const skillsDir = realpathSync(wanted);
  if (skillsDir !== root && !skillsDir.startsWith(root + sep)) {
    return { error: `${tool}'s skills folder ${parsed.manifest.skills} resolves outside the tool's repo.` };
  }
  if (!lstatSync(skillsDir).isDirectory()) return { error: `${tool}'s skills folder ${parsed.manifest.skills} is not a folder.` };

  /** @type {string[]} */
  const skills = [];
  for (const entry of readdirSync(skillsDir, { withFileTypes: true })) {
    if (entry.isSymbolicLink()) {
      return { error: `${tool}: ${join(parsed.manifest.skills, entry.name)} is a symlink; kodhama copies only regular files and folders.` };
    }
    if (!entry.isDirectory() || !existsSync(join(skillsDir, entry.name, "SKILL.md"))) continue;
    if (!NAME.test(entry.name)) {
      return { error: `${tool}: ${entry.name} is not a skill name. Skill names are lowercase letters, digits and "-", starting with a letter.` };
    }
    skills.push(entry.name);
  }
  if (skills.length === 0) return { error: `${tool}'s skills folder ${parsed.manifest.skills} holds no skill (a folder with a SKILL.md).` };
  return { skillsDir, skillsPath: parsed.manifest.skills, skills: skills.sort() };
};
