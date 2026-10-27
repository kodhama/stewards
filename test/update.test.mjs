// `update`: moving installed skills to another tag, two renames per skill,
// with the old copy kept in prev/, hand edits named, and a crashed run's
// stage folder recovered by the next run.

import assert from "node:assert/strict";
import { chmodSync, existsSync, lstatSync, mkdirSync, readFileSync, readdirSync, realpathSync, renameSync, symlinkSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
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
  const codexStage = join(machine.home, ".agents", ".kodhama-stage", "codex");
  const claudeStage = join(machine.claude, ".kodhama-stage", "claude");
  mkdirSync(codexStage, { recursive: true });
  renameSync(join(machine.codexSkills, "alpha"), join(codexStage, "alpha.old"));
  writeFiles(claudeStage, { "beta.old/SKILL.md": "an older beta\n", "beta/SKILL.md": "a half-built beta\n" });

  const outcome = machine.kodhama(["install", "demo"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  assert.match(outcome.stdout, /already installed/);
  assert.ok(existsSync(join(machine.codexSkills, "alpha", ".kodhama-skill.json")));
  assert.equal(text(join(machine.prev, "claude", "beta", "SKILL.md")), "an older beta\n");
  assert.match(text(join(machine.claudeSkills, "beta", "SKILL.md")), /Beta\./);
  assert.ok(!existsSync(dirname(codexStage)));
  assert.ok(!existsSync(dirname(claudeStage)));
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
  const stage = join(volume, ".kodhama-stage", "claude");
  mkdirSync(stage, { recursive: true });
  renameSync(join(volume, "skills", "alpha"), join(stage, "alpha.old"));

  const outcome = machine.kodhama(["install", "demo"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  assert.ok(existsSync(join(volume, "skills", "alpha", ".kodhama-skill.json")));
  assert.ok(!existsSync(stage));
  assert.ok(!existsSync(join(machine.claude, ".kodhama-stage")));
});

test("update with no tag never moves down from a pre-release newer than the newest stable tag", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.10.0", "0.11.0-rc.1"]);
  assert.equal(machine.kodhama(["install", "demo#v0.11.0-rc.1"]).status, 0);
  const before = machine.state();

  const outcome = machine.kodhama(["update", "demo"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  assert.match(outcome.stdout, /stays at v0\.11\.0-rc\.1.*newer than v0\.10\.0/);
  assert.deepEqual(machine.state(), before);
});

test("two harnesses' skills folders in one parent keep separate stages, and a Claude run leaves Codex's alone", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);
  const shared = join(machine.root, "shared");
  mkdirSync(join(shared, "claude-skills"), { recursive: true });
  mkdirSync(join(shared, "codex-skills"));
  mkdirSync(join(machine.home, ".agents"));
  symlinkSync(join(shared, "claude-skills"), machine.claudeSkills);
  symlinkSync(join(shared, "codex-skills"), machine.codexSkills);
  assert.equal(machine.kodhama(["install", "demo", "--harness", "codex"]).status, 0);
  const planted = join(shared, ".kodhama-stage", "codex", "alpha.old");
  writeFiles(planted, { "SKILL.md": "codex's interrupted copy\n" });

  const outcome = machine.kodhama(["install", "demo", "--harness", "claude"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  assert.equal(text(join(planted, "SKILL.md")), "codex's interrupted copy\n");
  assert.deepEqual(readdirSync(join(shared, "claude-skills")).sort(), ["alpha", "beta"]);
});

test("a stage folder that is a symlink is refused, and what it points at is untouched", (t) => {
  for (const link of [".kodhama-stage", join(".kodhama-stage", "claude")]) {
    const machine = scratch(t);
    machine.fakeTool("demo", ["0.1.0"]);
    const victim = join(machine.root, "victim");
    writeFiles(victim, { "precious.txt": "keep me\n", "alpha.old/SKILL.md": "not a stage\n" });
    mkdirSync(dirname(join(machine.claude, link)), { recursive: true });
    symlinkSync(victim, join(machine.claude, link));
    const before = machine.state();

    const outcome = machine.kodhama(["install", "demo"]);

    assert.equal(outcome.status, 1, link);
    assert.match(outcome.stderr, /not a real folder/, link);
    assert.deepEqual(machine.state(), before, link);
  }
});

test("a .moved leftover from a cross-filesystem move is deleted, and the prev/ copy it came from stays", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);
  assert.equal(machine.kodhama(["install", "demo"]).status, 0);
  writeFiles(join(machine.prev, "claude", "alpha"), { "SKILL.md": "the full previous copy\n" });
  const leftover = join(machine.claude, ".kodhama-stage", "claude", "alpha.old.moved");
  writeFiles(leftover, { "SKILL.md": "half deleted\n" });

  const outcome = machine.kodhama(["install", "demo"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  assert.ok(!existsSync(leftover));
  assert.equal(text(join(machine.prev, "claude", "alpha", "SKILL.md")), "the full previous copy\n");
});

test("update fetches from the source install would use, and refuses a lock that names another", (t) => {
  const machine = scratch(t);
  const tool = machine.fakeTool("demo", ["0.1.0"]);
  const repo = machine.project("work");
  assert.equal(machine.kodhama(["install", "demo", "--scope", "project"], { cwd: repo }).status, 0);
  // Another repo, with a newer tag carrying a skill the real demo never had.
  const other = join(machine.root, "other", "demo");
  machine.git(machine.root, ["clone", "-q", tool.path, other]);
  writeFiles(other, { "skills/planted/SKILL.md": "Not demo's.\n" });
  machine.git(other, ["add", "-A"]);
  machine.git(other, ["commit", "-q", "-m", "planted"]);
  machine.git(other, ["tag", "-a", "v0.2.0", "-m", "planted"]);
  const lockPath = join(repo, ".kodhama", "cli", "lock.json");
  const lock = /** @type {any} */ (readJson(lockPath));
  lock.tools.demo.source = `file://${other}`;
  writeFileSync(lockPath, `${JSON.stringify(lock, null, 2)}\n`);
  const before = machine.state();

  const outcome = machine.kodhama(["update", "demo", "--scope", "project"], { cwd: repo });

  assert.equal(outcome.status, 1);
  assert.ok(outcome.stderr.includes(`file://${other}`), outcome.stderr);
  assert.ok(outcome.stderr.includes(`file://${tool.path}`), outcome.stderr);
  assert.ok(!existsSync(join(repo, ".claude", "skills", "planted")));
  assert.deepEqual(machine.state(), before);
});

/**
 * Effect: installs demo at v1.1.0, hand-edits Claude's alpha and beta, and
 * runs an update to v1.2.0 that fails partway: Claude's skills swap, so the
 * hand-edited copies are now only in prev/, and Codex's stage cannot be
 * made. Returns the machine, the failed run, and the prev/ copies.
 * @param {import("node:test").TestContext} t
 */
const interruptedUpdate = (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["1.1.0", "1.2.0", "1.3.0"]);
  assert.equal(machine.kodhama(["install", "demo#1.1.0"]).status, 0);
  writeFileSync(join(machine.claudeSkills, "alpha", "SKILL.md"), "alpha edit\n");
  writeFileSync(join(machine.claudeSkills, "beta", "SKILL.md"), "beta edit\n");
  const agents = join(machine.home, ".agents");
  chmodSync(agents, 0o555);
  const failed = machine.kodhama(["update", "demo#1.2.0"]);
  chmodSync(agents, 0o755);
  assert.equal(failed.status, 1, failed.stdout);
  assert.match(text(join(machine.claudeSkills, "alpha", "SKILL.md")), /Alpha 1\.2\.0/);
  const kept = { alpha: join(machine.prev, "claude", "alpha"), beta: join(machine.prev, "claude", "beta") };
  /** Asserts both hand-edited copies are still in prev/. */
  const editsSurvive = (/** @type {string} */ after) => {
    assert.equal(text(join(kept.alpha, "SKILL.md")), "alpha edit\n", after);
    assert.equal(text(join(kept.beta, "SKILL.md")), "beta edit\n", after);
  };
  editsSurvive("the failed update");
  return { machine, failed, kept, editsSurvive };
};

test("an update that fails partway names the prev/ copies that now hold the hand edits", (t) => {
  if (process.getuid?.() === 0) {
    t.skip("root writes into the read-only folder this test fails the first run with");
    return;
  }
  const { machine, failed, kept } = interruptedUpdate(t);

  for (const skill of /** @type {const} */ (["alpha", "beta"])) {
    const line = `hand-edited ${join(machine.claudeSkills, skill, "SKILL.md")}; the copy with it is in ${kept[skill]}.`;
    assert.ok(failed.stderr.includes(line), failed.stderr);
  }
  assert.ok(failed.stderr.includes("kodhama update demo#v1.2.0"), failed.stderr);
});

test("after an update fails partway, remove refuses and the hand-edited prev/ copies survive", (t) => {
  if (process.getuid?.() === 0) {
    t.skip("root writes into the read-only folder this test fails the first run with");
    return;
  }
  const { machine, kept, editsSurvive } = interruptedUpdate(t);
  const before = machine.state();

  const outcome = machine.kodhama(["remove", "demo"]);

  assert.equal(outcome.status, 1, outcome.stdout);
  assert.ok(outcome.stderr.includes("kodhama update demo#v1.2.0"), outcome.stderr);
  assert.ok(outcome.stderr.includes(kept.alpha), outcome.stderr);
  editsSurvive("remove");
  assert.deepEqual(machine.state(), before);
});

test("after an update fails partway, an update to another tag refuses, and finishing the interrupted one keeps the edits", (t) => {
  if (process.getuid?.() === 0) {
    t.skip("root writes into the read-only folder this test fails the first run with");
    return;
  }
  const { machine, editsSurvive } = interruptedUpdate(t);
  const before = machine.state();

  for (const args of [["update", "demo"], ["update", "demo#1.1.0"]]) {
    const outcome = machine.kodhama(args);
    assert.equal(outcome.status, 1, `${args.join(" ")}: ${outcome.stdout}`);
    assert.ok(outcome.stderr.includes("kodhama update demo#v1.2.0"), outcome.stderr);
    editsSurvive(args.join(" "));
    assert.deepEqual(machine.state(), before, args.join(" "));
  }

  const finished = machine.kodhama(["update", "demo#1.2.0"]);

  assert.equal(finished.status, 0, finished.stderr);
  editsSurvive("the finished update");
  assert.equal(machine.kodhama(["check"]).status, 0);
});

test("after an update fails partway, install does not recommend remove", (t) => {
  if (process.getuid?.() === 0) {
    t.skip("root writes into the read-only folder this test fails the first run with");
    return;
  }
  const { machine, editsSurvive } = interruptedUpdate(t);

  const outcome = machine.kodhama(["install", "demo"]);

  assert.equal(outcome.status, 1, outcome.stdout);
  assert.ok(!outcome.stderr.includes("kodhama remove"), outcome.stderr);
  assert.ok(outcome.stderr.includes("kodhama update demo#v1.2.0"), outcome.stderr);
  editsSurvive("install");
});

test("with one skills folder shared by both harnesses, update names the prev/ slot it actually wrote", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0", "0.2.0"]);
  mkdirSync(join(machine.home, ".agents"));
  mkdirSync(machine.claudeSkills);
  symlinkSync(machine.claudeSkills, machine.codexSkills);
  assert.equal(machine.kodhama(["install", "demo#0.1.0"]).status, 0);
  writeFileSync(join(machine.claudeSkills, "alpha", "SKILL.md"), "my edit\n");

  const outcome = machine.kodhama(["update", "demo"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  const kept = join(machine.prev, "claude", "alpha");
  assert.equal(text(join(kept, "SKILL.md")), "my edit\n");
  assert.ok(outcome.stdout.includes(`the copy with it is in ${kept}.`), outcome.stdout);
  assert.ok(!outcome.stdout.includes(join(machine.prev, "codex")), outcome.stdout);
  assert.equal(outcome.stdout.match(/hand-edited/g)?.length, 1, outcome.stdout);
});

test("with one skills folder shared through a symlink, install --harness codex after a Claude update failed partway refuses, and the hand edit survives", (t) => {
  if (process.getuid?.() === 0) {
    t.skip("root writes into the read-only folder this test fails the first run with");
    return;
  }
  const machine = scratch(t);
  machine.fakeTool("demo", ["1.1.0", "1.2.0"]);
  mkdirSync(join(machine.home, ".agents"));
  mkdirSync(machine.claudeSkills);
  symlinkSync(machine.claudeSkills, machine.codexSkills);
  assert.equal(machine.kodhama(["install", "demo#1.1.0", "--harness", "claude"]).status, 0);
  writeFileSync(join(machine.claudeSkills, "alpha", "SKILL.md"), "alpha edit\n");
  // The update swaps alpha, then stops at beta: its prev/ slot cannot be cleared.
  const blocker = join(machine.prev, "claude", "beta", "ro");
  mkdirSync(blocker, { recursive: true });
  writeFileSync(join(blocker, "f"), "x\n");
  chmodSync(blocker, 0o555);
  const failed = machine.kodhama(["update", "demo#1.2.0"]);
  chmodSync(blocker, 0o755);
  assert.equal(failed.status, 1, failed.stdout);
  const kept = join(machine.prev, "claude", "alpha", "SKILL.md");
  assert.equal(text(kept), "alpha edit\n");
  const before = machine.state();

  const outcome = machine.kodhama(["install", "demo", "--harness", "codex"]);

  assert.equal(outcome.status, 1, outcome.stdout);
  assert.ok(outcome.stderr.includes("kodhama update demo#v1.2.0"), outcome.stderr);
  assert.match(text(join(machine.claudeSkills, "alpha", "SKILL.md")), /Alpha 1\.2\.0/);
  assert.equal(text(kept), "alpha edit\n");
  assert.deepEqual(machine.state(), before);
});

test("after an update fails partway and its tag then moves, update prints the way out by hand, which works and keeps the edits", (t) => {
  if (process.getuid?.() === 0) {
    t.skip("root writes into the read-only folder this test fails the first run with");
    return;
  }
  const { machine, kept } = interruptedUpdate(t);
  const source = join(machine.source, "demo");
  writeFileSync(join(source, "VERSION"), "retagged\n");
  machine.git(source, ["commit", "-q", "-am", "retag"]);
  machine.git(source, ["tag", "-f", "-a", "v1.2.0", "-m", "retag"]);

  const outcome = machine.kodhama(["update", "demo#1.2.0"]);

  assert.equal(outcome.status, 1, outcome.stdout);
  assert.ok(!outcome.stderr.includes("kodhama update demo#v1.2.0"), outcome.stderr);
  for (const step of [
    "Copy each prev/ folder named above somewhere safe.",
    "Move each live folder named above out of its skills folder.",
    "kodhama remove demo, then kodhama install demo",
    "KOD-25",
  ]) {
    assert.ok(outcome.stderr.includes(step), outcome.stderr);
  }
  for (const skill of /** @type {const} */ (["alpha", "beta"])) {
    assert.ok(outcome.stderr.includes(kept[skill]), outcome.stderr);
    assert.ok(outcome.stderr.includes(join(machine.claudeSkills, skill)), outcome.stderr);
  }

  // The steps, as printed.
  const safe = join(machine.root, "safe");
  mkdirSync(safe);
  const aside = join(machine.root, "aside");
  mkdirSync(aside);
  for (const skill of /** @type {const} */ (["alpha", "beta"])) {
    writeFileSync(join(safe, `${skill}.md`), text(join(kept[skill], "SKILL.md")));
    renameSync(join(machine.claudeSkills, skill), join(aside, skill));
  }
  const removed = machine.kodhama(["remove", "demo"]);
  assert.equal(removed.status, 0, removed.stderr);
  const installed = machine.kodhama(["install", "demo"]);
  assert.equal(installed.status, 0, installed.stderr);
  assert.equal(text(join(safe, "alpha.md")), "alpha edit\n");
  assert.equal(text(join(safe, "beta.md")), "beta edit\n");
  assert.equal(machine.kodhama(["check"]).status, 0);
});

test("every move into an occupied prev/ slot warns what the slot held: update, remove, install and recovery", (t) => {
  const machine = scratch(t);
  const tool = machine.fakeTool("demo", ["0.1.0", "0.2.0", "0.3.0"]);
  const slot = join(machine.prev, "claude", "alpha");
  const held = (/** @type {string} */ tag) => `${slot} held demo ${tag} (${tool.commit(tag)}), which this run replaced.`;
  assert.equal(machine.kodhama(["install", "demo#0.1.0", "--harness", "claude"]).status, 0);
  const first = machine.kodhama(["update", "demo#0.2.0"]);
  assert.equal(first.status, 0, first.stderr);
  assert.ok(!first.stdout.includes("which this run replaced"), first.stdout);

  const updated = machine.kodhama(["update", "demo#0.3.0"]);
  assert.equal(updated.status, 0, updated.stderr);
  assert.ok(updated.stdout.includes(held("v0.1.0")), updated.stdout);

  const removed = machine.kodhama(["remove", "demo"]);
  assert.equal(removed.status, 0, removed.stderr);
  assert.ok(removed.stdout.includes(held("v0.2.0")), removed.stdout);

  // install over marked folders the lock no longer knows moves them to prev/.
  assert.equal(machine.kodhama(["install", "demo#0.1.0", "--harness", "claude"]).status, 0);
  writeFiles(machine.data, { "kodhama/lock.json": null });
  const installed = machine.kodhama(["install", "demo#0.2.0", "--harness", "claude"]);
  assert.equal(installed.status, 0, installed.stderr);
  assert.ok(installed.stdout.includes(held("v0.3.0")), installed.stdout);

  // A crashed run's .old beside a live copy goes to prev/ too; this slot
  // holds a folder with no marker.
  writeFiles(join(machine.claude, ".kodhama-stage", "claude"), { "beta.old/SKILL.md": "an older beta\n" });
  writeFiles(join(machine.prev, "claude", "beta"), { ".kodhama-skill.json": null, "SKILL.md": "something\n" });
  const recovered = machine.kodhama(["install", "demo#0.2.0", "--harness", "claude"]);
  assert.equal(recovered.status, 0, recovered.stderr);
  assert.ok(
    recovered.stdout.includes(`${join(machine.prev, "claude", "beta")} held a copy with no kodhama marker it can read, which this run replaced.`),
    recovered.stdout,
  );
});

test("with one skills folder shared by both harnesses, the interrupted-update refusal names only the prev/ slots written", (t) => {
  if (process.getuid?.() === 0) {
    t.skip("root writes into the read-only folder this test fails the first run with");
    return;
  }
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0", "0.2.0"]);
  mkdirSync(join(machine.home, ".agents"));
  mkdirSync(machine.claudeSkills);
  symlinkSync(machine.claudeSkills, machine.codexSkills);
  assert.equal(machine.kodhama(["install", "demo#0.1.0"]).status, 0);
  writeFileSync(join(machine.claudeSkills, "alpha", "SKILL.md"), "alpha edit\n");
  const blocker = join(machine.prev, "claude", "beta", "ro");
  mkdirSync(blocker, { recursive: true });
  writeFileSync(join(blocker, "f"), "x\n");
  chmodSync(blocker, 0o555);
  const failed = machine.kodhama(["update", "demo"]);
  chmodSync(blocker, 0o755);
  assert.equal(failed.status, 1, failed.stdout);

  for (const args of [["remove", "demo"], ["remove", "demo", "--harness", "codex"]]) {
    const outcome = machine.kodhama(args);

    assert.equal(outcome.status, 1, outcome.stdout);
    assert.ok(outcome.stderr.includes(join(machine.prev, "claude", "alpha")), `${args.join(" ")}: ${outcome.stderr}`);
    assert.ok(!outcome.stderr.includes(join(machine.prev, "codex")), `${args.join(" ")}: ${outcome.stderr}`);
    assert.equal(text(join(machine.prev, "claude", "alpha", "SKILL.md")), "alpha edit\n");
  }
});
