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
  "it", "of", "on", "or", "that", "the", "this", "to", "what", "when", "where", "who", "why", "with",
  "about", "people", "saying", "say", "think", "thoughts", "opinion", "opinions",
]);

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

function addQuery(queries: PlannedQuery[], id: string, label: string, query: string, why: string) {
  const trimmed = normalizeText(query);
  if (!trimmed) return;
  if (queries.some((q) => q.query.toLowerCase() === trimmed.toLowerCase())) return;
  queries.push({ id, label, query: trimmed, why });
}

function inferNotes(question: string): string[] {
  const notes: string[] = [];
  if (/\b(today|now|right now|latest|recent)\b/i.test(question)) {
    notes.push("Prioritize recent mode with --since 1d or --since 12h.");
  }
  if (/\b(history|since\s+\d{4}|all time|long[- ]term|over years)\b/i.test(question)) {
    notes.push("Use --archive for historical coverage.");
  }
  if (/\bcompare|vs\b|versus\b/i.test(question)) {
    notes.push("Separate each side of the comparison into dedicated queries.");
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

  const queries: PlannedQuery[] = [];

  addQuery(
    queries,
    "core",
    "Core Discourse",
    `${baseTopic} lang:en -is:retweet`,
    "Get baseline signal and mainstream discussion."
  );

  addQuery(
    queries,
    "pain",
    "Bugs and Complaints",
    `(${baseTopic}) (bug OR issue OR broken OR outage OR regression) lang:en -is:retweet`,
    "Pull risk and failure reports."
  );

  addQuery(
    queries,
    "positive",
    "Wins and Positive Signal",
    `(${baseTopic}) (shipped OR launch OR release OR benchmark OR love) lang:en -is:retweet`,
    "Capture launch momentum and positive outcomes."
  );

  addQuery(
    queries,
    "links",
    "Linked Evidence",
    `(${baseTopic}) has:links lang:en -is:retweet`,
    "Find posts that reference external sources worth reading."
  );

  for (const handle of handles) {
    addQuery(
      queries,
      `handle-${handle}`,
      `Expert: @${handle}`,
      `from:${handle} (${baseTopic}) -is:retweet`,
      "Check direct statements from named accounts."
    );
  }

  const clipped = queries.slice(0, maxQueries);

  return {
    question: normalizedQuestion,
    generatedAt: new Date().toISOString(),
    queries: clipped,
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
