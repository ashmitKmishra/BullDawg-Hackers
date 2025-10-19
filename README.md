# Adaptive Benefit Questionnaire + CoverageCraft UI

This repository now hosts both:

- A Python/Flask backend that powers an adaptive benefits questionnaire and generates a PDF report.
- A React (Vite) frontend called "CoverageCraft" that provides a polished, animated UI.

You can run either independently.

## Backend (Flask) – Adaptive Benefit Questionnaire

Minimal Flask application that uses an adaptive engine to recommend benefits and generate a PDF.

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

## Frontend (React + Vite) – CoverageCraft

Animated UI and multi-step questionnaire experience. Lives under `src/` with Vite tooling.

### Quick Start

```bash
npm install
npm run dev
```

Build for production:

```bash
npm run build
```

### Tech Stack

- React 19 + Vite
- Framer Motion, React Router v6
- Custom CSS / Tailwind (where configured)

## Environment

Create a `.env` (backend) and/or `.env.local` (frontend) if needed. Example (backend optional):

```
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_key
```

## Testing (backend)

```bash
python -m pytest tests/
```

## License

MIT

— Built with ❤️ by BullDawg Hackers
