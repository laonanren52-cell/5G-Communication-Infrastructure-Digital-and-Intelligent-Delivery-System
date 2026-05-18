# AGENTS.md

## Project Goal

This project is a Python Streamlit demo for the competition direction "Track 4: automatic conversion from design deliverables to construction instructions".

The main demo flow is:

Design metadata Excel/CSV -> data validation -> lightweight design review -> BOM estimation -> construction task/report generation -> preview -> Word/Excel download.

The system is a communication infrastructure delivery prototype, not a production system. The focus is demonstrating how structured base-station design metadata can be converted into construction BOMs, process guidance, fiber allocation, quality acceptance items, and delivery reports.

## Tech Stack

- Python
- Streamlit
- Pandas
- openpyxl
- Standard library HTTP calls through `urllib.request` for OpenAI-compatible Chat Completions
- No database
- No QGIS integration
- No new UI framework unless explicitly requested

## Important Structure

```text
.
├── app.py
├── README.md
├── CHANGELOG.md
├── requirements.txt
├── .gitignore
├── docs/
│   ├── handoff.md
│   └── task-log.md
└── taste-skill-beta-v2/      # user/system-provided reference material; do not commit unless explicitly requested
```

Runtime cache:

```text
.design_file_cache/
```

This folder stores the recent 10 uploaded design files and is ignored by Git.

## Run Command

```powershell
cd C:\Users\cheng\Documents\Codex\2026-05-08\python-python-streamlit-5g-demo-web
.\.venv\Scripts\streamlit.exe run app.py --server.port 8501 --server.address 127.0.0.1
```

Then open:

```text
http://127.0.0.1:8501
```

## Test / Check Commands

Preferred syntax check when the project venv works:

```powershell
.\.venv\Scripts\python.exe -m py_compile app.py
```

Fallback syntax check used in the latest session because the project venv launcher sometimes points to a missing Python:

```powershell
& "C:\Users\cheng\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m py_compile app.py
```

Local page health check when Streamlit is running:

```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8501 -UseBasicParsing | Select-Object -ExpandProperty StatusCode
```

Expected status: `200`.

## Do Not Modify Casually

- Do not remove the existing Track 4 main flow.
- Do not rewrite the app into a multi-page architecture.
- Do not replace Streamlit with React, Next.js, Flask, Django, or other frameworks.
- Do not introduce a database.
- Do not force QGIS integration.
- Do not remove local Mock mode; the demo must run without an API key.
- Do not remove Word/Excel download behavior.
- Do not commit `taste-skill-beta-v2/` or `.design_file_cache/` unless explicitly requested.
- Do not reset or overwrite unrelated user changes.
- Do not continue broad UI redesign unless explicitly requested; use small, targeted fixes.

## Files Future Codex Must Read First

1. `docs/handoff.md`
2. `docs/task-log.md`
3. `AGENTS.md`
4. `README.md`
5. `app.py` only after reading the handoff and task log

## Required End-of-Turn Maintenance

At the end of every future Codex task in this project:

- Update `docs/handoff.md` with the latest state, blockers, and next minimal task.
- Update `docs/task-log.md` with the key actions, files changed, commands run, successes, failures, and pending items.
- Update `CHANGELOG.md` for every project-facing change, including feature, documentation, generated artifact, verification, and GitHub sync changes.
- After verification passes, commit the scoped project changes and push them to the GitHub repository unless the user explicitly asks not to push.
- Keep updates concise and factual.
