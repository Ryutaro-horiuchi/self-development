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
- Accept an optional numeric argument from 1 to 6 to set the largest heading level in the output (for example, `/transcript-to-markdown 2` uses `##` headings). If no valid number is supplied, default to level 2 (`##`). Use deeper heading levels for subsections as needed, and do not use a shallower level than the requested one.
- Organize the body primarily as concise bullet points, grouping related points under clear headings when useful. Use short prose paragraphs only when they make the summary easier to follow; avoid turning every sentence into a bullet or forcing a fixed template.
- Preserve examples when they clarify an idea, but shorten them without changing their point. Omit timestamps unless the user asks for them or they are needed to locate material.
- If the source is incomplete or ambiguous, summarize only what can be established from the supplied text instead of guessing.
