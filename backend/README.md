# Benefits PDF Analyzer Backend

FastAPI backend service for analyzing employee benefits PDFs.

## Setup

```bash
# Activate virtual environment
source ../LincHack/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your GEMINI_API_KEY

# Run server
python main.py
```

## API Endpoints

### POST /upload-pdf
Upload and analyze benefits PDF
- **Input:** PDF file (multipart/form-data)
- **Output:** JSON with categorized insurance plans

### GET /health
Health check endpoint

### GET /
API status and version

## Environment Variables

- `GEMINI_API_KEY` - Google AI Studio API key (required)

## Output Directories

- `extracted_data/` - PDF text summaries
- `categorized_data/` - JSON analysis results
- `uploads/` - Temporary upload storage
