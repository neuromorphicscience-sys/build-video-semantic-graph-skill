# Source package

The complete executable source is stored in `dist/build-video-semantic-graph.skill`.

The `.skill` extension identifies an installable agent-skill bundle; the file itself is a standard ZIP archive. It contains:

```text
SKILL.md
agents/
references/
scripts/
```

No source is compiled, minified, encrypted, or obfuscated.

## Extract

```bash
python tools/unpack_skill.py --output unpacked
```

## Verify integrity

```text
SHA-256: 45defd220e6ebfae001fefffe991137227561ff7bed27bfd996a1174bd3566f8
```

The root-level `SKILL.md`, `agents/`, and `references/` are also exposed separately for convenient review. The packaged copy is the distribution artifact used by agent clients.
