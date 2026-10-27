// The lock is read back only when kodhama could have written it: a source
// git could read as an option, or a tool, skill or file name that would step
// out of its folder, makes the whole lock unreadable, so no verb acts on it.

import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { chmodSync, existsSync, mkdirSync, readFileSync, statSync, utimesSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { test } from "node:test";

import { withTool } from "../src/fetch.mjs";
import { keepAlive } from "../src/lock.mjs";
import { withRunLock } from "../src/targets.mjs";
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

test("a run lock whose token is no longer ours survives our release", (t) => {
  const machine = scratch(t);
  const path = join(machine.data, "kodhama", "run.lock");

  withRunLock(path, () => writeFileSync(join(path, "owner"), "another run\n"));

  assert.ok(existsSync(join(path, "owner")));
});

test("a held run lock is refreshed before each phase, so a long run never looks stale", (t) => {
  const machine = scratch(t);
  const path = join(machine.data, "kodhama", "run.lock");
  const old = new Date(Date.now() - 60 * 60 * 1000);

  const refreshed = withRunLock(path, () => {
    utimesSync(path, old, old);
    keepAlive();
    return statSync(path).mtimeMs;
  });

  assert.ok(Date.now() - /** @type {number} */ (refreshed) < 60 * 1000);
  assert.ok(!existsSync(path));
});

/**
 * Effect: a folder holding a `git` that, for each step whose name is among
 * its arguments, first runs that step's shell hook, then the real git.
 * Returns the PATH that puts it first.
 * @param {ReturnType<typeof scratch>} machine
 * @param {Readonly<Record<string, string>>} hooks
 */
const gitWith = (machine, hooks) => {
  const real = execFileSync("sh", ["-c", "command -v git"], { encoding: "utf8" }).trim();
  const dir = join(machine.root, "hooked-git");
  const cases = Object.entries(hooks).map(([step, hook]) => `case " $* " in *" ${step} "*) ${hook} ;; esac\n`);
  writeFiles(dir, { git: `#!/bin/sh\n${cases.join("")}exec "${real}" "$@"\n` });
  chmodSync(join(dir, "git"), 0o755);
  return { PATH: `${dir}:${machine.env.PATH}` };
};

test("the run lock is refreshed between the fetch's git calls, so a slow fetch never looks stale", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);
  const held = join(machine.data, "kodhama", "run.lock");
  const recent = join(machine.root, "ten-minutes-ago");
  writeFileSync(recent, "");
  const then = new Date(Date.now() - 10 * 60 * 1000);
  utimesSync(recent, then, then);
  const seen = join(machine.root, "seen");
  // fetch ages the lock past stale; checkout, the next git call, records
  // whether it was refreshed in between.
  const path = gitWith(machine, {
    fetch: `touch -t 200001010000 "${held}"`,
    checkout: `if [ "${held}" -nt "${recent}" ]; then echo fresh > "${seen}"; else echo stale > "${seen}"; fi`,
  });

  const outcome = machine.kodhama(["install", "demo"], { env: path });

  assert.equal(outcome.status, 0, outcome.stderr);
  assert.equal(readFileSync(seen, "utf8"), "fresh\n");
});

test("a run whose lock another run took over during the fetch stops before it swaps or writes the lock", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);
  const held = join(machine.data, "kodhama", "run.lock");
  // The last git call of the fetch: the lock now names another run.
  const path = gitWith(machine, { "rev-parse": `printf 'another run\\n' > "${held}/owner"` });

  const outcome = machine.kodhama(["install", "demo"], { env: path });

  assert.equal(outcome.status, 1, outcome.stdout);
  assert.match(outcome.stderr, /took over/);
  assert.ok(outcome.stderr.includes(held), outcome.stderr);
  assert.ok(!existsSync(machine.claudeSkills));
  assert.ok(!existsSync(machine.codexSkills));
  assert.ok(!existsSync(machine.lock));
  assert.equal(readFileSync(join(held, "owner"), "utf8"), "another run\n");
});
