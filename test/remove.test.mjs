// `remove`: moving a tool's installed skills out to prev/, only where the
// folder is marked as the tool's and in the lock, and never deleting one.

import assert from "node:assert/strict";
import { existsSync, mkdirSync, readFileSync, readdirSync, rmSync, statSync, symlinkSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { pathToFileURL } from "node:url";
import { test } from "node:test";

import { readJson, scratch } from "./helpers/scratch.mjs";

test("remove moves only marked folders to prev/, names the rest, and deletes the empty lock", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);
  assert.equal(machine.kodhama(["install", "demo"]).status, 0);
  const unmarked = join(machine.codexSkills, "alpha");
  rmSync(join(unmarked, ".kodhama-skill.json"));
  writeFileSync(join(machine.claudeSkills, "beta", "SKILL.md"), "edited beta\n");
  const kept = readFileSync(join(unmarked, "SKILL.md"));

  const outcome = machine.kodhama(["remove", "demo"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  assert.ok(outcome.stdout.includes(unmarked), outcome.stdout);
  assert.ok(outcome.stdout.includes(`hand-edited ${join(machine.claudeSkills, "beta", "SKILL.md")}`), outcome.stdout);
  assert.deepEqual(readdirSync(machine.claudeSkills), []);
  assert.deepEqual(readdirSync(machine.codexSkills), ["alpha"]);
  assert.deepEqual(readFileSync(join(unmarked, "SKILL.md")), kept);
  assert.deepEqual(readdirSync(join(machine.prev, "claude")).sort(), ["alpha", "beta"]);
  assert.deepEqual(readdirSync(join(machine.prev, "codex")), ["beta"]);
  assert.equal(readFileSync(join(machine.prev, "claude", "beta", "SKILL.md"), "utf8"), "edited beta\n");
  assert.ok(!existsSync(machine.lock));
});

test("remove --harness codex leaves the Claude copies and the lock's claude entry", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);
  machine.fakeTool("other", ["1.0.0"], { files: { "skills/alpha/SKILL.md": null, "skills/alpha/scripts/run.sh": null, "skills/beta/SKILL.md": null, "skills/omega/SKILL.md": "Omega.\n" } });
  assert.equal(machine.kodhama(["install", "demo"]).status, 0);
  assert.equal(machine.kodhama(["install", "other"]).status, 0);

  const outcome = machine.kodhama(["remove", "demo", "--harness", "codex"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  assert.deepEqual(readdirSync(machine.claudeSkills).sort(), ["alpha", "beta", "omega"]);
  assert.deepEqual(readdirSync(machine.codexSkills), ["omega"]);
  const tools = /** @type {any} */ (readJson(machine.lock)).tools;
  assert.deepEqual(tools.demo.harnesses, ["claude"]);
  assert.deepEqual(tools.other.harnesses, ["claude", "codex"]);
  assert.equal(machine.kodhama(["check"]).status, 0);

  assert.equal(machine.kodhama(["remove", "demo"]).status, 0);
  assert.deepEqual(Object.keys(/** @type {any} */ (readJson(machine.lock)).tools), ["other"]);
});

test("remove of a tool that is not installed refuses", (t) => {
  const machine = scratch(t);

  const outcome = machine.kodhama(["remove", "demo"]);

  assert.equal(outcome.status, 1);
  assert.match(outcome.stderr, /demo is not installed/);
});

test("remove --harness codex leaves a skills folder Claude shares through a symlink, and drops only codex from the lock", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);
  mkdirSync(join(machine.home, ".agents"));
  mkdirSync(machine.claudeSkills);
  symlinkSync(machine.claudeSkills, machine.codexSkills);
  assert.equal(machine.kodhama(["install", "demo"]).status, 0);

  const outcome = machine.kodhama(["remove", "demo", "--harness", "codex"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  assert.ok(outcome.stdout.includes(machine.claudeSkills), outcome.stdout);
  assert.deepEqual(readdirSync(machine.claudeSkills).sort(), ["alpha", "beta"]);
  assert.ok(!existsSync(join(machine.prev, "codex")));
  assert.deepEqual(/** @type {any} */ (readJson(machine.lock)).tools.demo.harnesses, ["claude"]);
  const checked = machine.kodhama(["check"]);
  assert.equal(checked.status, 0, checked.stderr);
});

test("a cross-filesystem remove sets the live folder aside in the stage, where recovery deletes it, never in the skills folder", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);
  assert.equal(machine.kodhama(["install", "demo"]).status, 0);
  // Every rename into prev/ fails as if prev/ were on another filesystem;
  // with KODHAMA_TEST_CRASH, the run dies as it deletes a folder set aside.
  const preload = join(machine.root, "exdev.mjs");
  writeFileSync(
    preload,
    `import fs from "node:fs";
import { syncBuiltinESMExports } from "node:module";
const { renameSync, rmSync, existsSync } = fs;
fs.renameSync = (from, to) => {
  if (String(to).startsWith(${JSON.stringify(machine.prev)})) {
    throw Object.assign(new Error("EXDEV: cross-device link not permitted"), { code: "EXDEV" });
  }
  return renameSync(from, to);
};
fs.rmSync = (path, options) => {
  if (process.env.KODHAMA_TEST_CRASH && String(path).endsWith(".moved") && existsSync(path)) process.exit(9);
  return rmSync(path, options);
};
syncBuiltinESMExports();
`,
  );
  const exdev = { NODE_OPTIONS: `--import=${pathToFileURL(preload).href}` };

  const copied = machine.kodhama(["remove", "demo", "--harness", "codex"], { env: exdev });

  assert.equal(copied.status, 0, copied.stderr);
  assert.deepEqual(readdirSync(machine.codexSkills), []);
  assert.ok(statSync(join(machine.prev, "codex", "alpha", "scripts", "run.sh")).mode & 0o100, "the exec bit survives the copy");
  assert.ok(!existsSync(join(machine.home, ".agents", ".kodhama-stage")));

  const crashed = machine.kodhama(["remove", "demo"], { env: { ...exdev, KODHAMA_TEST_CRASH: "1" } });

  assert.equal(crashed.status, 9, crashed.stderr);
  assert.deepEqual(readdirSync(machine.claudeSkills).filter((name) => name.endsWith(".moved")), []);
  const aside = join(machine.claude, ".kodhama-stage", "claude", "alpha.moved");
  assert.ok(existsSync(aside), "the folder set aside is in the stage");
  assert.equal(readFileSync(join(machine.prev, "claude", "alpha", "SKILL.md"), "utf8"), "---\nname: alpha\n---\nAlpha 0.1.0.\n");
  // The run died holding its lock; it is left to go stale.
  rmSync(join(machine.data, "kodhama", "run.lock"), { recursive: true });

  const recovered = machine.kodhama(["remove", "demo"]);

  assert.equal(recovered.status, 0, recovered.stderr);
  assert.ok(!existsSync(join(machine.claude, ".kodhama-stage")));
  assert.deepEqual(readdirSync(machine.claudeSkills), []);
  assert.ok(!existsSync(machine.lock));
});
