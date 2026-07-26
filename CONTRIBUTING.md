# Contributing

Contributions are welcome for provider adapters, schema validation, retrieval/reranking methods, reporting, and documentation.

## Before opening a pull request

1. Run `python -m compileall -q scripts`.
2. Run `python scripts/self_check.py`.
3. Keep changes backward-compatible with the documented data contracts, or explain schema migrations explicitly.
4. Add or update validation rules when introducing a new output field.
5. Keep user-facing text free of internal implementation terminology.

## Do not submit

- copyrighted or private video files;
- API keys, tokens, `.env` files, or certificates;
- raw model requests/responses or caches;
- extracted audio or private transcripts;
- CrossFrame production JSON or other project-specific datasets.

## Design principles

- source media is immutable;
- model output is an auditable draft;
- filenames are weak supervision only;
- validation and human review precede apply;
- failed records should be isolated rather than corrupting a whole batch.
