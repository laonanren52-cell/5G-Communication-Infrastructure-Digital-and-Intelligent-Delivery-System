# Handoff

## Current Overall Goal

Build and polish a Python Streamlit demo for communication infrastructure delivery:

Design metadata Excel/CSV -> validation -> lightweight intelligent design review -> BOM estimation -> construction/fiber/quality/delivery materials -> Word/Excel export.

The project remains primarily focused on competition Track 4: automatic conversion from design deliverables to construction instructions. A lightweight Track 3-style design review module has been added as a pre-generation check.

## Original Request In This Round

The user asked to add a "lightweight intelligent review result" module before generating construction materials, without changing the existing main flow. Requirements included:

- Field completeness review
- Cable distance review
- Duplicate site ID review
- Fiber core occupancy review
- Power supply construction risk review
- Resource conflict review
- Review summary, statistics, and detail table
- Continue allowing BOM preview when errors exist, but block formal construction material generation
- README update

Follow-up requests added:

- Let users switch between problematic and normal review items
- Add clearer colors for review reminders
- Add fiber allocation table output after intelligent conversion
- Add batch file processing
- Add cache for the latest 10 uploaded files
- Add file-source tracing to review rows for batch uploads
- Split review detail filters into five options: all, error, high risk, reminder, normal

## Completed Features

- Added lightweight intelligent design review functions:
  - `run_design_review(df)`
  - `build_review_summary(review_df, total_rows)`
  - `render_review_result(review_df, summary)`
- Added required review result schema:
  - `check_item`
  - `level`
  - `message`
  - `field`
  - `row_index`
  - `site_id`
  - `suggestion`
- Added review levels:
  - `normal`
  - `info`
  - `warning`
  - `error`
- Added page section titled `轻量智能审查结果`.
- Added review summary metrics and conclusion logic.
- Added review filtering tabs:
  - `需处理项`
  - `正常项`
  - `全部明细`
- Added row-level color styling for risk levels.
- Added flow control:
  - If review has `error`, formal generation is blocked.
  - BOM/report preview can still be viewed with a warning.
- Added standard English review fields to built-in demo data while keeping existing Chinese fields.
- Added `build_fiber_allocation_table(data)` and a `纤芯分配表` tab in intelligent conversion output.
- Added `纤芯分配表` sheet to Excel export.
- Added multi-file upload through Streamlit `accept_multiple_files=True`.
- Added batch processing overview for uploaded files.
- Added recent 10-file cache using `.design_file_cache/`.
- Added `source_file` / `文件来源` to lightweight review detail rows so each issue can be traced to its uploaded drawing/file.
- Added batch review detail aggregation across all uploaded files.
- Replaced the review detail filter tabs with five options:
  - `全部明细`
  - `错误项`
  - `高风险项`
  - `提醒项`
  - `正常项`
- Added `.design_file_cache/` to `.gitignore`.
- Updated `README.md` with Track 3 lightweight review, batch upload, cache, review filtering, and fiber allocation descriptions.

## Modified Files

- `app.py`
  - Added review constants, review functions, render functions, batch/cache helpers, fiber allocation table generation, and page integration.
  - Changed upload control to support multiple files.
  - Added current-file selector for uploaded and cached files.
  - Added batch summary table and recent file cache display.
  - Added batch review detail table with file-source attribution.
  - Changed review detail tabs to all/error/high-risk/reminder/normal filters.
  - Added review gating before formal material generation.
- `README.md`
  - Added documentation for lightweight review, batch upload, cache, filtered review table, and fiber allocation output.
  - Updated version summary through version 12 and added rule-document references.
- `.gitignore`
  - Added `.design_file_cache/`.
- `AGENTS.md`
  - Added long-term project rules for future Codex sessions.
- `docs/handoff.md`
  - Current handoff state.
- `docs/task-log.md`
  - Current task process log.
- `CHANGELOG.md`
  - Added version records for lightweight review, grouped review detail filters, fiber allocation table, batch upload, recent file cache, handoff documents, and rule documents.
  - Added version 12 for batch review file-source tracing, five review filters, rule DOCX output, README updates, and GitHub sync policy.

## Current Blocking / Risk State

The app had a runtime error after the cache feature was first added:

```text
NameError: name 'CACHE_INDEX_FILE' is not defined
```

This was fixed by adding the missing imports and constants:

- `hashlib`
- `datetime`
- `Path`
- `RECENT_FILE_LIMIT`
- `CACHE_DIR`
- `CACHE_INDEX_FILE`

After the fix:

```text
py_compile app.py passed
http://127.0.0.1:8501 returned 200
```

## Known Errors / Key Terminal Lines

Previously observed key runtime error:

```text
NameError: name 'CACHE_INDEX_FILE' is not defined
File "...\app.py", line 1949, in <module>
recent_files = cache_design_files(uploaded_files)
File "...\app.py", line 861, in cache_design_files
return load_recent_file_index()
File "...\app.py", line 841, in load_recent_file_index
if not CACHE_INDEX_FILE.exists():
```

Previously observed environment issue:

```text
Unable to create process using '"C:\Users\cheng\AppData\Local\Programs\Python\Python312\python.exe" ...'
```

Fallback Python was used successfully:

```text
C:\Users\cheng\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe
```

## Unresolved / Not Yet Solved

- No deep browser visual QA was performed after the latest cache/fiber/batch changes.
- The `.venv` Python launcher may still point to a missing Python install in some commands, even though the app was reachable at `127.0.0.1:8501` after the latest fix.
- Git commit/push was not completed in this session.
- `taste-skill-beta-v2/` remains untracked and should not be committed without explicit instruction.

## Minimal Next Task For Next Codex

Do not add new features first. The minimal next task should be:

1. Open the running Streamlit page.
2. Verify the latest review table tabs, batch upload selector, recent file cache display, and fiber allocation tab visually.
3. Fix only visible runtime/UI defects found in those areas.
4. Re-run syntax check and page health check.
5. Update `docs/handoff.md` and `docs/task-log.md`.

## Files To Read First Next Round

1. `AGENTS.md`
2. `docs/handoff.md`
3. `docs/task-log.md`
4. `README.md`
5. Targeted sections of `app.py`

## Files / Directions Not To Touch

- Do not touch `taste-skill-beta-v2/` unless explicitly requested.
- Do not commit `.design_file_cache/`.
- Do not rewrite the single-file Streamlit architecture.
- Do not replace Streamlit.
- Do not remove local Mock mode.
- Do not remove or bypass review gating unless explicitly requested.
- Do not continue broad visual redesign unless the user asks for UI polish.

## Current Commands

Run app:

```powershell
cd C:\Users\cheng\Documents\Codex\2026-05-08\python-python-streamlit-5g-demo-web
.\.venv\Scripts\streamlit.exe run app.py --server.port 8501 --server.address 127.0.0.1
```

Fallback syntax check:

```powershell
& "C:\Users\cheng\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m py_compile app.py
```

Health check:

```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8501 -UseBasicParsing | Select-Object -ExpandProperty StatusCode
```

## Current Test / Runtime State

Latest known checks:

- `py_compile app.py`: passed.
- `http://127.0.0.1:8501`: returned `200`.
- Function-level checks were run earlier for review and fiber allocation generation.
- Browser refresh after the latest review-table change showed the five review filter tabs and no visible runtime exception.
- Function-level batch review check confirmed `source_file` is present and includes uploaded file names.
- Generated two Word rule documents under `docs/`:
  - `程序检查规则.docx`
  - `数据校验规则.docx`
- `py_compile docs/build_rule_docs.py`: passed.
- DOCX render QA could not complete because LibreOffice/soffice was not found on this machine.
- `CHANGELOG.md` has been updated through version 11.
- `README.md`, `CHANGELOG.md`, and `AGENTS.md` have been updated to record the version 12 state and the rule that future project-facing updates should be committed and pushed to GitHub after verification.
- Streamlit startup via `.venv\Scripts\streamlit.exe` still fails because the venv launcher points to a missing Python 3.12 install.
- Backup startup with bundled Python plus `.venv\Lib\site-packages` reached `http://127.0.0.1:8501`, but the foreground command was killed by timeout before a separate health check could confirm `200`.
