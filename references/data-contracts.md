# Data contracts

## Video asset

Each video record needs a stable `video_id`, user-facing title and summary, `video_type`, duration, playback URL, preview time, analysis status, copyright status, and confidence. Use `/media/videos/{safe_filename}` locally or an HTTPS asset URL in production.

## Entry semantic segment

Each entry segment needs a unique `segment_id`, parent `video_id`, ordered index, `start`, `end`, stage, user-facing summary/title, tags, preview time, and confidence.

Require `0 <= start < end <= video.duration`. Select segment matches with `start <= current_time < end`; use the nearest segment only at uncovered boundaries.

## Result node

Represent a simple result video as one result node. Split it only when distinct events can be entered independently. Keep every preview/start time within the valid media range.

## Recommendation edge

Each source entry segment should resolve to one primary and two alternatives with distinct target nodes. Store internal reasoning for audit, but do not expose it automatically in the H5. Preserve target start and preview times.

## Generated versus formal data

Write drafts to:

```text
backend/app/data/videos.generated.json
backend/app/data/segments.generated.json
backend/app/data/relations.generated.json
```

Only explicit validated apply may replace `videos.json`, `segments.json`, and `relations.json`.
