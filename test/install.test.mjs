// The command line and `install`: reading the arguments, and the program run
// for real with no terminal on a scratch machine whose tool repos stand in
// for GitHub.

import assert from "node:assert/strict";
import { sep } from "node:path";
import { test } from "node:test";

import { parseArgs } from "../src/cli.mjs";
import { scratch } from "./helpers/scratch.mjs";

test("the scratch machine keeps every path it hands the program under its root", (t) => {
  const machine = scratch(t);

  for (const name of [
    "HOME",
    "XDG_DATA_HOME",
    "CODEX_HOME",
    "CLAUDE_CONFIG_DIR",
    "KODHAMA_TOOL_SOURCE",
    "TMPDIR",
  ]) {
    assert.ok(machine.env[name].startsWith(machine.root + sep), name);
  }
  assert.deepEqual(machine.written(), ["claude", "codex", "data", "home", "tmp"]);
});

test("install reads a tool, a tag, a scope, harnesses and --migrate", () => {
  assert.deepEqual(parseArgs(["install", "grove#0.3.0", "--harness", "codex"]), {
    command: "install",
    tool: "grove",
    tag: "v0.3.0",
    scope: "user",
    harnesses: ["codex"],
    migrate: false,
  });
  assert.deepEqual(
    parseArgs([
      "install",
      "--scope=project",
      "demo#v1.2.3-rc.1",
      "--harness",
      "codex",
      "--harness=claude",
      "--migrate",
    ]),
    {
      command: "install",
      tool: "demo",
      tag: "v1.2.3-rc.1",
      scope: "project",
      harnesses: ["claude", "codex"],
      migrate: true,
    },
  );
  assert.deepEqual(parseArgs(["install", "demo"]), {
    command: "install",
    tool: "demo",
    tag: undefined,
    scope: "user",
    harnesses: ["claude", "codex"],
    migrate: false,
  });
});

test("update, check and remove take what the verb table gives them", () => {
  assert.deepEqual(parseArgs(["update", "demo#0.2.0", "--scope", "project"]), {
    command: "update",
    tool: "demo",
    tag: "v0.2.0",
    scope: "project",
    harnesses: ["claude", "codex"],
    migrate: false,
  });
  assert.deepEqual(parseArgs(["check"]), {
    command: "check",
    tool: undefined,
    tag: undefined,
    scope: "user",
    harnesses: ["claude", "codex"],
    migrate: false,
  });
  assert.deepEqual(parseArgs(["check", "demo"]).tool, "demo");
  assert.deepEqual(parseArgs(["remove", "demo", "--harness", "codex"]), {
    command: "remove",
    tool: "demo",
    tag: undefined,
    scope: "user",
    harnesses: ["codex"],
    migrate: false,
  });
});

test("a command line the verb table does not allow is an error", () => {
  for (const args of [
    [],
    ["adopt"],
    ["uninstall", "demo"],
    ["install"],
    ["install", "demo", "extra"],
    ["install", "demo", "--force"],
    ["install", "demo", "--scope"],
    ["install", "demo", "--scope", "team"],
    ["install", "demo", "--scope", "user", "--scope", "project"],
    ["install", "demo", "--harness", "cursor"],
    ["install", "Demo"],
    ["install", "demo#"],
    ["install", "demo#-x"],
    ["install", "../demo"],
    ["update", "demo", "--harness", "codex"],
    ["update", "demo", "--migrate"],
    ["check", "demo#v1.0.0"],
    ["check", "--harness", "codex"],
    ["remove"],
    ["remove", "grove#v1.0.0"],
    ["remove", "demo", "--migrate"],
  ]) {
    assert.ok("error" in parseArgs(args), JSON.stringify(args));
  }
});

test("a usage error prints the usage and exits 2, for each way of making one", (t) => {
  const machine = scratch(t);

  for (const args of [
    [],
    ["adopt"],
    ["uninstall", "grove"],
    ["install", "grove", "--force"],
    ["install", "grove", "--scope", "team"],
    ["remove", "grove#v1.0.0"],
  ]) {
    const outcome = machine.kodhama(args);
    assert.equal(outcome.status, 2, JSON.stringify(args));
    assert.match(outcome.stderr, /Usage: kodhama <command>/, JSON.stringify(args));
    assert.equal(outcome.stdout, "");
  }
  assert.match(machine.kodhama(["uninstall", "grove"]).stderr, /use remove/);
  assert.deepEqual(machine.written(), ["claude", "codex", "data", "home", "tmp"]);
});

test("a verb not built yet says so and exits 1, writing nothing", (t) => {
  const machine = scratch(t);

  for (const args of [["update", "demo"], ["check"], ["remove", "demo"]]) {
    const outcome = machine.kodhama(args);
    assert.equal(outcome.status, 1, JSON.stringify(args));
    assert.match(outcome.stderr, /not built yet/, JSON.stringify(args));
  }
  assert.deepEqual(machine.written(), ["claude", "codex", "data", "home", "tmp"]);
});
