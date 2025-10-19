# Adaptive Benefit Questionnaire (Flask-only)

Minimal Flask application that uses an adaptive engine to recommend benefits and generate a PDF. This repo has been simplified to contain only what's needed to run the adaptive benefit questionnaire.

### Quick Start

1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server
   ```bash
   python app_with_pdf.py
   ```

3. Open browser: http://localhost:5000

### Project Structure (backend)

```
├── app_with_pdf.py                  # Flask app with inlined PDF generation and risk assessment
├── adaptive_questionnaire_engine.py # Core questioning logic
├── templates/index.html             # Web interface (single template)
├── tests/                           # Test suite
└── reports/                         # Generated PDF reports
```

## What was removed

- React/Vite frontend and related configs (vite.config.js, package.json, tailwind/postcss, src/)
- Extra pages (Home/HR) – the app now serves the questionnaire directly at `/`

## Host on GitHub

This repo publishes a static site from `docs/` to GitHub Pages (workflow runs on HR-manager). The static site needs a running backend.

Steps:
- Deploy backend (choose one):
   1) Render (one-click): create a new Web Service from this repo; Render will read `render.yaml`.
   2) Any Python host: run `gunicorn app_with_pdf:app --bind 0.0.0.0:$PORT` with Python 3.10+.
- Note your backend URL (e.g., `https://your-app.onrender.com`).
- Edit `docs/config.js` and set `window.API_BASE = 'https://your-app.onrender.com'`.
- Push to HR-manager; GitHub Actions will deploy Pages. Enable Pages for the repo (Source: GitHub Actions).
- Visit: `https://<owner>.github.io/<repo>/`.

Local preview of docs:
Open `docs/index.html` directly in a browser and set API_BASE to your local Flask server (e.g., `http://127.0.0.1:5000`).

## Environment

Create a `.env` if needed. Example (optional):

```
# Not required anymore – external integrations removed
# SUPABASE_URL=your_supabase_url
# SUPABASE_ANON_KEY=your_supabase_key
```

## Testing (backend)

```bash
python -m pytest tests/
```


