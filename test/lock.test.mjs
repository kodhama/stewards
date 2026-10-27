// The lock is read back only when kodhama could have written it: a source
// git could read as an option, or a tool, skill or file name that would step
// out of its folder, makes the whole lock unreadable, so no verb acts on it.

import assert from "node:assert/strict";
import { existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { test } from "node:test";

import { withTool } from "../src/fetch.mjs";
import { scratch, writeFiles } from "./helpers/scratch.mjs";

/**
 * A lock entry kodhama could have written, with `change` laid over it.
 * @param {Record<string, unknown>} change
 */
const entry = (change) => ({
  tag: "v0.1.0",
  commit: "0".repeat(40),
  source: "https://github.com/kodhama/demo.git",
  harnesses: ["claude", "codex"],
  skills: { alpha: { "SKILL.md": { sha256: "0".repeat(64), exec: false } } },
  ...change,
});

test("a lock whose source git could read as an option is refused, and git never runs it", (t) => {
  const machine = scratch(t);
  const repo = machine.project("work");
  const pwned = join(machine.root, "pwned");
  writeFiles(repo, {
    ".kodhama/cli/lock.json": `${JSON.stringify({ lock: 1, tools: { demo: entry({ source: `--upload-pack=touch ${pwned}` }) } })}\n`,
  });
  const before = machine.state();

  for (const verb of ["update", "remove"]) {
    const outcome = machine.kodhama([verb, "demo", "--scope", "project"], { cwd: repo });
    assert.equal(outcome.status, 1, verb);
    assert.match(outcome.stderr, /not a lock this kodhama can read/, verb);
  }
  assert.ok(!existsSync(pwned));
  assert.deepEqual(machine.state(), before);
});

test("fetch takes only an https:// or file:// source", (t) => {
  const machine = scratch(t);
  const pwned = join(machine.root, "pwned");

  const fetched = withTool("demo", undefined, { env: machine.env, tmp: machine.tmp, source: `--upload-pack=touch ${pwned}` }, () => "ran");

  assert.ok("error" in fetched);
  assert.match(fetched.error, /https:\/\/ or file:\/\//);
  assert.ok(!existsSync(pwned));
});

test("a lock with a tool, skill or file name that leaves its folder is refused, and nothing moves", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0", "0.2.0"]);
  // Something for each escape to reach, should it get through.
  mkdirSync(join(machine.claude, "x"));
  writeFiles(machine.claude, { "x/SKILL.md": "not a skill of demo's\n" });

  for (const tools of [
    { demo: entry({ skills: { "../x": { "SKILL.md": { sha256: "0".repeat(64), exec: false } } } }) },
    { "../demo": entry({}) },
    { demo: entry({ skills: { alpha: { "../../x/SKILL.md": { sha256: "0".repeat(64), exec: false } } } }) },
    { demo: entry({ skills: { alpha: { "/etc/passwd": { sha256: "0".repeat(64), exec: false } } } }) },
    { demo: entry({ skills: { alpha: { "a\\..\\b": { sha256: "0".repeat(64), exec: false } } } }) },
  ]) {
    writeFiles(machine.data, { "kodhama/lock.json": `${JSON.stringify({ lock: 1, tools })}\n` });
    const before = machine.state();
    for (const verb of ["remove", "update"]) {
      const outcome = machine.kodhama([verb, "demo"]);
      assert.equal(outcome.status, 1, `${verb} ${JSON.stringify(tools)}`);
      assert.match(outcome.stderr, /not a lock this kodhama can read/, verb);
    }
    assert.deepEqual(machine.state(), before, JSON.stringify(tools));
  }
});
