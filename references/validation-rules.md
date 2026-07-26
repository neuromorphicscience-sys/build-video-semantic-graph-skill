# Validation rules

Block apply when any of these checks fail:

- Duplicate or empty video, segment, or edge IDs.
- Entry segment boundaries are negative, reversed, or outside video duration.
- Preview/start times fall outside their video or segment.
- Entry coverage has serious gaps or overlaps.
- A relation references a missing source segment or target video.
- An entry segment has no primary recommendation.
- Primary and alternatives repeat the same target node.
- A local `/media/videos/` URL has no corresponding file.
- A generated record lacks validated model output when model analysis is required.
- Copyright status is missing, pending, or unusable for formal media.
- User-visible text contains internal implementation terminology.

Warn and require human review for low confidence, filename/visual conflict, missing transcript when speech is material, possible black preview frames, only one entry segment, or insufficient recommendation diversity.

Run validation before exporting a review workbook and immediately before apply. Never downgrade an error merely to make apply pass.
