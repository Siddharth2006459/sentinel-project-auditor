# SENTINEL

Evidence-linked project review prototype. Upload project materials, inspect gaps and contradictions, review source citations, assign priority ratings, and export reports.

## Run locally

Python 3 is required. From the repository folder:

```sh
python3 serve.py --open
```

Visit http://127.0.0.1:4173/. Keep the terminal open. On macOS, you can also run `Start-SENTINEL.command`.

## Test

Node.js with the built-in test runner is required:

```sh
node --test test.mjs
```

## Demo

Upload only `demo/01_UPLOAD_SENTINEL_TEST.txt` with an empty paste box. The current engine produces 12 candidates. See `demo/VIDEO_RECORDING_GUIDE.md` for a three-minute walkthrough and `demo/EXPECTED_RESULTS.json` for the answer key. The optional revised plan must be tested separately.

## Features

- Eight contextual audit dimensions
- Assumption, constraint, question and contradiction categories
- Exact source-line citations and source viewer
- Placeholder and fixed-label conflict detection
- CSV missing-cell and inconsistent-width profiling
- Reviewer-supplied scoring: round((S * P * D * T) / E)
- Finding filters, review status, Markdown and JSON export

## Architecture

Static HTML/CSS and native JavaScript modules. `dist/app.mjs` manages input and the interface; `dist/engine.mjs` contains analysis, scoring and export functions. `serve.py` serves only app assets on loopback. No dependencies, backend API, database or model credentials are required.

## Scope and limitations

This release uses deterministic rules, not an LLM. It can miss semantic gaps and produce false positives. Missing wording is a review candidate, not proof that a control does not exist. Scores require reviewer judgments. The tool does not establish compliance, correctness, completeness or release readiness.

Supports UTF-8 TXT, MD, CSV and JSON-as-text, capped at 1 MB total. PDF, Word documents, images and graphical workflows require text conversion. CSV checks are structural only. JSON input is not schema-validated.

Project materials remain in browser memory and are cleared on reload. Export before leaving; JSON exports include original sources. The app does not send project materials to a backend.

## Static deployment

Publish the contents of `dist/` with a static host; no build step is needed. Serve `.mjs` files as JavaScript.
