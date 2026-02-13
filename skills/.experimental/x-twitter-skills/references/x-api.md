# X API Reference

## Auth

Use Bearer auth with `X_BEARER_TOKEN`.

```bash
-H "Authorization: Bearer $X_BEARER_TOKEN"
```

## Endpoints Used

### Recent Search (last 7 days)

```text
GET https://api.x.com/2/tweets/search/recent
```

### Full-Archive Search (all time)

```text
GET https://api.x.com/2/tweets/search/all
```

This skill uses full-archive when CLI flag `--archive` is passed.

### Profile Lookup

```text
GET https://api.x.com/2/users/by/username/{username}
```

### Single Tweet Lookup

```text
GET https://api.x.com/2/tweets/{id}
```

## Core Query Params

```text
tweet.fields=created_at,public_metrics,author_id,conversation_id,entities
expansions=author_id
user.fields=username,name,public_metrics
max_results=100
```

Optional params:

- `sort_order=relevancy|recency`
- `start_time=<ISO-8601>`
- `pagination_token=<token>`

## Useful Search Operators

- `from:username`
- `to:username`
- `lang:en`
- `-is:retweet`
- `-is:reply`
- `has:links`
- `url:github.com`
- `conversation_id:<tweet_id>`

Notes:

- `OR` must be uppercase.
- `min_likes` / `min_retweets` are not native operators. Filter post-hoc.

## Response Shape (Simplified)

```json
{
  "data": [{
    "id": "...",
    "text": "...",
    "author_id": "...",
    "created_at": "...",
    "conversation_id": "...",
    "public_metrics": {
      "like_count": 0,
      "retweet_count": 0,
      "reply_count": 0,
      "quote_count": 0,
      "bookmark_count": 0,
      "impression_count": 0
    },
    "entities": {
      "urls": [{"expanded_url": "https://..."}],
      "mentions": [{"username": "..."}],
      "hashtags": [{"tag": "..."}]
    }
  }],
  "includes": {
    "users": [{"id": "...", "username": "...", "name": "..."}]
  },
  "meta": {
    "next_token": "...",
    "result_count": 100
  }
}
```

## Tweet URL Construction

```text
https://x.com/{username}/status/{tweet_id}
```

## Rate Limiting and Cost

If a 429 occurs, read `x-rate-limit-reset` and retry after that epoch time.

Costs and limits can change. Check official docs before assuming specific prices:

- [X API docs](https://docs.x.com/x-api)
- [Developer console](https://console.x.com)
