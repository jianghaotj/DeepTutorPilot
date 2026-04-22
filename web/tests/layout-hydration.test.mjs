import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const layoutPath = resolve(process.cwd(), "app/layout.tsx");
const layoutSource = readFileSync(layoutPath, "utf8");

test("RootLayout suppresses hydration warnings on body for extension-injected attributes", () => {
  assert.match(
    layoutSource,
    /<body[^>]*suppressHydrationWarning/,
    "Expected <body> to suppress hydration warnings for pre-hydration DOM mutations",
  );
});
