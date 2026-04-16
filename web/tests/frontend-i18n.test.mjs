import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";

function loadLocale(language) {
  const baseDir = join(process.cwd(), "locales", language);
  return {
    ...JSON.parse(readFileSync(join(baseDir, "common.json"), "utf8")),
    ...JSON.parse(readFileSync(join(baseDir, "app.json"), "utf8")),
  };
}

test("frontend i18n locales include all newly required UI keys", () => {
  const en = loadLocale("en");
  const zh = loadLocale("zh");

  const requiredKeys = [
    "Visualize",
    "Generate SVG, Chart.js, or Mermaid visualizations",
    "Describe the chart or diagram you want to visualize...",
    "Render Mode",
    "Chart.js",
    "SVG",
    "Mermaid",
    "Show code",
    "Hide code",
    "Copied",
    "Copy code",
    "Review",
    "Chart rendering error",
    "SVG rendering error",
    "Reference",
    "image",
    "Describe what you want to learn",
    "Generate learning plan",
    "Notebook Context",
    "Select Records",
    "Learning History",
    "Completed",
    "In Progress",
    "Planned",
    "Ready to open",
    "Generating interactive page...",
    "Generation failed",
    "Waiting in queue",
    "Open",
    "Starting...",
    "Waiting for the selected interactive page...",
    "Open any page once it is ready. Early stages are prioritized.",
    "Current page",
    "Knowledge Point",
    "Loading history...",
    "No learning history yet",
    "Summary",
    "Complete",
    "pages ready",
    "Untitled",
    "Untitled Session",
  ];

  for (const key of requiredKeys) {
    assert.ok(en[key], `missing en locale key: ${key}`);
    assert.ok(zh[key], `missing zh locale key: ${key}`);
  }
});

test("new zh translations follow the approved mixed terminology", () => {
  const zh = loadLocale("zh");

  assert.equal(zh["Visualize"], "可视化");
  assert.equal(
    zh["Generate SVG, Chart.js, or Mermaid visualizations"],
    "生成 SVG、Chart.js 或 Mermaid 可视化内容",
  );
  assert.equal(zh["Chart.js"], "Chart.js 图表");
  assert.equal(zh["SVG"], "SVG 图形");
  assert.equal(zh["Mermaid"], "Mermaid 图示");
  assert.equal(zh["Render Mode"], "渲染模式");
});
