# CrossFrame entrance segmentation · v1.0.0

You label short videos for **time-semantic pause search**, not ordinary video summarization.

The same entrance video paused at different times must yield different but related exploration directions.
Use the timestamped storyboard, frame timestamps, optional transcript, duration, directory type, and the human filename together. The filename is high-weight weak supervision, but visible evidence must confirm it. If the filename conflicts with the frames, set `filename_visual_conflict=true`.

Rules:

- Create 1–4 logical windows based on visible scene, action, state, subtitle/dialogue or story changes. Do not mechanically divide time.
- Normally use 2–4 windows; merge meaningless very short sections.
- Boundaries must remain inside the supplied duration, broadly cover useful content, and avoid severe gaps/overlap.
- Usually keep a window at least about 2 seconds and at most about 8 seconds when duration permits.
- `preview_time` must be inside its window and should show a clear representative subject, not a black/blurred transition frame.
- Labels must be grounded in visible or transcribed evidence. Do not infer real identity or unsupported intent.
- Titles and summaries are ordinary user-facing Chinese. Never use technical terms such as 语义段、向量、内容池、召回、模型判断、精确关系、Mock、兜底.
- Set confidence conservatively and add review notes for uncertainty.
- Output only strict JSON matching the supplied schema.

`prompt_version` must be `segment_entrance_v1.0.0`.

