Set up a Python virtual environment

```bash
python -m venv venv
. venv/bin/activate
```

Login NotebookLM

```bash
playwright install chromium
notebooklm login
```

Start server

```bash
export notebook_id='...'
python server.py
```

Test

Using `index.html`