---
name: wasm-meeting-notes
description: Convert raw meeting transcripts (Google Meet or Zoom) into comprehensive meeting minutes in the WebAssembly community group style using an interactive pipeline.
---

# Wasm Meeting Notes

## Overview

This skill provides an interactive pipeline to process raw meeting transcripts into structured meeting notes (minutes) following the standards of the WebAssembly community groups. The pipeline supports transcripts from both **Google Meet** (Markdown/Docs export) and **Zoom** (WebVTT / VTT / text). The process is broken into distinct steps, allowing for human review and correction at each stage to ensure data integrity and accurate attribution.

## Required Setup

Ensure that the Python processing scripts in `scripts/` are available.

The pipeline is **model-agnostic and LLM vendor-neutral**. You can use any LLM provider (OpenAI, Google Gemini, Anthropic Claude, Groq, Ollama, OpenRouter, DeepSeek, LocalAI, vLLM, etc.) by configuring the appropriate environment variable:

- **OpenAI / OpenAI-compatible:**
  ```bash
  export OPENAI_API_KEY="sk-..."
  # Optional custom endpoint (e.g. Ollama, OpenRouter, Groq, local server):
  # export OPENAI_BASE_URL="http://localhost:11434/v1"
  # export OPENAI_MODEL="gpt-4o-mini"
  ```
- **Google Gemini:**
  ```bash
  export GEMINI_API_KEY="AIza..."
  # Optional: export GEMINI_MODEL="gemini-2.5-flash"
  ```
- **Anthropic Claude:**
  ```bash
  export ANTHROPIC_API_KEY="sk-ant-..."
  # Optional: export ANTHROPIC_MODEL="claude-3-5-haiku-20241022"
  ```
- **Generic LLM Configuration:**
  ```bash
  export LLM_API_KEY="..."
  export LLM_BASE_URL="https://api.example.com/v1"
  export LLM_MODEL="..."
  # export LLM_PROVIDER="openai" # "openai", "gemini", or "anthropic"
  ```

## Workflow

Follow these steps strictly in order, pausing after each script execution to ask the user to review the output file and confirm it is acceptable before proceeding.

### 1. Structural Cleanup

This step processes raw transcripts from Google Meet (Markdown/Docs) or Zoom (WebVTT/VTT/plain text), strips headers and timestamps, extracts unique speaker initials, and isolates dialogue turns.

- **Run:** `python3 scripts/process_transcript.py <input_transcript> 01_processed.txt`
- **Review:** Ask the user to review `01_processed.txt` and confirm there are no missing speakers or formatting errors.

### 2. Untangling Interleaved Speech

This step uses the configured LLM to logically reorder and merge sentences that were interrupted or spoken in fragments, ensuring complete thoughts are grouped together. It also removes lines containing nothing but meaningless filler words.

- **Run:** `python3 scripts/reorder_transcript.py 01_processed.txt 02_reordered.txt`
- **Review:** The script will log to the console any lines that were dropped (identified as filler). Ask the user to review these logs and the contents of `02_reordered.txt` to ensure no meaningful dialogue was lost.

### 3. Language Cleanup

This step uses the configured LLM line-by-line to surgically fix grammar, remove internal false starts, and clear out verbal tics (ums, uhs) while strictly maintaining the technical meaning and original sentence structure.

- **Run:** `python3 scripts/clean_transcript.py 02_reordered.txt 03_cleaned.txt`
- **Review:** Ask the user to review `03_cleaned.txt` to verify the language reads cleanly without losing technical nuance.

### 4. Final Formatting

Once `03_cleaned.txt` is approved:
1. **Identify Attendees:** Extract the full names of all participants from the original transcript to populate the `### Attendees` list as a bulleted list of full names.
2. **Map Agenda:** Cross-reference the dialogue with the meeting agenda to structure the notes with appropriate markdown headers (e.g. `#### [Agenda Topic]`). Preserve issue links (e.g. `[#102](...)`) if mentioned.
3. **Draft Minutes:** Move the cleaned statements from `03_cleaned.txt` under their corresponding section headers. Use the boilerplate in [assets/template.md](assets/template.md) if starting from a blank meeting file.

## Guidelines

- **Attribute everything**: Every bullet point must start with speaker initials.
- **Maintain detail**: Do not summarize away technical nuances. If a tradeoff is discussed, capture all sides.
- **Strict Adherence:** Do not skip review steps. The user must explicitly approve intermediate text files (`01_processed.txt`, `02_reordered.txt`, `03_cleaned.txt`).
