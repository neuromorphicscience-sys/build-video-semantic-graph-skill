# CrossFrame recommendation reranking · v1.0.0

Rerank result videos for one entrance time-semantic window.

This is pause-time video exploration, not generic similarity. Use the source window, its previous/next context and each candidate's filename-backed but visually verified labels.

Select exactly three distinct result nodes:

1. `main_result`: most directly and naturally related to the paused moment.
2. `alternative_1`: a different useful direction such as explanation, another view, cause or continuation.
3. `alternative_2`: another distinct direction such as tutorial, similar content, route, product or consequence.

Do not select three videos that repeat the same idea. Never select the entrance video itself unless the candidate is an explicitly legal separate result node. If fewer than three credible candidates exist, do not fabricate IDs.

`reason_internal` is for human review only. `button_title` must be short, natural Chinese. Output only strict JSON matching the supplied schema.

`prompt_version` must be `rerank_results_v1.0.0`.
