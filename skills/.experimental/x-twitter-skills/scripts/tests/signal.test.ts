import test from "node:test";
import assert from "node:assert/strict";
import { rankBySignal, type ScoredTweet } from "../lib/signal";
import type { Tweet } from "../lib/api";

const FIXED_NOW = Date.parse("2026-02-10T12:00:00.000Z");

const TWEETS: Tweet[] = [
  {
    id: "1",
    text: "Great launch is happening now with clear benchmark gains and open benchmarks",
    author_id: "u1",
    username: "alice",
    name: "Alice",
    created_at: "2026-02-10T11:30:00.000Z",
    conversation_id: "1",
    metrics: {
      likes: 120,
      retweets: 20,
      replies: 3,
      quotes: 2,
      impressions: 2000,
      bookmarks: 4,
    },
    urls: ["https://openai.com/blog"],
    mentions: [],
    hashtags: [],
    tweet_url: "https://x.com/alice/status/1",
  },
  {
    id: "2",
    text: "Old post about nothing specific",
    author_id: "u2",
    username: "bob",
    name: "Bob",
    created_at: "2026-02-01T11:30:00.000Z",
    conversation_id: "2",
    metrics: {
      likes: 800,
      retweets: 10,
      replies: 2,
      quotes: 1,
      impressions: 100,
      bookmarks: 0,
    },
    urls: [],
    mentions: [],
    hashtags: [],
    tweet_url: "https://x.com/bob/status/2",
  },
  {
    id: "1",
    text: "Duplicate id should collapse",
    author_id: "u1",
    username: "alice",
    name: "Alice",
    created_at: "2026-02-10T11:00:00.000Z",
    conversation_id: "1",
    metrics: {
      likes: 10,
      retweets: 2,
      replies: 1,
      quotes: 0,
      impressions: 100,
      bookmarks: 0,
    },
    urls: ["https://github.com/openai"],
    mentions: [],
    hashtags: [],
    tweet_url: "https://x.com/alice/status/1",
  },
];

test("rankBySignal dedupes duplicate ids", () => {
  const scored = rankBySignal(TWEETS, { nowMs: FIXED_NOW });
  assert.equal(scored.length, 2);
});

test("rankBySignal prioritizes recent high-signal posts", () => {
  const scored = rankBySignal(TWEETS, { nowMs: FIXED_NOW });
  assert.ok(scored.length >= 2);
  assert.ok((scored[0] as ScoredTweet).signalScore >= (scored[1] as ScoredTweet).signalScore);
  assert.ok(Array.isArray((scored[0] as ScoredTweet).signalReasons));
  assert.ok((scored[0] as ScoredTweet).signalReasons.length > 0);
});

test("rankBySignal respects minScore threshold", () => {
  const scored = rankBySignal(TWEETS, { nowMs: FIXED_NOW, minScore: 200 });
  assert.ok(scored.every((row) => (row as ScoredTweet).signalScore >= 200));
});
