export interface PlannedQuery {
  id: string;
  label: string;
  query: string;
  why: string;
}

export interface ResearchPlan {
  question: string;
  generatedAt: string;
  queries: PlannedQuery[];
  notes: string[];
}

const STOPWORDS = new Set([
  "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "how", "i", "in", "is",
  "it", "of", "on", "or", "that", "the", "this", "to", "what", "when", "where", "who", "why",
  "with", "about", "people", "saying", "say", "think", "thoughts", "opinion", "opinions", "just",
  "some", "their", "they", "them", "too", "want", "would", "could", "does", "did", "have", "had", "has",
]);

type QueryBuilder = (topic: string) => string;

interface IntentLane {
  id: string;
  label: string;
  why: string;
  build: QueryBuilder;
  enabled: (question: string) => boolean;
}

const LANE_LIBRARY: IntentLane[] = [
  {
    id: "core",
    label: "Core Discourse",
    why: "Capture broad community sentiment and signal baseline.",
    build: (topic) => `${topic} lang:en -is:retweet -is:reply`,
    enabled: () => true,
  },
  {
    id: "risk",
    label: "Reliability and Complaints",
    why: "Prioritize failures, outages, and quality concerns.",
    build: (topic) => `(${topic}) (bug OR issue OR outage OR regression OR error OR broken OR incident) lang:en -is:retweet`,
    enabled: (q) => /\b(bug|issue|outage|incident|regress|error|downtime|flaky|crash)\b/i.test(q),
  },
  {
    id: "wins",
    label: "Wins and Positive Signal",
    why: "Track launch momentum and strong execution stories.",
    build: (topic) => `(${topic}) (launch OR shipped OR release OR announcement OR benchmark OR improved OR wins) lang:en -is:retweet`,
    enabled: () => true,
  },
  {
    id: "evidence",
    label: "Linked Evidence",
    why: "Find posts that share docs, repos, PRs, or official references.",
    build: (topic) => `(${topic}) has:links lang:en -is:retweet`,
    enabled: () => true,
  },
  {
    id: "competition",
    label: "Competition and Alternatives",
    why: "Map relative positioning and framing versus alternatives.",
    build: (topic) => `(${topic}) (vs OR versus OR compare OR alternative OR competitor OR alternatives OR options) lang:en -is:retweet`,
    enabled: (q) =>
      /\b(compare|vs|versus|alternative|alternatives|competitor|competitors|which is better)\b/i.test(q),
  },
  {
    id: "economics",
    label: "Pricing, Cost and Economics",
    why: "Track business model and pricing pressure signals.",
    build: (topic) => `(${topic}) (pricing OR price OR cost OR revenue OR margin OR fees OR billing OR monetization) lang:en -is:retweet`,
    enabled: (q) => /\b(price|pricing|cost|revenue|fees?|monetization|billing)\b/i.test(q),
  },
  {
    id: "roadmap",
    label: "Roadmap and Official Signals",
    why: "Track explicit plans and official platform updates.",
    build: (topic) => `(${topic}) (roadmap OR "official" OR "release" OR "changelog" OR "announcement") lang:en -is:reply -is:retweet`,
    enabled: (q) => /\b(roadmap|announcement|release|plan|timeline|when)\b/i.test(q),
  },
];

function clamp(n: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, n));
}

function normalizeText(text: string): string {
  return text.replace(/\s+/g, " ").trim();
}

function removeHandles(text: string): string {
  return text.replace(/@[A-Za-z0-9_]{1,15}/g, "").replace(/\s+/g, " ").trim();
}

function extractHandles(text: string): string[] {
  const found = text.match(/@[A-Za-z0-9_]{1,15}/g) || [];
  const uniq = new Set(found.map((h) => h.replace(/^@/, "").toLowerCase()));
  return [...uniq];
}

function topicTokens(question: string): string[] {
  return normalizeText(removeHandles(question))
    .toLowerCase()
    .split(/[^a-z0-9$#]+/)
    .filter((t) => t.length > 1 && !STOPWORDS.has(t));
}

function buildTopicPhrase(question: string): string {
  const tokens = topicTokens(question);
  if (tokens.length === 0) return normalizeText(removeHandles(question));
  return tokens.slice(0, 7).join(" ");
}

function addQuery(
  queries: PlannedQuery[],
  id: string,
  label: string,
  query: string,
  why: string
) {
  const trimmed = normalizeText(query);
  if (!trimmed) return;
  if (queries.some((q) => q.query.toLowerCase() === trimmed.toLowerCase())) return;
  queries.push({ id, label, query: trimmed, why });
}

function pickLanes(question: string): IntentLane[] {
  return LANE_LIBRARY.filter((lane) => lane.enabled(question));
}

function inferNotes(question: string): string[] {
  const notes: string[] = [];
  if (/\b(today|now|right now|latest|recent)\b/i.test(question)) {
    notes.push("Favor short windows (`--since 1d`) and keep the API window tight.");
  }
  if (/\b(history|since\s+\d{4}|all time|long[- ]term|over years)\b/i.test(question)) {
    notes.push("Prefer archive mode and a wider window for context.");
  }
  if (/\b(compare|vs|versus)\b/i.test(question)) {
    notes.push("Split perspectives into dedicated queries and compare evidence quality.");
  }
  if (/\bsecurity|risk|breach|incident/i.test(question)) {
    notes.push("Watch both community commentary and official incident channels.");
  }
  return notes;
}

export function buildResearchPlan(
  question: string,
  opts: { maxQueries?: number } = {}
): ResearchPlan {
  const maxQueries = clamp(opts.maxQueries ?? 5, 2, 10);
  const normalizedQuestion = normalizeText(question);
  const baseTopic = buildTopicPhrase(normalizedQuestion) || normalizedQuestion;
  const handles = extractHandles(normalizedQuestion);
  const lanes = pickLanes(normalizedQuestion);
  const queries: PlannedQuery[] = [];

  for (const lane of lanes) {
    addQuery(queries, lane.id, lane.label, lane.build(baseTopic), lane.why);
  }

  for (const handle of handles) {
    addQuery(
      queries,
      `handle-${handle}`,
      `Expert: @${handle}`,
      `from:${handle} (${baseTopic}) -is:retweet -is:reply`,
      "Check direct statements from named accounts."
    );
  }

  return {
    question: normalizedQuestion,
    generatedAt: new Date().toISOString(),
    queries: queries.slice(0, maxQueries),
    notes: inferNotes(normalizedQuestion),
  };
}

export function formatPlanMarkdown(plan: ResearchPlan): string {
  let out = `# Research Plan: ${plan.question}\n\n`;
  out += `Generated: ${plan.generatedAt}\n\n`;

  if (plan.notes.length > 0) {
    out += "## Notes\n\n";
    for (const note of plan.notes) {
      out += `- ${note}\n`;
    }
    out += "\n";
  }

  out += "## Queries\n\n";
  for (const q of plan.queries) {
    out += `### ${q.label}\n`;
    out += `- Why: ${q.why}\n`;
    out += `- Query: \`${q.query}\`\n\n`;
  }

  return out;
}
