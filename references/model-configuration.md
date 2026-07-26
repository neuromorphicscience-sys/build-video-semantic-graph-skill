# Model configuration and privacy

Configure the multimodal provider through process environment variables:

```text
CROSSFRAME_VLM_PROVIDER=volcengine_ark
CROSSFRAME_VLM_MODEL=<vision-capable-model-id>
CROSSFRAME_VLM_API_KEY=<secret>
CROSSFRAME_VLM_BASE_URL=<OpenAI-compatible-base-url>
```

`ARK_API_KEY` remains a legacy environment-only alias. Prefer `CROSSFRAME_VLM_API_KEY`.

The bundled production adapter uses an OpenAI-compatible Responses/Files interface and timestamped storyboard images. Confirm that the chosen endpoint accepts image inputs and strict JSON instructions. Never place secrets in `.env` files that will be packaged, prompt files, command output, request summaries, or model caches.

When no API key is configured, inventory and extraction remain available. The runner must stop before creating semantic labels for uncached videos. It must not infer visual labels from filenames alone.

ASR is optional. If a separate transcription provider is introduced, configure it only through `CROSSFRAME_ASR_PROVIDER`, `CROSSFRAME_ASR_MODEL`, `CROSSFRAME_ASR_API_KEY`, and `CROSSFRAME_ASR_BASE_URL`. Mark missing transcripts for review rather than inventing dialogue.

Before public distribution, exclude these paths:

```text
work/model_requests/
work/model_responses/
work/model_cache/
work/ark_files/
work/audio/
work/transcripts/
```
