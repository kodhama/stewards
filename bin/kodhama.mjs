#!/usr/bin/env node
// The program `npx -y github:kodhama/stewards#v<version> <command>` runs. It
// prints a command's lines, to standard error when the command failed, and
// exits with its code. An error no command expected, such as a folder it
// could not read before writing anything, is printed as one line and exits 1.

import { run } from "../src/cli.mjs";

/** @type {import("../src/cli.mjs").Outcome} */
const { code, lines } = await run(process.argv.slice(2), process.cwd()).catch(
  (/** @type {unknown} */ error) => ({
    code: 1,
    lines: [
      `kodhama stopped: ${(error instanceof Error ? error.message : String(error)).replace(/\s*\n\s*/g, " ").trim()}`,
    ],
  }),
);
for (const line of lines) {
  if (code === 0) console.log(line);
  else console.error(line);
}
process.exitCode = code;
