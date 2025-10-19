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

## License

MIT

— Built with ❤️ by BullDawg Hackers
