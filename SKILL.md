---
name: build-video-semantic-graph
description: Build a timestamp-aware semantic-search graph from local short-video folders by inventorying media, extracting timestamped storyboards, calling a configured multimodal model for structured entry-video segmentation and result-video labeling, recalling and reranking diverse recommendations, validating references, exporting review artifacts, and safely applying generated JSON. Use when Codex needs to turn entry/result video collections into pause-time search data, rerun one video, rebuild relations, audit generated graph data, or prepare data for a video-search H5 without modifying source media.
---

# Build Video Semantic Graph

Turn short-video folders into validated time-semantic search data. Preserve source media and treat model output as an auditable draft until validation and human review succeed.

## Start safely

1. Resolve the target project root explicitly.
2. Read [model-configuration.md](references/model-configuration.md) before any model call.
3. Read [data-contracts.md](references/data-contracts.md) before changing schemas or integrating another frontend/backend.
4. Run a dry run first:

```powershell
python scripts/run_pipeline.py --project-root D:\path\to\project --dry-run
```

5. Never modify files below `raw/` and never read credentials from project files.

## Expected project layout

Accept either Chinese or English source buckets:

```text
project/
├── raw/入口/       # or raw/entry/
├── raw/结果/       # or raw/result/
├── backend/app/data/
├── frontend/public/media/videos/
├── data/generated/
├── reports/autolabel/
└── work/
```

Treat filenames as high-weight weak supervision, not as proof of visual content. Keep generated files separate from formal runtime JSON until explicit apply.

## Choose the smallest workflow

- Inventory only: `--mode inventory`
- Extract frames/storyboards/audio only: `--mode extract`
- Analyze one changed video: `--mode analyze --video <id-or-filename>`
- Rebuild candidate recall and relations: `--mode relations`
- Validate generated artifacts: `--mode validate`
- Export the review workbook: `--mode export`
- Run the complete pipeline: `--mode all`

Use `--sample` for two entry videos and six result videos. Use `--force` only when intentionally invalidating cached model outputs.

## Run the complete pipeline

From this skill directory, execute:

```powershell
python scripts/run_pipeline.py `
  --project-root D:\path\to\project `
  --mode all
```

The runner sets the project and prompt paths for bundled scripts. It pauses safely when uncached videos require a model but `CROSSFRAME_VLM_API_KEY` is absent. Do not substitute filename-only or random labels.

## Review before apply

1. Inspect `reports/raw_video_inventory.csv` for decode and codec failures.
2. Inspect storyboards and preview frames under `work/`.
3. Inspect model outputs for unsupported claims and low confidence.
4. Read [validation-rules.md](references/validation-rules.md).
5. Run `--mode validate` and require a passing report.
6. Review `data/generated/video_semantic_graph_review.xlsx`.
7. Apply only with explicit authorization:

```powershell
python scripts/run_pipeline.py `
  --project-root D:\path\to\project `
  --mode validate `
  --apply
```

Applying creates a timestamped backup below `backend/app/data/backup/` before replacing formal JSON.

## Preserve evidence and resumability

- Cache calls by model, prompt version, input metadata, and image hashes.
- Keep request summaries and responses below `work/`; exclude them from public repositories.
- Reuse validated cached analysis when inputs are unchanged.
- Record failures per video and continue independent batch work where possible.
- Keep prompt versions with every structured output.

## Extend carefully

Read [prompt-design.md](references/prompt-design.md) before editing prompts. Use the bundled versioned prompts in `references/prompts/`. Keep user-visible titles and summaries free of implementation terms such as vector, recall, model judgment, mock, or fallback.

For a compact example of proven scale and outputs, read [crossframe-case-study.md](references/crossframe-case-study.md). Do not copy its video IDs or relationships into another project.
