import test from "node:test";
import assert from "node:assert/strict";
import { mergeThreadTweets, parseSince, type Tweet } from "../lib/api";

const ROOT: Tweet = {
  id: "1",
  text: "root",
  author_id: "u1",
  username: "alice",
  name: "Alice",
  created_at: "2026-02-10T00:00:00.000Z",
  conversation_id: "1",
  metrics: {
    likes: 10,
    retweets: 1,
    replies: 3,
    quotes: 0,
    impressions: 100,
    bookmarks: 0,
  },
  urls: [],
  mentions: [],
  hashtags: [],
  tweet_url: "https://x.com/alice/status/1",
};

const REPLY_A: Tweet = {
  ...ROOT,
  id: "2",
  text: "reply-a",
  created_at: "2026-02-10T00:05:00.000Z",
  tweet_url: "https://x.com/alice/status/2",
};

const REPLY_B: Tweet = {
  ...ROOT,
  id: "3",
  text: "reply-b",
  created_at: "2026-02-10T00:02:00.000Z",
  tweet_url: "https://x.com/alice/status/3",
};

test("parseSince handles shorthand relative timestamps", () => {
  const now = Date.parse("2026-02-10T01:00:00.000Z");
  assert.equal(parseSince("30m", now), "2026-02-10T00:30:00.000Z");
  assert.equal(parseSince("2h", now), "2026-02-09T23:00:00.000Z");
  assert.equal(parseSince("1d", now), "2026-02-09T01:00:00.000Z");
});

test("parseSince returns null for invalid date values", () => {
  assert.equal(parseSince("banana"), null);
  assert.equal(parseSince("2026-99-01"), null);
});

test("mergeThreadTweets keeps root once and sorts chronologically", () => {
  const merged = mergeThreadTweets(ROOT, [REPLY_A, ROOT, REPLY_B]);

  assert.deepEqual(
    merged.map((t) => t.id),
    ["1", "3", "2"]
  );
});
