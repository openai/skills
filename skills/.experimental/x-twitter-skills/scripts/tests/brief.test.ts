import test from "node:test";
import assert from "node:assert/strict";
import { createBriefReport } from "../lib/brief";
import { type Tweet } from "../lib/api";
import { buildResearchPlan } from "../lib/planner";

const TWEETS: Tweet[] = [
  {
    id: "1",
    text: "Great launch, fast benchmark results",
    author_id: "u1",
    username: "alice",
    name: "Alice",
    created_at: "2026-02-01T00:00:00.000Z",
    conversation_id: "1",
    metrics: { likes: 100, retweets: 10, replies: 3, quotes: 2, impressions: 1000, bookmarks: 5 },
    urls: ["https://github.com/openai/openai-agents"],
    mentions: [],
    hashtags: [],
    tweet_url: "https://x.com/alice/status/1",
  },
  {
    id: "2",
    text: "This update has a bug and outage risk",
    author_id: "u2",
    username: "bob",
    name: "Bob",
    created_at: "2026-02-01T01:00:00.000Z",
    conversation_id: "2",
    metrics: { likes: 50, retweets: 4, replies: 2, quotes: 0, impressions: 600, bookmarks: 1 },
    urls: ["https://docs.example.com/postmortem"],
    mentions: [],
    hashtags: [],
    tweet_url: "https://x.com/bob/status/2",
  },
  {
    id: "1",
    text: "Great launch, fast benchmark results",
    author_id: "u1",
    username: "alice",
    name: "Alice",
    created_at: "2026-02-01T00:00:00.000Z",
    conversation_id: "1",
    metrics: { likes: 100, retweets: 10, replies: 3, quotes: 2, impressions: 1000, bookmarks: 5 },
    urls: ["https://github.com/openai/openai-agents"],
    mentions: [],
    hashtags: [],
    tweet_url: "https://x.com/alice/status/1",
  },
];

test("createBriefReport dedupes tweets and computes rankings", () => {
  const plan = buildResearchPlan("OpenAI agents", { maxQueries: 4 });
  const report = createBriefReport({
    question: "OpenAI agents",
    mode: "recent",
    since: "7d",
    plan,
    queryRuns: [
      { id: "core", label: "Core", query: "openai agents", rawCount: 2, cached: false },
      { id: "links", label: "Links", query: "openai agents has:links", rawCount: 1, cached: true },
    ],
    tweets: TWEETS,
  });

  assert.equal(report.uniqueTweetCount, 2);
  assert.equal(report.rawTweetReads, 3);
  assert.equal(report.topVoices[0]?.username, "alice");
  assert.equal(report.topDomains[0]?.domain, "github.com");
  assert.ok(report.themes.some((t) => t.theme === "Launches"));
  assert.ok(report.themes.some((t) => t.theme === "Reliability"));
});
