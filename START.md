# Start commands

## Installing UV

UV is a fast Python package manager. Install it once on your machine:

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, restart your terminal so the `uv` command is available.

---

## CSV Analyser Manual Run

1. Open a terminal in this folder.
2. Install dependencies:

   **With UV (recommended):**
   ```
   uv sync
   ```

   **With pip (traditional):**
   ```
   pip install -r requirements.txt
   ```

3. Start the app:

   **With UV:**
   ```
   uv run uvicorn csv_analyser.main:app --app-dir src --reload --port 8001
   ```

   **With pip / standard Python:**
   ```
   uvicorn csv_analyser.main:app --app-dir src --reload --port 8001
   ```

4. Open your browser:
   - App: http://127.0.0.1:8001/
   - API docs: http://127.0.0.1:8001/docs
