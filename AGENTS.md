# AGENTS Guide

This file defines practical working rules for coding agents in this repository.

## Project Snapshot

- Name: `biomedical-fastapi-app`
- Stack: Python 3.11+, FastAPI, Plotly, Pandas, Jinja2
- Package root: `src/biomed_api`
- Test suite: `tests/`
- Key runtime directories:
- `data/` for uploaded CSV (`data/data.csv`)
- `output/images/` for generated charts
- `output/insights/` for generated insights artifacts

## Setup and Run

```bash
uv sync
uv run uvicorn biomed_api.main:app --reload
```

Common checks:

```bash
uv run pytest
uv run ruff check .
uv run ruff format .
```

## Code Map

- App bootstrap/lifespan: `src/biomed_api/main.py`
- API routes: `src/biomed_api/api/routes.py`
- Services: `src/biomed_api/services/`
- Schemas: `src/biomed_api/models/schemas.py`
- Templates: `src/biomed_api/templates/`

## Output Lifecycle (Important)

On API startup, transient outputs are intentionally reset by the app lifecycle:

- `output/images/` is emptied
- `output/insights/` is emptied
- `output/report.md` is removed
- `output/RESPONSE_TO_OBJECTIVES.md` is removed

Do not treat those files as durable state.

## Environment Variables

- OpenRouter is used for LLM-backed generation endpoints.
- Set `OPENROUTER_API_KEY` for response-to-objectives generation.
- Core upload/summary/chart/report/insight routes should work without API keys.

## Agent Working Rules

- Keep changes minimal and scoped to the user request.
- Preserve existing module boundaries (routes call services; services hold business logic).
- Prefer adding or updating tests in `tests/` for behavior changes.
- Avoid committing generated artifacts in `output/` unless explicitly requested.
- Do not introduce secrets into code, tests, or fixtures.
- Keep lint and tests passing for touched behavior.

## Editing Conventions

- Follow Ruff line length (`100`) and Python 3.11 compatibility.
- Use explicit, readable function names; avoid ambiguous abbreviations.
- Add comments only where logic is non-obvious.
- Keep API responses and schema fields consistent with existing route patterns.

## Recommended Change Workflow

1. Read impacted route/service/test files.
2. Implement focused code changes.
3. Run targeted tests first, then broader suite if needed.
4. Run `ruff check` (and format if required).
5. Summarize behavioral changes and any residual risks.
