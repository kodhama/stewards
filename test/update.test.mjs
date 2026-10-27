// `update`: moving installed skills to another tag, two renames per skill,
// with the old copy kept in prev/, hand edits named, and a crashed run's
// stage folder recovered by the next run.

import assert from "node:assert/strict";
import { chmodSync, existsSync, lstatSync, mkdirSync, readFileSync, readdirSync, realpathSync, renameSync, symlinkSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { test } from "node:test";

import { readJson, scratch, sha256, writeFiles } from "./helpers/scratch.mjs";

/** @param {string} path */
const text = (path) => readFileSync(path, "utf8");

test("update swaps each skill to the new tag and keeps the old copy in prev/", (t) => {
  const machine = scratch(t);
  const tool = machine.fakeTool("demo", ["0.1.0", "0.2.0"]);
  assert.equal(machine.kodhama(["install", "demo#0.1.0"]).status, 0);

  const outcome = machine.kodhama(["update", "demo"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  assert.match(outcome.stdout, /v0\.1\.0 to v0\.2\.0/);
  for (const [harness, skills] of /** @type {const} */ ([["claude", machine.claudeSkills], ["codex", machine.codexSkills]])) {
    assert.deepEqual(readdirSync(skills).sort(), ["alpha", "beta"]);
    assert.match(text(join(skills, "alpha", "SKILL.md")), /Alpha 0\.2\.0/);
    assert.equal(/** @type {any} */ (readJson(join(skills, "alpha", ".kodhama-skill.json"))).tag, "v0.2.0");
    assert.match(text(join(machine.prev, harness, "alpha", "SKILL.md")), /Alpha 0\.1\.0/);
    assert.ok(!existsSync(join(skills, "..", ".kodhama-stage")), `${harness} stage left behind`);
  }
  const locked = /** @type {any} */ (readJson(machine.lock)).tools.demo;
  assert.equal(locked.tag, "v0.2.0");
  assert.equal(locked.commit, tool.commit("v0.2.0"));
});

test("update names each hand-edited file and the prev/ copy that now holds it", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0", "0.2.0"]);
  assert.equal(machine.kodhama(["install", "demo#0.1.0"]).status, 0);
  writeFileSync(join(machine.codexSkills, "alpha", "SKILL.md"), "my edit\n");

  const outcome = machine.kodhama(["update", "demo"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  const kept = join(machine.prev, "codex", "alpha");
  assert.ok(outcome.stdout.includes(`hand-edited ${join(machine.codexSkills, "alpha", "SKILL.md")}`), outcome.stdout);
  assert.ok(outcome.stdout.includes(kept), outcome.stdout);
  assert.equal(text(join(kept, "SKILL.md")), "my edit\n");
});

test("a skill the new tag drops moves to prev/ and leaves the lock", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0", "0.2.0"], { at: { "0.2.0": { "skills/beta/SKILL.md": null } } });
  assert.equal(machine.kodhama(["install", "demo#0.1.0"]).status, 0);

  const outcome = machine.kodhama(["update", "demo"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  assert.match(outcome.stdout, /beta/);
  for (const [harness, skills] of /** @type {const} */ ([["claude", machine.claudeSkills], ["codex", machine.codexSkills]])) {
    assert.deepEqual(readdirSync(skills), ["alpha"]);
    assert.ok(existsSync(join(machine.prev, harness, "beta", "SKILL.md")));
  }
  assert.deepEqual(Object.keys(/** @type {any} */ (readJson(machine.lock)).tools.demo.skills), ["alpha"]);
});

test("update at the newest tag writes nothing", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);
  assert.equal(machine.kodhama(["install", "demo"]).status, 0);
  const before = machine.state();

  const outcome = machine.kodhama(["update", "demo"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  assert.match(outcome.stdout, /already at v0\.1\.0/);
  assert.deepEqual(machine.state(), before);
});

test("an explicit older tag rolls the skills back", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0", "0.2.0"]);
  assert.equal(machine.kodhama(["install", "demo"]).status, 0);

  const outcome = machine.kodhama(["update", "demo#0.1.0"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  assert.match(text(join(machine.claudeSkills, "alpha", "SKILL.md")), /Alpha 0\.1\.0/);
  assert.equal(/** @type {any} */ (readJson(machine.lock)).tools.demo.tag, "v0.1.0");
});

test("a new skill whose name an unmarked folder holds refuses the update, and nothing is written", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0", "0.2.0"], { at: { "0.2.0": { "skills/gamma/SKILL.md": "Gamma.\n" } } });
  assert.equal(machine.kodhama(["install", "demo#0.1.0"]).status, 0);
  writeFiles(machine.codexSkills, { "gamma/SKILL.md": "my own gamma\n" });
  const before = machine.state();

  const outcome = machine.kodhama(["update", "demo"]);

  assert.equal(outcome.status, 1);
  assert.ok(outcome.stderr.includes(join(machine.codexSkills, "gamma")), outcome.stderr);
  assert.deepEqual(machine.state(), before);
});

test("update of a tool that is not installed refuses", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);

  const outcome = machine.kodhama(["update", "demo"]);

  assert.equal(outcome.status, 1);
  assert.match(outcome.stderr, /not installed/);
});

test("the next run recovers a crashed swap: a lone .old goes back into place, one beside a live copy goes to prev/", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);
  assert.equal(machine.kodhama(["install", "demo"]).status, 0);
  const codexStage = join(machine.home, ".agents", ".kodhama-stage");
  const claudeStage = join(machine.claude, ".kodhama-stage");
  mkdirSync(codexStage);
  renameSync(join(machine.codexSkills, "alpha"), join(codexStage, "alpha.old"));
  writeFiles(claudeStage, { "beta.old/SKILL.md": "an older beta\n", "beta/SKILL.md": "a half-built beta\n" });

  const outcome = machine.kodhama(["install", "demo"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  assert.match(outcome.stdout, /already installed/);
  assert.ok(existsSync(join(machine.codexSkills, "alpha", ".kodhama-skill.json")));
  assert.equal(text(join(machine.prev, "claude", "beta", "SKILL.md")), "an older beta\n");
  assert.match(text(join(machine.claudeSkills, "beta", "SKILL.md")), /Beta\./);
  assert.ok(!existsSync(codexStage));
  assert.ok(!existsSync(claudeStage));
  assert.equal(machine.kodhama(["check"]).status, 0);
});

test("two projects updated at project scope keep their old copies in separate prev/ slots", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0", "0.2.0"]);
  const repos = [machine.project("one"), machine.project("two")];

  for (const repo of repos) {
    assert.equal(machine.kodhama(["install", "demo#0.1.0", "--scope", "project"], { cwd: repo }).status, 0);
    writeFileSync(join(repo, ".agents", "skills", "beta", "SKILL.md"), `edited in ${repo}\n`);
    const outcome = machine.kodhama(["update", "demo", "--scope", "project"], { cwd: repo });
    assert.equal(outcome.status, 0, outcome.stderr);
  }

  const keys = repos.map((repo) => sha256(realpathSync(repo)).slice(0, 12));
  assert.notEqual(keys[0], keys[1]);
  assert.deepEqual(readdirSync(join(machine.prev, "projects")).sort(), [...keys].sort());
  repos.forEach((repo, at) => {
    assert.equal(text(join(machine.prev, "projects", keys[at], "codex", "beta", "SKILL.md")), `edited in ${repo}\n`);
  });
  assert.ok(!existsSync(join(machine.prev, "codex")), "project updates leave the user slots alone");
});

test("an update retried after it failed partway keeps the hand-edited copy in prev/", (t) => {
  if (process.getuid?.() === 0) {
    t.skip("root writes into the read-only folder this test fails the first run with");
    return;
  }
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0", "0.2.0"]);
  assert.equal(machine.kodhama(["install", "demo#0.1.0"]).status, 0);
  writeFileSync(join(machine.claudeSkills, "alpha", "SKILL.md"), "my edit\n");
  // Claude's skills swap first; Codex's stage cannot be made, so the run
  // stops with Claude at v0.2.0, Codex at v0.1.0 and the lock at v0.1.0.
  const agents = join(machine.home, ".agents");
  chmodSync(agents, 0o555);
  const failed = machine.kodhama(["update", "demo"]);
  chmodSync(agents, 0o755);
  assert.equal(failed.status, 1, failed.stdout);
  assert.match(text(join(machine.claudeSkills, "alpha", "SKILL.md")), /Alpha 0\.2\.0/);

  const retried = machine.kodhama(["update", "demo"]);

  assert.equal(retried.status, 0, retried.stderr);
  assert.equal(text(join(machine.prev, "claude", "alpha", "SKILL.md")), "my edit\n");
  assert.match(text(join(machine.codexSkills, "alpha", "SKILL.md")), /Alpha 0\.2\.0/);
  assert.equal(/** @type {any} */ (readJson(machine.lock)).tools.demo.tag, "v0.2.0");
  assert.equal(machine.kodhama(["check"]).status, 0);
});

test("a skills folder that is a symlink keeps its stage beside the real folder, where renames stay on one filesystem", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);
  const volume = join(machine.root, "volume");
  mkdirSync(join(volume, "skills"), { recursive: true });
  symlinkSync(join(volume, "skills"), machine.claudeSkills);
  assert.equal(machine.kodhama(["install", "demo"]).status, 0);
  assert.ok(lstatSync(machine.claudeSkills).isSymbolicLink());
  const stage = join(volume, ".kodhama-stage");
  mkdirSync(stage);
  renameSync(join(volume, "skills", "alpha"), join(stage, "alpha.old"));

  const outcome = machine.kodhama(["install", "demo"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  assert.ok(existsSync(join(volume, "skills", "alpha", ".kodhama-skill.json")));
  assert.ok(!existsSync(stage));
  assert.ok(!existsSync(join(machine.claude, ".kodhama-stage")));
});
