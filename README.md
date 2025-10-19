# Adaptive Benefit Questionnaire

An intelligent Flask web application that uses adaptive questioning to provide personalized employee benefit recommendations.

## Features

- **Adaptive Questioning Engine**: Smart question selection based on user responses
- **Machine Learning Models**: Advanced benefit scoring using XGBoost, LightGBM, and CatBoost
- **PDF Report Generation**: Comprehensive benefit assessment reports
- **Risk Assessment**: Multi-dimensional risk analysis
- **Interactive Web Interface**: Clean, responsive UI for questionnaire completion

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Open Browser**
   Navigate to `http://localhost:5000`

## Project Structure

```
├── app.py                          # Main Flask application
├── adaptive_questionnaire_engine.py # Core questioning logic
├── pdf_report_generator.py         # PDF report generation
├── templates/index.html            # Web interface
├── models/                         # Trained ML models
├── data/                          # Training datasets
├── tests/                         # Test suite
└── reports/                       # Generated PDF reports
```

## Core Components

### Adaptive Engine
- Entropy-based question selection
- Dynamic benefit scoring
- Intelligent stopping criteria

### Machine Learning
- Multi-model ensemble approach
- Feature engineering for benefit prediction
- Continuous model improvement

### Report Generation
- Professional PDF reports with burgundy theme
- Comprehensive risk assessment
- Actionable benefit recommendations

## Environment Setup

Create a `.env` file for Supabase integration (optional):
```
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_key
```

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

## Development

The application uses:
- **Backend**: Flask, Python 3.11+
- **ML**: scikit-learn, XGBoost, LightGBM, CatBoost
- **PDF**: ReportLab
- **Database**: Supabase (optional)
- **Frontend**: Vanilla JavaScript, CSS3

## License

MIT License