
# My First Project

A simple Python project that uses environment variables.

## Installation

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate it (Windows):

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create `.env` from `.env.example`:

```powershell
Copy-Item .env.example .env
```

## Environment Variables

- `APP_NAME` — application name.
- `API_KEY` — API key.

## Run

```bash
python main.py
```


