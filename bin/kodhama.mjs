#!/usr/bin/env node
// The program `npx -y github:kodhama/stewards#v<version> <command>` runs. It
// prints a command's lines, to standard error when the command failed, and
// exits with its code. An error no command expected, such as a folder it
// could not read before writing anything, is printed as one line, after any
// lines it carries of what was done before it, and exits 1.

import { run } from "../src/cli.mjs";

/** @type {import("../src/cli.mjs").Outcome} */
const { code, lines } = await run(process.argv.slice(2), process.cwd()).catch(
  (/** @type {unknown} */ error) => ({
    code: 1,
    lines: [
      ...(/** @type {{ lines?: string[] }} */ (error)?.lines ?? []),
      `kodhama stopped: ${(error instanceof Error ? error.message : String(error)).replace(/\s*\n\s*/g, " ").trim()}`,
    ],
  }),
);
for (const line of lines) {
  if (code === 0) console.log(line);
  else console.error(line);
}
process.exitCode = code;
// One turn of the event loop, so a SIGINT or SIGTERM that arrived while the
// command ran is handled now (and exits 130 or 143) instead of being dropped.
await new Promise((done) => setImmediate(done));
