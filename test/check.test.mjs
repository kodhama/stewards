// `check`: comparing installed skills with the lock, offline and without
// writing, one line per problem.

import assert from "node:assert/strict";
import { chmodSync, mkdirSync, rmSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { test } from "node:test";

import { scratch } from "./helpers/scratch.mjs";

test("check with nothing installed says so and passes", (t) => {
  const machine = scratch(t);

  const outcome = machine.kodhama(["check"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  assert.match(outcome.stdout, /nothing installed/);
});

test("check passes on a clean install with no network and no git", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);
  assert.equal(machine.kodhama(["install", "demo"]).status, 0);
  const empty = join(machine.root, "empty");
  mkdirSync(empty);

  // No tool repo to reach, and no git on the PATH to reach it with.
  const outcome = machine.kodhama(["check", "demo"], { env: { KODHAMA_TOOL_SOURCE: empty, PATH: "" } });

  assert.equal(outcome.status, 0, outcome.stderr);
  assert.match(outcome.stdout, /demo v0\.1\.0 is intact/);
});

test("check names each problem on its own line and writes nothing", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"], { files: { "skills/gamma/SKILL.md": "Gamma.\n", "skills/delta/SKILL.md": "Delta.\n", "skills/delta/notes.md": "notes\n" } });
  assert.equal(machine.kodhama(["install", "demo"]).status, 0);
  const claude = machine.claudeSkills;
  const codex = machine.codexSkills;
  writeFileSync(join(claude, "alpha", "SKILL.md"), "hand edit\n");
  rmSync(join(codex, "beta"), { recursive: true });
  rmSync(join(claude, "beta", ".kodhama-skill.json"));
  writeFileSync(join(codex, "alpha", "extra.md"), "added\n");
  chmodSync(join(codex, "gamma", "SKILL.md"), 0o755);
  rmSync(join(claude, "delta", "notes.md"));
  writeFileSync(join(codex, "delta", ".kodhama-skill.json"), `${JSON.stringify({ tool: "demo", skill: "delta", tag: "v9.9.9", commit: "0" })}\n`);
  const before = machine.state();

  const outcome = machine.kodhama(["check"]);

  assert.equal(outcome.status, 1);
  const lines = outcome.stderr.trim().split("\n").sort();
  assert.deepEqual(lines, [
    `added ${join(codex, "alpha", "extra.md")}`,
    `deleted ${join(claude, "delta", "notes.md")}`,
    `exec changed ${join(codex, "gamma", "SKILL.md")}`,
    `hand-edited ${join(claude, "alpha", "SKILL.md")}`,
    `marker differs ${join(codex, "delta")}`,
    `missing ${join(codex, "beta")}`,
    `unmarked ${join(claude, "beta")}`,
  ]);
  assert.deepEqual(machine.state(), before);
});

test("check of a tool that is not installed fails", (t) => {
  const machine = scratch(t);

  const outcome = machine.kodhama(["check", "demo"]);

  assert.equal(outcome.status, 1);
  assert.match(outcome.stderr, /demo is not installed/);
});
