import type { VisualizeRenderType } from "@/lib/visualize-types";

const TOOL_LABEL_KEYS: Record<string, string> = {
  brainstorm: "Brainstorm",
  rag: "RAG",
  web_search: "Web Search",
  code_execution: "Code Execution",
  reason: "Reason",
  paper_search: "Arxiv Search",
};

const TOOL_DESCRIPTION_KEYS: Record<string, string> = {
  brainstorm: "Broadly explore multiple possibilities for a topic and give a short rationale for each.",
  rag: "Search a knowledge base using Retrieval-Augmented Generation. Returns relevant passages and an LLM-synthesised answer.",
  web_search: "Search the web and return summarised results with citations.",
  code_execution:
    "Turn a natural-language computation request into Python, run it in a restricted Python worker, and return the result.",
  reason:
    "Perform deep reasoning on a complex sub-problem using a dedicated LLM call. Use when the current context is insufficient for a confident answer.",
  paper_search: "Search arXiv preprints by keyword and return concise metadata.",
};

const CAPABILITY_LABEL_KEYS: Record<string, string> = {
  chat: "Chat",
  deep_solve: "Deep Solve",
  deep_question: "Quiz Generation",
  deep_research: "Deep Research",
  math_animator: "Math Animator",
  visualize: "Visualize",
};

const CAPABILITY_DESCRIPTION_KEYS: Record<string, string> = {
  chat: "Agentic chat with autonomous tool selection across enabled tools.",
  deep_solve: "Multi-agent problem solving (Plan -> ReAct -> Write).",
  deep_question: "Fast question generation (Template batches -> Generate).",
  deep_research: "Multi-agent deep research with report generation.",
  math_animator: "Generate math animations or storyboard images with Manim.",
  visualize: "Generate SVG, Chart.js, or Mermaid visualizations",
};

const VISUALIZE_RENDER_TYPE_LABEL_KEYS: Record<VisualizeRenderType, string> = {
  chartjs: "Chart.js",
  svg: "SVG",
  mermaid: "Mermaid",
};

function titleCase(value: string): string {
  return value.replaceAll("_", " ").replace(/\b\w/g, (char) => char.toUpperCase());
}

export function getToolLabelKey(name: string): string {
  return TOOL_LABEL_KEYS[name] ?? titleCase(name);
}

export function getToolDescriptionKey(name: string): string | null {
  return TOOL_DESCRIPTION_KEYS[name] ?? null;
}

export function getCapabilityLabelKey(name: string): string {
  return CAPABILITY_LABEL_KEYS[name] ?? titleCase(name);
}

export function getCapabilityDescriptionKey(name: string): string | null {
  return CAPABILITY_DESCRIPTION_KEYS[name] ?? null;
}

export function getVisualizeRenderTypeLabelKey(renderType: VisualizeRenderType): string {
  return VISUALIZE_RENDER_TYPE_LABEL_KEYS[renderType];
}
