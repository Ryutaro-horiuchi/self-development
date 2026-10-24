---
name: transcript-to-markdown
description: Summarize supplied transcripts or spoken notes as concise, faithful Markdown, especially Japanese lecture and explainer transcripts.
---

### Purpose

Turn a user-provided transcript or spoken-note text into a clear Markdown summary that preserves its main ideas and important examples.

### Instructions

- Treat the supplied transcript as the source of truth. Do not add facts, explanations, or conclusions that are not supported by it.
- Identify the central topic, key claims, definitions, distinctions, and examples. Remove repetition, filler, and conversational transitions while preserving meaningful nuance.
- Write in the transcript's language unless the user requests another language. For Japanese, use concise, natural prose and familiar terminology.
- Return the summary directly as Markdown. Do not add a preamble or closing note unless requested.
- Use `###` for the largest heading in the output. Do not use `#` or `##`; use `####` for subsections when useful. A title can be the first `###` heading.
- Keep the structure proportional to the source: use a short introduction and a small number of sections or bullets only when they make the ideas easier to scan. Avoid forcing every transcript into a fixed template.
- Preserve examples when they clarify an idea, but shorten them without changing their point. Omit timestamps unless the user asks for them or they are needed to locate material.
- If the source is incomplete or ambiguous, summarize only what can be established from the supplied text instead of guessing.
