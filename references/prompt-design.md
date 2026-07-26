# Prompt design

Use separate versioned prompts for unified video understanding, repair, and recommendation reranking. The bundled prompts live in `references/prompts/`.

Every prompt must state that this is pause-time semantic video search, not generic summarization. Require visible evidence, prohibit identity guesses, and require strict JSON matching the supplied schema.

For entry videos, choose boundaries around changes in people, scene, action, object state, dialogue/topic, result, or likely exploration intent. Do not mechanically divide time. Prefer one to four meaningful windows and avoid tiny fragments.

For result videos, use the filename as a high-weight clue while verifying it against the storyboard. Do not simply copy the filename when visual evidence conflicts.

For reranking, provide source context, candidate labels, neighboring entry context, and already selected directions. Require one highly relevant primary and two meaningfully different alternatives. If three reasonable targets do not exist, report the shortage instead of fabricating one.

Increment `prompt_version` after behavioral changes so cache keys and audit records remain trustworthy.
