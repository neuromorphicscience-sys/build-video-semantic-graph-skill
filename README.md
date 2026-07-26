# Build Video Semantic Graph Skill

[中文说明](README.zh-CN.md)

An open-source Codex/agent skill for turning local short-video collections into a **timestamp-aware semantic search graph**.

It inventories source media, extracts timestamped storyboards, calls a configured multimodal model for structured video understanding, recalls and reranks related clips, validates every reference, exports a human-review workbook, and only then applies generated JSON with automatic backup.

> Built from the production workflow behind **CrossFrame — “pause to search, search to continue the story.”**

## Why this skill exists

Traditional video recommendation works at the video level. Visual search needs to understand **what is happening at the exact moment a user pauses**.

This skill converts raw entry/result video folders into:

- timestamp-aware entry segments;
- structured visual semantics for people, objects, actions, scenes, and event states;
- recommendation edges from each pause-time segment to related result videos;
- auditable model outputs and validation reports;
- runtime-ready `videos.json`, `segments.json`, and `relations.json`.

## Core pipeline

```text
Local videos
  → inventory and codec checks
  → timestamped storyboard extraction
  → multimodal model analysis
  → entry-video semantic segmentation
  → result-video labeling
  → candidate recall
  → model reranking and diversity control
  → graph validation
  → review workbook
  → explicit backup-and-apply
```

## What is actually implemented

The current implementation uses:

1. **Timestamped storyboard extraction** from local videos.
2. **A configurable vision-capable multimodal model** through an OpenAI-compatible API.
3. **Strict structured outputs** for entry segmentation and result labeling.
4. **Text/semantic candidate recall** followed by model reranking.
5. **Graph-level validation** for timing, references, diversity, copyright state, and runtime files.
6. **Human review before apply**, with timestamped backups.

The project does **not** claim that a vector database or multimodal embedding model is mandatory. Those can be added as a scale-out retrieval layer, while this skill already provides the segment schema, validation contracts, and reranking workflow required by such a system.

## Proven reference scale

The CrossFrame case study processed:

- 33 local videos;
- 15 entry videos and 18 result videos;
- 100 timestamp-aware semantic segments;
- a validated multi-round recommendation graph.

The media, model responses, credentials, and project-specific runtime JSON are intentionally not included.

## Repository structure

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── crossframe-case-study.md
│   ├── data-contracts.md
│   ├── model-configuration.md
│   ├── prompt-design.md
│   ├── validation-rules.md
│   └── prompts/
├── scripts/
│   ├── run_pipeline.py
│   ├── extract_video_features.py
│   ├── analyze_videos_with_model.py
│   ├── build_recommendation_graph.py
│   ├── validate_generated_data.py
│   ├── export_review_workbook.py
│   └── requirements.txt
└── dist/
    └── build-video-semantic-graph.skill
```

## Requirements

- Python 3.10+
- `ffmpeg` and `ffprobe` on `PATH`
- A vision-capable multimodal model endpoint for the analysis phase

Install Python dependencies:

```bash
python -m pip install -r scripts/requirements.txt
```

## Expected project layout

The target video project should contain:

```text
project/
├── raw/入口/                 # or raw/entry/
├── raw/结果/                 # or raw/result/
├── backend/app/data/
├── frontend/public/media/videos/
├── data/generated/
├── reports/autolabel/
└── work/
```

Source videos under `raw/` are treated as immutable.

## Model configuration

Set credentials through process environment variables only:

```bash
export CROSSFRAME_VLM_PROVIDER=volcengine_ark
export CROSSFRAME_VLM_MODEL=<vision-capable-model-id>
export CROSSFRAME_VLM_API_KEY=<secret>
export CROSSFRAME_VLM_BASE_URL=<openai-compatible-base-url>
```

`ARK_API_KEY` is supported only as a legacy environment alias.

Never commit credentials, `.env` files containing secrets, model request/response caches, extracted audio, or transcripts.

## Quick start

Run a safe dry run first:

```bash
python scripts/run_pipeline.py \
  --project-root /path/to/project \
  --dry-run
```

Run the full pipeline:

```bash
python scripts/run_pipeline.py \
  --project-root /path/to/project \
  --mode all
```

Validate and require three distinct recommendations per source segment:

```bash
python scripts/run_pipeline.py \
  --project-root /path/to/project \
  --mode validate \
  --require-three-results
```

Apply generated data only after review:

```bash
python scripts/run_pipeline.py \
  --project-root /path/to/project \
  --mode validate \
  --require-three-results \
  --apply
```

The apply step creates a timestamped backup before replacing formal runtime JSON.

## Available modes

| Mode | Purpose |
|---|---|
| `inventory` | Inventory videos and detect decode/codec problems |
| `extract` | Extract timestamped frames, storyboards, and optional audio |
| `analyze` | Analyze one or more videos with the configured multimodal model |
| `relations` | Build candidate recall and recommendation edges |
| `validate` | Validate timing, references, diversity, media files, and text |
| `report` | Generate model-call and data-quality reports |
| `export` | Export the human-review workbook |
| `all` | Run the complete workflow |

Useful options include `--video`, `--sample`, `--force`, `--workers`, `--dry-run`, and `--apply`.

## Safety principles

- Never modify files below `raw/`.
- Never fabricate visual labels from filenames alone.
- Treat filenames only as weak supervision.
- Stop safely if uncached videos require a model and no API key is configured.
- Keep model evidence and caches outside public repositories.
- Block apply on invalid timing, missing references, duplicate IDs, missing media, or unusable copyright status.
- Require human review for low confidence and ambiguous visual evidence.

## Self-check

```bash
python scripts/self_check.py
```

Expected output:

```text
Skill self-check: PASS
```

## Using the packaged skill

A ready-to-install package is available at:

```text
dist/build-video-semantic-graph.skill
```

The source tree is the canonical version for review and contribution.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please do not submit copyrighted media, credentials, private model responses, or project-specific generated datasets.

## License

MIT License. See [LICENSE](LICENSE).
