// The command line and `install`: reading the arguments, and the program run
// for real with no terminal on a scratch machine whose tool repos stand in
// for GitHub.

import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, readdirSync, statSync, writeFileSync } from "node:fs";
import { join, sep } from "node:path";
import { test } from "node:test";

import { parseArgs } from "../src/cli.mjs";
import {
  copyFiles,
  listFiles,
  pickTag,
  toolSource,
  withTool,
} from "../src/fetch.mjs";
import { MARKER, parseManifest } from "../src/manifest.mjs";
import { readJson, scratch, sha256, writeFiles } from "./helpers/scratch.mjs";

// What a scratch machine holds before the program runs: its empty folders.
const UNTOUCHED = ["claude", "codex", "data", "home", "tmp"];

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
  assert.deepEqual(machine.written(), UNTOUCHED);
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
  assert.deepEqual(machine.written(), UNTOUCHED);
});

test("with no tag named, the highest stable vX.Y.Z wins, in numeric order", () => {
  const tags = ["v0.1.0", "v0.9.0", "v0.10.0", "v0.11.0-rc.1", "latest", "v1.0", "v01.0.0"];

  assert.equal(pickTag(tags, undefined), "v0.10.0");
  assert.equal(pickTag(tags, "v0.1.0"), "v0.1.0");
  assert.equal(pickTag(tags, "v0.11.0-rc.1"), "v0.11.0-rc.1");
  assert.equal(pickTag(tags, "latest"), "latest");
  assert.equal(pickTag(tags, "v9.9.9"), undefined);
  assert.equal(pickTag([], undefined), undefined);
  assert.equal(pickTag(["latest", "v2.0.0-beta.1"], undefined), undefined);
});

test("a tool comes from GitHub, or from KODHAMA_TOOL_SOURCE when it is set", () => {
  assert.equal(toolSource("grove", {}), "https://github.com/kodhama/grove.git");
  assert.equal(
    toolSource("grove", { KODHAMA_TOOL_SOURCE: "/srv/tools" }),
    "file:///srv/tools/grove",
  );
});

test("a fetched tool carries its tag, the clone's commit and its skills, and the clone is gone after", (t) => {
  const machine = scratch(t);
  const tool = machine.fakeTool("demo", ["0.1.0", "0.9.0", "0.10.0", "0.11.0-rc.1"]);
  const options = { env: machine.env, tmp: machine.tmp };

  const newest = withTool("demo", undefined, options, (fetched) => fetched);
  assert.ok("value" in newest, JSON.stringify(newest));
  assert.equal(newest.value.tag, "v0.10.0");
  assert.equal(newest.value.commit, tool.commit("v0.10.0"));
  assert.equal(newest.value.source, `file://${tool.path}`);
  assert.deepEqual(
    newest.value.skills.map(({ name, files }) => ({ name, files })),
    [
      { name: "alpha", files: ["SKILL.md", join("scripts", "run.sh")] },
      { name: "beta", files: ["SKILL.md"] },
    ],
  );

  const older = withTool("demo", "v0.1.0", options, (fetched) => fetched);
  assert.ok("value" in older);
  assert.equal(older.value.tag, "v0.1.0");
  assert.equal(older.value.commit, tool.commit("v0.1.0"));

  const named = withTool("demo", "v0.11.0-rc.1", options, (fetched) => fetched.tag);
  assert.deepEqual(named, { value: "v0.11.0-rc.1" });

  assert.deepEqual(machine.written(), UNTOUCHED);
});

test("a fresh install copies each skill into both harnesses, marked, and writes the lock last", (t) => {
  const machine = scratch(t);
  const tool = machine.fakeTool("demo", ["0.1.0", "0.9.0", "0.10.0", "0.11.0-rc.1"]);
  const commit = tool.commit("v0.10.0");

  const outcome = machine.kodhama(["install", "demo"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  assert.match(outcome.stdout, /Installed demo v0\.10\.0/);
  const skillTree = ["SKILL.md", "scripts", join("scripts", "run.sh")];
  /** @param {string} base @param {string} skills */
  const installed = (base, skills) =>
    ["alpha", "beta"].flatMap((skill) => [
      join(skills, skill),
      join(skills, skill, MARKER),
      ...(skill === "alpha" ? skillTree : ["SKILL.md"]).map((rel) => join(skills, skill, rel)),
    ]).map((rel) => join(base, rel));
  assert.deepEqual(
    machine.written(),
    [
      ...UNTOUCHED,
      ...installed("claude", "skills"),
      join("claude", "skills"),
      join("data", "kodhama"),
      join("data", "kodhama", "lock.json"),
      join("home", ".agents"),
      join("home", ".agents", "skills"),
      ...installed(join("home", ".agents"), "skills"),
    ].sort(),
  );
  for (const skills of [machine.claudeSkills, machine.codexSkills]) {
    for (const skill of ["alpha", "beta"]) {
      assert.deepEqual(readJson(join(skills, skill, MARKER)), { commit, skill, tag: "v0.10.0", tool: "demo" });
    }
    assert.notEqual(statSync(join(skills, "alpha", "scripts", "run.sh")).mode & 0o111, 0);
    assert.equal(statSync(join(skills, "alpha", "SKILL.md")).mode & 0o111, 0);
  }

  const text = readFileSync(machine.lock, "utf8");
  assert.equal(text, `${JSON.stringify(readJson(machine.lock), null, 2)}\n`);
  assert.deepEqual(readJson(machine.lock), {
    lock: 1,
    tools: {
      demo: {
        commit,
        harnesses: ["claude", "codex"],
        skills: {
          alpha: {
            "SKILL.md": { exec: false, sha256: sha256(readFileSync(join(machine.claudeSkills, "alpha", "SKILL.md"))) },
            "scripts/run.sh": { exec: true, sha256: sha256("#!/bin/sh\necho alpha\n") },
          },
          beta: { "SKILL.md": { exec: false, sha256: sha256("---\nname: beta\n---\nBeta.\n") } },
        },
        source: `file://${tool.path}`,
        tag: "v0.10.0",
      },
    },
  });
  assert.ok(text.indexOf('"commit"') < text.indexOf('"harnesses"'), "keys are sorted");
});

test("install demo#0.1.0 installs that older tag", (t) => {
  const machine = scratch(t);
  const tool = machine.fakeTool("demo", ["0.1.0", "0.2.0"]);

  const outcome = machine.kodhama(["install", "demo#0.1.0"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  const locked = /** @type {any} */ (readJson(machine.lock)).tools.demo;
  assert.equal(locked.tag, "v0.1.0");
  assert.equal(locked.commit, tool.commit("v0.1.0"));
  assert.match(readFileSync(join(machine.codexSkills, "alpha", "SKILL.md"), "utf8"), /Alpha 0\.1\.0/);
});

test("a project-scope install writes the repo's skills folders and its own lock, and no user state", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);
  const repo = machine.project("work");
  mkdirSync(join(repo, "src"));

  const outcome = machine.kodhama(["install", "demo", "--scope", "project"], { cwd: join(repo, "src") });

  assert.equal(outcome.status, 0, outcome.stderr);
  for (const skills of [join(repo, ".claude", "skills"), join(repo, ".agents", "skills")]) {
    assert.deepEqual(readdirSync(skills).sort(), ["alpha", "beta"]);
  }
  assert.equal(/** @type {any} */ (readJson(join(repo, ".kodhama", "cli", "lock.json"))).tools.demo.tag, "v0.1.0");
  assert.deepEqual(readdirSync(join(repo, ".kodhama")), ["cli"]);
  assert.deepEqual(readdirSync(join(repo, ".kodhama", "cli")), ["lock.json"]);
  assert.ok(!existsSync(machine.lock));
  assert.ok(!existsSync(machine.claudeSkills));
  assert.ok(!existsSync(machine.codexSkills));
});

test("project scope outside a git repo refuses", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);

  const outcome = machine.kodhama(["install", "demo", "--scope", "project"]);

  assert.equal(outcome.status, 1);
  assert.match(outcome.stderr, /not inside a git repo/);
  assert.deepEqual(machine.written(), UNTOUCHED);
});

test("a second install of the same tag says already installed and changes no byte or mtime", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);
  assert.equal(machine.kodhama(["install", "demo"]).status, 0);
  const before = machine.state();

  const outcome = machine.kodhama(["install", "demo"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  assert.match(outcome.stdout, /already installed/);
  assert.deepEqual(machine.state(), before);
});

test("an unmarked or foreign folder at a target refuses the install, and nothing is written", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);
  writeFiles(machine.codexSkills, { "alpha/SKILL.md": "my own alpha\n" });
  writeFiles(machine.claudeSkills, { [`beta/${MARKER}`]: `${JSON.stringify({ tool: "other" })}\n`, "beta/SKILL.md": "other's\n" });
  const before = machine.state();

  const outcome = machine.kodhama(["install", "demo"]);

  assert.equal(outcome.status, 1);
  assert.ok(outcome.stderr.includes(join(machine.codexSkills, "alpha")), outcome.stderr);
  assert.ok(outcome.stderr.includes(join(machine.claudeSkills, "beta")), outcome.stderr);
  assert.match(outcome.stderr, /marked as other's/);
  assert.deepEqual(machine.state(), before);
});

test("install at another tag than the lock's points at update", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0", "0.2.0"]);
  assert.equal(machine.kodhama(["install", "demo#0.1.0"]).status, 0);
  const before = machine.state();

  const outcome = machine.kodhama(["install", "demo"]);

  assert.equal(outcome.status, 1);
  assert.match(outcome.stderr, /installed at v0\.1\.0.*kodhama update demo/s);
  assert.deepEqual(machine.state(), before);
});

test("install with a new --harness at the same tag adds that harness's copies", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);

  assert.equal(machine.kodhama(["install", "demo", "--harness", "claude"]).status, 0);
  assert.ok(!existsSync(machine.codexSkills));
  assert.deepEqual(/** @type {any} */ (readJson(machine.lock)).tools.demo.harnesses, ["claude"]);

  const outcome = machine.kodhama(["install", "demo", "--harness", "codex"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  assert.deepEqual(readdirSync(machine.codexSkills).sort(), ["alpha", "beta"]);
  assert.deepEqual(/** @type {any} */ (readJson(machine.lock)).tools.demo.harnesses, ["claude", "codex"]);
});

test("a missing tag, a tool with no tags and a tool not in the source each exit 1, writing nothing", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);
  machine.fakeTool("bare", []);

  for (const [args, said] of /** @type {const} */ ([
    [["install", "demo#v9.9.9"], /no tag v9\.9\.9/],
    [["install", "bare"], /no vX\.Y\.Z tag/],
    [["install", "ghost"], /could not list the tags/],
  ])) {
    const outcome = machine.kodhama(args);
    assert.equal(outcome.status, 1, JSON.stringify(args));
    assert.match(outcome.stderr, said, outcome.stderr);
  }
  assert.deepEqual(machine.written(), UNTOUCHED);
});

test("a tool whose kodhama.json or skills break the contract exits 1, writing nothing", (t) => {
  const machine = scratch(t);
  /** @param {unknown} value */
  const manifest = (value) => ({ "kodhama.json": `${JSON.stringify(value)}\n` });
  const cases = [
    ["missing", { files: { "kodhama.json": null } }, /has no kodhama\.json/],
    ["notjson", { files: { "kodhama.json": "{\n" } }, /not valid JSON/],
    ["mismatch", { files: manifest({ name: "other", skills: "skills" }) }, /names other/],
    ["typo", { files: manifest({ name: "typo", skills: "skills", skil: "x" }) }, /unknown key skil/],
    ["escape", { files: manifest({ name: "escape", skills: "../x" }) }, /\.\./],
    [
      "linkout",
      { files: manifest({ name: "linkout", skills: "out" }), links: { out: "/" } },
      /outside the tool's repo/,
    ],
    ["badname", { files: { "skills/Bad_Name/SKILL.md": "Bad.\n" } }, /Bad_Name is not a skill name/],
    ["symlink", { links: { "skills/alpha/link.md": "SKILL.md" } }, /skills\/alpha\/link\.md is a symlink/],
    ["marker", { files: { "skills/alpha/.kodhama-skill.json": "{}\n" } }, /skills\/alpha ships its own \.kodhama-skill\.json/],
    ["noskills", { files: { "skills/alpha/SKILL.md": null, "skills/alpha/scripts/run.sh": null, "skills/beta/SKILL.md": null, "skills/README.md": "none\n" } }, /holds no skill/],
    [
      "helper",
      { files: manifest({ name: "helper", skills: "skills", helper: ">=0.1.0" }) },
      /later kodhama/,
    ],
  ];

  for (const [name, change, said] of cases) {
    machine.fakeTool(name, ["0.1.0"], change);
    const outcome = machine.kodhama(["install", name]);
    assert.equal(outcome.status, 1, `${name}: ${outcome.stderr}`);
    assert.match(outcome.stderr, said, `${name}: ${outcome.stderr}`);
  }
  assert.deepEqual(machine.written(), UNTOUCHED);
});

test("kodhama.json is a name and a skills folder inside the repo, and nothing else", () => {
  assert.deepEqual(parseManifest('{"name": "grove", "skills": "skills"}', "grove"), {
    manifest: { name: "grove", skills: "skills" },
  });
  assert.ok("manifest" in parseManifest('{"name": "grove", "skills": "./a/b"}', "grove"));
  for (const text of [
    "[]",
    "null",
    '"grove"',
    '{"skills": "skills"}',
    '{"name": "grove"}',
    '{"name": "grove", "skills": 1}',
    '{"name": "grove", "skills": ""}',
    '{"name": "grove", "skills": "/etc"}',
    '{"name": "grove", "skills": "a/../b"}',
    '{"name": "grove", "skills": "a\\\\..\\\\b"}',
    '{"name": "Grove", "skills": "skills"}',
  ]) {
    assert.ok("error" in parseManifest(text, "grove"), text);
  }
});

test("copying a skill keeps its bytes and its exec bit, in both harness folders", (t) => {
  const machine = scratch(t);
  machine.fakeTool("demo", ["0.1.0"]);
  const targets = [join(machine.claude, "skills"), join(machine.home, ".agents", "skills")];

  const copied = withTool("demo", undefined, { env: machine.env, tmp: machine.tmp }, (fetched) => {
    const alpha = fetched.skills.find((skill) => skill.name === "alpha");
    assert.ok(alpha);
    for (const target of targets) copyFiles(alpha.dir, join(target, "alpha"), alpha.files);
    return readFileSync(join(alpha.dir, "scripts", "run.sh"));
  });

  assert.ok("value" in copied);
  for (const target of targets) {
    const script = join(target, "alpha", "scripts", "run.sh");
    assert.notEqual(statSync(script).mode & 0o111, 0, script);
    assert.equal(statSync(join(target, "alpha", "SKILL.md")).mode & 0o111, 0);
    assert.deepEqual(readFileSync(script), copied.value);
  }
});

test("a skill folder holding a special file is refused", (t) => {
  const machine = scratch(t);
  const skill = join(machine.tmp, "skill");
  mkdirSync(skill);
  writeFileSync(join(skill, "SKILL.md"), "x\n");
  execFileSync("mkfifo", [join(skill, "pipe")]);

  const listed = listFiles(skill);

  assert.ok("error" in listed);
  assert.match(listed.error, /pipe is not a regular file/);
});

// The grove guard and --migrate. Each guard test has no grove repo in the
// source unless it needs one, so a run that fetched would fail on the fetch
// and say so, not on the guard.

const SETTINGS_WITH_GROVE = `{
  "enabledPlugins": {
    "grove@grove": true,
    "trellis@kodhama": true
  },
  "extraKnownMarketplaces": {
    "grove": { "source": { "source": "github", "repo": "kodhama/grove" } },
    "kodhama": { "source": { "source": "github", "repo": "kodhama/stewards" } }
  },
  "statusLine": "a \\u2014 dash"
}
`;

const TOML_HEAD = `model = "o3"

[plugins."trellis@kodhama"]
enabled = true

[marketplaces.kodhama]
source = "https://github.com/kodhama/stewards"
`;

const TOML_GROVE = `[plugins."grove@grove"]
enabled = true

[plugins."grove@grove".settings]
mode = "full"

[marketplaces.grove]
source = "https://github.com/kodhama/grove"

`;

const TOML_TAIL = `[projects."/x/grove"]
trust_level = "trusted"
`;

test("a Claude grove enable blocks install grove before any fetch, naming the file and key", (t) => {
  const machine = scratch(t);
  writeFiles(machine.claude, { "settings.json": '{"enabledPlugins": {"grove@grove": true}}\n' });
  const before = machine.state();

  const outcome = machine.kodhama(["install", "grove"]);

  assert.equal(outcome.status, 1);
  assert.ok(outcome.stderr.includes(`${join(machine.claude, "settings.json")}: enabledPlugins["grove@grove"]`), outcome.stderr);
  assert.match(outcome.stderr, /--migrate/);
  assert.doesNotMatch(outcome.stderr, /could not list/);
  assert.deepEqual(machine.state(), before);
});

test("a Codex grove plugin table with enabled = true blocks the same way", (t) => {
  const machine = scratch(t);
  writeFiles(machine.codex, { "config.toml": `${TOML_HEAD}\n[plugins."grove@grove"]\nenabled = true # on\n` });
  const before = machine.state();

  const outcome = machine.kodhama(["install", "grove"]);

  assert.equal(outcome.status, 1);
  assert.ok(outcome.stderr.includes(`${join(machine.codex, "config.toml")}: [plugins."grove@grove"] enabled`), outcome.stderr);
  assert.doesNotMatch(outcome.stderr, /could not list/);
  assert.deepEqual(machine.state(), before);
});

test("disabled grove entries do not block", (t) => {
  const machine = scratch(t);
  machine.fakeTool("grove", ["0.3.0"]);
  writeFiles(machine.claude, { "settings.json": '{"enabledPlugins": {"grove@grove": false}}\n' });
  writeFiles(machine.codex, { "config.toml": '[plugins."grove@grove"]\nenabled = false\n' });

  const outcome = machine.kodhama(["install", "grove"]);

  assert.equal(outcome.status, 0, outcome.stderr);
});

test("a dotted grove key in config.toml blocks a plain install, to be edited by hand", (t) => {
  const machine = scratch(t);
  writeFiles(machine.codex, { "config.toml": 'plugins."grove@grove".enabled = true\n' });
  const before = machine.state();

  const outcome = machine.kodhama(["install", "grove"]);

  assert.equal(outcome.status, 1);
  assert.match(outcome.stderr, /config\.toml: line 1/);
  assert.match(outcome.stderr, /by hand/);
  assert.doesNotMatch(outcome.stderr, /could not list/);
  assert.deepEqual(machine.state(), before);
});

test("install --migrate takes out only grove's enables and marketplace, records a receipt first, then installs", (t) => {
  const machine = scratch(t);
  machine.fakeTool("grove", ["0.3.0"]);
  const settings = join(machine.claude, "settings.json");
  const config = join(machine.codex, "config.toml");
  const tomlBefore = `${TOML_HEAD}\n${TOML_GROVE}${TOML_TAIL}`;
  writeFiles(machine.claude, { "settings.json": SETTINGS_WITH_GROVE });
  writeFiles(machine.codex, { "config.toml": tomlBefore });

  const outcome = machine.kodhama(["install", "grove", "--migrate"]);

  assert.equal(outcome.status, 0, outcome.stderr);
  assert.equal(readFileSync(config, "utf8"), `${TOML_HEAD}\n${TOML_TAIL}`);
  const before = /** @type {any} */ (JSON.parse(SETTINGS_WITH_GROVE));
  delete before.enabledPlugins["grove@grove"];
  delete before.extraKnownMarketplaces.grove;
  assert.deepEqual(readJson(settings), before);
  assert.match(outcome.stdout, /claude plugin marketplace remove grove/);

  const receipts = join(machine.data, "kodhama", "receipts");
  const [name, ...more] = readdirSync(receipts);
  assert.deepEqual(more, []);
  assert.match(name, /^migrate-grove-\d{8}T\d{6}Z\.json$/);
  const receipt = /** @type {any} */ (readJson(join(receipts, name)));
  assert.equal(receipt.receipt, 1);
  assert.equal(receipt.kind, "migrate");
  assert.equal(receipt.tool, "grove");
  assert.deepEqual(
    receipt.files.map((/** @type {any} */ file) => [file.path, file.original, file.sha256_before, file.sha256_after]),
    [
      [settings, SETTINGS_WITH_GROVE, sha256(SETTINGS_WITH_GROVE), sha256(readFileSync(settings))],
      [config, tomlBefore, sha256(tomlBefore), sha256(readFileSync(config))],
    ],
  );
  assert.deepEqual(
    receipt.files[1].removed.map((/** @type {any} */ item) => item.key),
    ['plugins."grove@grove"', 'plugins."grove@grove".settings', "marketplaces.grove"],
  );
  assert.equal(receipt.files[1].removed.map((/** @type {any} */ item) => item.text).join(""), TOML_GROVE);
  assert.deepEqual(
    receipt.files[0].removed,
    [
      { key: 'enabledPlugins["grove@grove"]', text: "true" },
      { key: "extraKnownMarketplaces.grove", text: JSON.stringify(JSON.parse(SETTINGS_WITH_GROVE).extraKnownMarketplaces.grove) },
    ],
  );
  assert.equal(/** @type {any} */ (readJson(machine.lock)).tools.grove.tag, "v0.3.0");
});

test("install --migrate with a missing tag writes no receipt and edits nothing", (t) => {
  const machine = scratch(t);
  machine.fakeTool("grove", ["0.3.0"]);
  writeFiles(machine.claude, { "settings.json": SETTINGS_WITH_GROVE });
  const before = machine.state();

  const outcome = machine.kodhama(["install", "grove#v9.9.9", "--migrate"]);

  assert.equal(outcome.status, 1);
  assert.match(outcome.stderr, /no tag v9\.9\.9/);
  assert.deepEqual(machine.state(), before);
});

test("--migrate refuses TOML it does not recognise or cannot cut cleanly, leaving config and receipts alone", (t) => {
  const machine = scratch(t);
  machine.fakeTool("grove", ["0.3.0"]);
  for (const toml of [
    'plugins."grove@grove".enabled = true\n',
    `[plugins."grove@grove"]\nenabled = true\nnote = """\nmany lines\n"""\n`,
    `[plugins."grove@grove"]\nenabled = true\n\n[other]\nplugins = { "grove@grove" = { enabled = true } }\n`,
    `[plugins."grove@grove"]\nenabled = true\nargs = [\n  "never closed",\n`,
  ]) {
    writeFiles(machine.codex, { "config.toml": toml });
    const before = machine.state();

    const outcome = machine.kodhama(["install", "grove", "--migrate"]);

    assert.equal(outcome.status, 1, toml);
    assert.match(outcome.stderr, /by hand/, toml);
    assert.deepEqual(machine.state(), before, toml);
  }
});

test("a project-file grove enable refuses a project-scope install, even with --migrate", (t) => {
  const machine = scratch(t);
  machine.fakeTool("grove", ["0.3.0"]);
  for (const [rel, text] of [
    [join(".claude", "settings.local.json"), '{"enabledPlugins": {"grove@grove": true}}\n'],
    [join(".codex", "config.toml"), '[plugins."grove@grove"]\nenabled = true\n'],
  ]) {
    const repo = machine.project(`work-${rel.split(sep)[0].slice(1)}`);
    writeFiles(repo, { [rel]: text });
    const before = machine.state();

    for (const args of [["install", "grove", "--scope", "project"], ["install", "grove", "--scope", "project", "--migrate"]]) {
      const outcome = machine.kodhama(args, { cwd: repo });
      assert.equal(outcome.status, 1, rel);
      assert.ok(outcome.stderr.includes(join(repo, rel)), outcome.stderr);
      assert.deepEqual(machine.state(), before, rel);
    }
  }
});

test("update refuses while grove is enabled, before fetching", (t) => {
  const machine = scratch(t);
  machine.fakeTool("grove", ["0.3.0", "0.4.0"]);
  assert.equal(machine.kodhama(["install", "grove#0.3.0"]).status, 0);
  writeFiles(machine.claude, { "settings.json": '{"enabledPlugins": {"grove@kodhama": true}}\n' });
  const before = machine.state();

  const outcome = machine.kodhama(["update", "grove"]);

  assert.equal(outcome.status, 1);
  assert.match(outcome.stderr, /enabledPlugins\["grove@kodhama"\]/);
  assert.deepEqual(machine.state(), before);
});

test("a multi-line array in grove's table cannot hide its enabled = true, and --migrate cuts the whole table", (t) => {
  const machine = scratch(t);
  const config = join(machine.codex, "config.toml");
  // Nested arrays on lines of their own start with "[", and one holds a "]"
  // inside a string, so a header test that ignores either misreads the file.
  const table = `[plugins."grove@grove"]\nargs = [\n  ["a]", "b"],\n  [ "c" ], # a ] in a comment\n]\nenabled = true\n\n`;
  writeFiles(machine.codex, { "config.toml": `${TOML_HEAD}\n${table}${TOML_TAIL}` });

  const blocked = machine.kodhama(["install", "grove"]);
  assert.equal(blocked.status, 1);
  assert.ok(blocked.stderr.includes(`${config}: [plugins."grove@grove"] enabled`), blocked.stderr);

  machine.fakeTool("grove", ["0.3.0"]);
  const migrated = machine.kodhama(["install", "grove", "--migrate"]);
  assert.equal(migrated.status, 0, migrated.stderr);
  assert.equal(readFileSync(config, "utf8"), `${TOML_HEAD}\n${TOML_TAIL}`);
});

test(`a quoted "enabled" key in grove's table blocks too`, (t) => {
  const machine = scratch(t);
  writeFiles(machine.codex, { "config.toml": '[plugins."grove@grove"]\n"enabled" = true\n' });

  const outcome = machine.kodhama(["install", "grove"]);

  assert.equal(outcome.status, 1);
  assert.match(outcome.stderr, /\[plugins\."grove@grove"\] enabled/);
});
