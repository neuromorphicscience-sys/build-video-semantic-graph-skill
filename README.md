# Build Video Semantic Graph Skill

[中文说明](README.zh-CN.md)

An open-source Codex/agent skill for turning local short-video collections into a **timestamp-aware semantic search graph**.

It inventories media, extracts timestamped storyboards, calls a configured multimodal model for structured video understanding, creates entry-video semantic windows, labels result videos, recalls and reranks candidates, validates the graph, exports a human-review workbook, and applies generated JSON only after explicit approval and backup.

> Built from the production workflow behind **CrossFrame — “pause to search, search to continue the story.”**

## What the skill produces

- timestamp-aware entry segments;
- structured people, object, action, scene, and event-state semantics;
- recommendation edges from pause-time segments to related result videos;
- model-call and data-quality reports;
- a human-review workbook;
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

## Honest technical scope

The current implementation uses:

1. timestamped storyboard extraction from local videos;
2. a configurable vision-capable multimodal model through an OpenAI-compatible API;
3. strict structured outputs for entry segmentation and result labeling;
4. text/semantic candidate recall followed by model reranking;
5. graph-level validation for timing, references, diversity, copyright status, and runtime media;
6. human review before apply, with timestamped backups.

It does **not** claim that a vector database or multimodal embedding model is already mandatory. At platform scale, a multimodal embedding service can be added as the first-stage retrieval layer while retaining this skill's segment schema, validation contracts, and reranking workflow.

## Proven reference scale

The CrossFrame case study processed:

- 33 local videos;
- 15 entry videos and 18 result videos;
- 100 timestamp-aware semantic segments;
- a validated multi-round recommendation graph.

Media, credentials, private model responses, and project-specific production JSON are intentionally excluded.

## Distribution format

The complete executable source is distributed as:

```text
dist/build-video-semantic-graph.skill
```

A `.skill` file is a ZIP-compatible source package containing `SKILL.md`, `agents/`, `references/`, and the full `scripts/` directory. Nothing is obfuscated or compiled.

Package SHA-256:

```text
45defd220e6ebfae001fefffe991137227561ff7bed27bfd996a1174bd3566f8
```

Extract it with Python:

```bash
python tools/unpack_skill.py --output unpacked
```

Or with any ZIP utility after copying/renaming the file to `.zip`.

## Repository structure

```text
.
├── SKILL.md
├── agents/openai.yaml
├── references/
├── dist/build-video-semantic-graph.skill
├── tools/unpack_skill.py
├── SOURCE.md
├── README.md
├── README.zh-CN.md
├── LICENSE
├── CONTRIBUTING.md
└── SECURITY.md
```

After extraction, the full runnable tree additionally contains `scripts/`.

## Requirements

- Python 3.10+
- `ffmpeg` and `ffprobe` available on `PATH`
- a vision-capable multimodal model endpoint for the analysis phase

Extract and install dependencies:

```bash
python tools/unpack_skill.py --output unpacked
python -m pip install -r unpacked/scripts/requirements.txt
```

## Expected target-project layout

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

Source videos under `raw/` are immutable.

## Model configuration

Set credentials through process environment variables only:

```bash
export CROSSFRAME_VLM_PROVIDER=volcengine_ark
export CROSSFRAME_VLM_MODEL=<vision-capable-model-id>
export CROSSFRAME_VLM_API_KEY=<secret>
export CROSSFRAME_VLM_BASE_URL=<openai-compatible-base-url>
```

Never commit credentials, secret-bearing `.env` files, private model request/response caches, extracted audio, or transcripts.

## Quick start

Safe dry run:

```bash
python unpacked/scripts/run_pipeline.py \
  --project-root /path/to/project \
  --dry-run
```

Full pipeline:

```bash
python unpacked/scripts/run_pipeline.py \
  --project-root /path/to/project \
  --mode all
```

Validate three distinct recommendations per source segment:

```bash
python unpacked/scripts/run_pipeline.py \
  --project-root /path/to/project \
  --mode validate \
  --require-three-results
```

Apply generated data only after review:

```bash
python unpacked/scripts/run_pipeline.py \
  --project-root /path/to/project \
  --mode validate \
  --require-three-results \
  --apply
```

The apply step creates a timestamped backup before replacing formal runtime JSON.

## Safety principles

- Never modify files below `raw/`.
- Never fabricate visual labels from filenames alone.
- Treat filenames only as weak supervision.
- Stop safely when uncached videos require a model and no API key is configured.
- Keep model evidence and caches outside public repositories.
- Block apply on invalid timing, missing references, duplicate IDs, missing media, or unusable copyright status.
- Require human review for low confidence and ambiguous evidence.

## Self-check

```bash
python unpacked/scripts/self_check.py
```

Expected output:

```text
Skill self-check: PASS
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Do not submit copyrighted media, credentials, private model responses, or project-specific generated datasets.

## License

MIT License. See [LICENSE](LICENSE).
