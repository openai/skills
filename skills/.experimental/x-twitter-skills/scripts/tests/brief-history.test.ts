import test from "node:test";
import assert from "node:assert/strict";
import {
  compareSnapshots,
  createSnapshot,
  estimateWorstCaseCost,
  type BriefSnapshot,
} from "../lib/brief-history";
import { createBriefReport } from "../lib/brief";
import { buildResearchPlan } from "../lib/planner";
import type { Tweet } from "../lib/api";

const TWEETS: Tweet[] = [
  {
    id: "a",
    text: "Great launch and benchmark win",
    author_id: "u1",
    username: "alpha",
    name: "Alpha",
    created_at: "2026-02-01T00:00:00.000Z",
    conversation_id: "a",
    metrics: { likes: 40, retweets: 4, replies: 1, quotes: 0, impressions: 800, bookmarks: 0 },
    urls: ["https://github.com/org/repo"],
    mentions: [],
    hashtags: [],
    tweet_url: "https://x.com/alpha/status/a",
  },
  {
    id: "b",
    text: "This has a bug and outage risk",
    author_id: "u2",
    username: "beta",
    name: "Beta",
    created_at: "2026-02-01T01:00:00.000Z",
    conversation_id: "b",
    metrics: { likes: 10, retweets: 1, replies: 2, quotes: 0, impressions: 300, bookmarks: 0 },
    urls: [],
    mentions: [],
    hashtags: [],
    tweet_url: "https://x.com/beta/status/b",
  },
];

test("estimateWorstCaseCost computes deterministic upper bound", () => {
  assert.equal(estimateWorstCaseCost(4, 2), 4);
  assert.equal(estimateWorstCaseCost(5, 1, { tweetsPerPage: 50, readCostUsd: 0.01 }), 2.5);
});

test("createSnapshot captures top voices and theme counts", () => {
  const report = createBriefReport({
    question: "openai agents",
    mode: "recent",
    since: "7d",
    plan: buildResearchPlan("openai agents", { maxQueries: 4 }),
    queryRuns: [{ id: "core", label: "Core", query: "openai agents", rawCount: 2, cached: false }],
    tweets: TWEETS,
  });

  const snapshot = createSnapshot(report);
  assert.equal(snapshot.question, "openai agents");
  assert.ok(snapshot.topVoices.includes("alpha"));
  assert.ok(snapshot.themes["Launches"] >= 1);
});

test("compareSnapshots surfaces voice and theme deltas", () => {
  const prev: BriefSnapshot = {
    question: "q",
    generatedAt: "2026-02-01T00:00:00.000Z",
    uniqueTweetCount: 20,
    rawTweetReads: 100,
    topVoices: ["alpha", "beta"],
    themes: { Launches: 7, Reliability: 2 },
  };

  const curr: BriefSnapshot = {
    question: "q",
    generatedAt: "2026-02-02T00:00:00.000Z",
    uniqueTweetCount: 28,
    rawTweetReads: 120,
    topVoices: ["alpha", "gamma"],
    themes: { Launches: 4, Reliability: 5 },
  };

  const delta = compareSnapshots(prev, curr);
  assert.equal(delta.uniqueTweetDelta, 8);
  assert.equal(delta.tweetReadDelta, 20);
  assert.deepEqual(delta.newVoices, ["gamma"]);
  assert.deepEqual(delta.droppedVoices, ["beta"]);
  assert.ok(delta.themeChanges.some((t) => t.theme === "Launches" && t.delta === -3));
  assert.ok(delta.themeChanges.some((t) => t.theme === "Reliability" && t.delta === 3));
});
