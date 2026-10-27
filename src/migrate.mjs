// The grove guard and `--migrate`. A plugin enable for a tool, in Claude's
// settings or Codex's config.toml, would load the plugin's skills beside the
// copies kodhama installs, so install and update refuse while one is on.
// `--migrate` takes a tool's enables and marketplace out of the user-level
// files only, after writing a receipt holding each file's original bytes.
// The TOML side is line-based and refuses anything it does not recognise,
// so it needs no parser and edits no line it was not asked to.

import { chmodSync, existsSync, mkdirSync, readFileSync, realpathSync, statSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";

import { claudeHome, homeOf, isRecord, jsonText, sha256, stateHome, writeAtomic } from "./lock.mjs";

/**
 * An enable the guard found: the file, what in it, whether it is a user-level
 * file, and whether `--migrate` knows how to take it out.
 * @typedef {{ readonly path: string, readonly key: string, readonly user: boolean, readonly editable: boolean }} Hit
 */

/**
 * One file `--migrate` edits: its text before and after, and each item it
 * takes out with the text that item had.
 * @typedef {{
 *   readonly path: string,
 *   readonly before: string,
 *   readonly after: string,
 *   readonly removed: readonly { readonly key: string, readonly text: string }[],
 * }} Edit
 */

/** @param {NodeJS.ProcessEnv} env */
const claudeSettings = (env) => join(claudeHome(env), "settings.json");

/** @param {NodeJS.ProcessEnv} env */
const codexConfig = (env) => join(env.CODEX_HOME || join(homeOf(env), ".codex"), "config.toml");

/**
 * The patterns for one tool. Its name is lowercase letters, digits and "-",
 * so it goes into a pattern as it is.
 * @param {string} tool
 */
const patterns = (tool) => ({
  mention: new RegExp(`(?<![a-z0-9-])${tool}@`),
  market: new RegExp(`marketplaces\\s*\\.\\s*(?:"${tool}"|'${tool}'|${tool})(?![a-z0-9-])`),
  plugin: new RegExp(`^\\[\\s*plugins\\s*\\.\\s*(["'])${tool}@[^"']*\\1\\s*(\\.[^\\]]*)?\\]\\s*(?:#.*)?$`),
  marketplace: new RegExp(`^\\[\\s*marketplaces\\s*\\.\\s*(?:(["'])${tool}\\1|${tool})\\s*(\\.[^\\]]*)?\\]\\s*(?:#.*)?$`),
});

/**
 * A recognised table: its header's key, and whether it is a plugin's own
 * table (not a subtable or a marketplace), where `enabled` lives.
 * @typedef {{ readonly key: string, readonly enables: boolean }} Table
 */

/**
 * How far a value line opens (or closes) arrays and inline tables, counting
 * no bracket inside a quoted string or after a comment.
 * @param {string} line
 */
const bracketDepth = (line) => {
  let depth = 0;
  /** @type {string | undefined} */
  let quote;
  for (let at = 0; at < line.length; at += 1) {
    const char = line[at];
    if (quote !== undefined) {
      if (quote === '"' && char === "\\") at += 1;
      else if (char === quote) quote = undefined;
    } else if (char === "#") break;
    else if (char === '"' || char === "'") quote = char;
    else if (char === "[" || char === "{") depth += 1;
    else if (char === "]" || char === "}") depth -= 1;
  }
  return depth;
};

/**
 * config.toml split into lines, each with the recognised table it sits in,
 * if any, and the bracket depth after it. A table runs from its header to
 * just before the next line whose first non-space character is `[` while no
 * multi-line value is open; inside one, such a line is part of the value.
 * @param {string} text
 * @param {string} tool
 * @returns {readonly { readonly line: string, readonly at: number, readonly text: string, readonly header: boolean, readonly table: Table | undefined, readonly depth: number }[]}
 */
const tomlRows = (text, tool) => {
  const { plugin, marketplace } = patterns(tool);
  /** @type {Table | undefined} */
  let table;
  let depth = 0;
  return text.split(/(?<=\n)/).map((line, at) => {
    const trimmed = line.trim();
    const header = depth === 0 && trimmed.startsWith("[");
    if (!header) depth += bracketDepth(trimmed);
    if (header) {
      const asPlugin = plugin.exec(trimmed);
      const recognised = asPlugin ?? marketplace.exec(trimmed);
      table =
        recognised === null
          ? undefined
          : {
              key: trimmed.replace(/\s*#.*$/, "").slice(1, -1).trim(),
              enables: asPlugin !== null && asPlugin[2] === undefined,
            };
    }
    return { line, at, text: trimmed, header, table, depth };
  });
};

/** @param {string} text */
const isComment = (text) => text === "" || text.startsWith("#");

/**
 * Effect: the enables for `tool` in one config file. A form the guard does
 * not recognise counts, so it fails closed.
 * @param {{ readonly path: string, readonly kind: "json" | "toml", readonly user: boolean }} file
 * @param {string} tool
 * @returns {readonly Hit[]}
 */
const hitsIn = ({ path, kind, user }, tool) => {
  if (!existsSync(path)) return [];
  const text = readFileSync(path, "utf8");
  if (kind === "json") {
    /** @type {unknown} */
    let value;
    try {
      value = JSON.parse(text);
    } catch {
      return [{ path, key: "the whole file, which is not valid JSON", user, editable: false }];
    }
    const enabled = isRecord(value) ? value.enabledPlugins : undefined;
    return isRecord(enabled)
      ? Object.keys(enabled)
          .filter((key) => key.startsWith(`${tool}@`) && enabled[key] === true)
          .map((key) => ({ path, key: `enabledPlugins[${JSON.stringify(key)}]`, user, editable: true }))
      : [];
  }
  const { mention } = patterns(tool);
  return tomlRows(text, tool).flatMap(({ at, text: line, header, table }) => {
    if (isComment(line)) return [];
    if (table?.enables && !header && /^(?:enabled|"enabled"|'enabled')\s*=\s*true\s*(?:#.*)?$/.test(line)) {
      return [{ path, key: `[${table.key}] enabled`, user, editable: true }];
    }
    if (table === undefined && mention.test(line)) {
      return [{ path, key: `line ${at + 1}, a form kodhama does not edit; edit it by hand`, user, editable: false }];
    }
    return [];
  });
};

/**
 * Effect: every enable for `tool` that would load in the scope: the user
 * files, and at project scope the repo's files too.
 * @param {string} tool
 * @param {"user" | "project"} scope
 * @param {NodeJS.ProcessEnv} env
 * @param {string | undefined} root
 * @returns {readonly Hit[]}
 */
export const findEnables = (tool, scope, env, root) =>
  [
    { path: claudeSettings(env), kind: /** @type {const} */ ("json"), user: true },
    { path: codexConfig(env), kind: /** @type {const} */ ("toml"), user: true },
    ...(scope === "project" && root !== undefined
      ? [
          { path: join(root, ".claude", "settings.json"), kind: /** @type {const} */ ("json"), user: false },
          { path: join(root, ".claude", "settings.local.json"), kind: /** @type {const} */ ("json"), user: false },
          { path: join(root, ".codex", "config.toml"), kind: /** @type {const} */ ("toml"), user: false },
        ]
      : []),
  ].flatMap((file) => hitsIn(file, tool));

/**
 * The refusal for a set of enables, or `undefined` when the run may go on:
 * there are none, or `--migrate` was asked and can take every one out.
 * @param {string} tool
 * @param {readonly Hit[]} hits
 * @param {boolean} migrate
 * @param {string} fix what to do about the enables, for a run without --migrate
 * @returns {readonly string[] | undefined}
 */
export const guardRefusal = (tool, hits, migrate, fix) => {
  const blocking = migrate ? hits.filter((hit) => !hit.user || !hit.editable) : hits;
  if (blocking.length === 0) return undefined;
  return [
    `${tool} is enabled as a plugin, which would load beside the skills kodhama copies:`,
    ...blocking.map((hit) => `  ${hit.path}: ${hit.key}${hit.user ? "" : " (a project file, which --migrate never edits)"}`),
    migrate ? "--migrate edits only user-level settings in a form it recognises, so it changed nothing." : fix,
  ];
};

/**
 * Effect: the edits `--migrate` would make to the user-level files, or why
 * it must leave them to be edited by hand. Nothing is written.
 * @param {string} tool
 * @param {NodeJS.ProcessEnv} env
 * @returns {{ readonly edits: readonly Edit[], readonly touchedClaude: boolean } | { readonly error: string }}
 */
export const planMigration = (tool, env) => {
  /** @type {Edit[]} */
  const edits = [];

  const settings = claudeSettings(env);
  if (existsSync(settings)) {
    const before = readFileSync(settings, "utf8");
    /** @type {unknown} */
    let value;
    try {
      value = JSON.parse(before);
    } catch {
      return { error: `${settings} is not valid JSON; edit it by hand.` };
    }
    /** @type {{ key: string, text: string }[]} */
    const removed = [];
    if (isRecord(value) && isRecord(value.enabledPlugins)) {
      const enabled = value.enabledPlugins;
      for (const key of Object.keys(enabled).filter((name) => name.startsWith(`${tool}@`))) {
        removed.push({ key: `enabledPlugins[${JSON.stringify(key)}]`, text: JSON.stringify(enabled[key]) });
        delete enabled[key];
      }
    }
    if (isRecord(value) && isRecord(value.extraKnownMarketplaces) && Object.hasOwn(value.extraKnownMarketplaces, tool)) {
      const markets = value.extraKnownMarketplaces;
      removed.push({ key: `extraKnownMarketplaces.${tool}`, text: JSON.stringify(markets[tool]) });
      delete markets[tool];
    }
    if (removed.length > 0) edits.push({ path: settings, before, after: `${JSON.stringify(value, null, 2)}\n`, removed });
  }

  const config = codexConfig(env);
  if (existsSync(config)) {
    const before = readFileSync(config, "utf8");
    const { mention, market } = patterns(tool);
    /** @type {{ key: string, text: string }[]} */
    const removed = [];
    let after = "";
    const rows = tomlRows(before, tool);
    for (const { line, at, text, header, table } of rows) {
      if (table === undefined) {
        if (!isComment(text) && (mention.test(text) || market.test(text))) {
          return { error: `${config} line ${at + 1} mentions ${tool} in a form kodhama does not edit; edit it by hand.` };
        }
        after += line;
      } else if (header) removed.push({ key: table.key, text: line });
      else removed[removed.length - 1] = { key: table.key, text: removed[removed.length - 1].text + line };
    }
    const multiline = removed.find((item) => item.text.includes('"""') || item.text.includes("'''"));
    if (removed.length > 0 && (rows.at(-1)?.depth ?? 0) !== 0) {
      return { error: `${config} ends inside an open array or inline table, so kodhama cannot tell where a table ends; edit it by hand.` };
    }
    if (multiline !== undefined) {
      return { error: `${config}: the [${multiline.key}] table holds a multi-line string, which kodhama does not cut; edit it by hand.` };
    }
    if (removed.length > 0) edits.push({ path: config, before, after, removed });
  }
  return { edits, touchedClaude: edits.some(({ path }) => path === settings) };
};

/**
 * Effect: writes the receipt, with exclusive create so no earlier receipt
 * is ever overwritten, then applies each edit through a temp file, keeping
 * the file's mode. A symlinked config is written through its link, so the
 * link survives, and the receipt names both paths. The receipt holds whole
 * config files, which may hold secrets, so only the user can read it.
 * Returns the receipt's path.
 * @param {string} tool
 * @param {readonly Edit[]} edits
 * @param {NodeJS.ProcessEnv} env
 * @returns {string}
 */
export const applyMigration = (tool, edits, env) => {
  const at = new Date().toISOString().replace(/\.\d+Z$/, "Z");
  const receipt = join(stateHome(env), "receipts", `migrate-${tool}-${at.replace(/[-:]/g, "")}.json`);
  const resolved = edits.map(({ path }) => realpathSync(path));
  mkdirSync(dirname(receipt), { recursive: true, mode: 0o700 });
  chmodSync(dirname(receipt), 0o700);
  writeFileSync(
    receipt,
    jsonText({
      receipt: 1,
      kind: "migrate",
      tool,
      at,
      files: edits.map(({ path, before, after, removed }, index) => ({
        path,
        ...(resolved[index] === path ? {} : { resolved: resolved[index] }),
        sha256_before: sha256(before),
        sha256_after: sha256(after),
        original: before,
        removed,
      })),
    }),
    { flag: "wx", mode: 0o600 },
  );
  edits.forEach(({ path, after }, index) => writeAtomic(resolved[index], after, statSync(path).mode & 0o7777));
  return receipt;
};
