# Benefits PDF Analyzer - Backend API

AI-powered backend service for analyzing employee benefits PDFs and categorizing insurance plans using Google Gemini 2.5 Pro.

## Features

- 📄 PDF text extraction and chunking (handles large documents)
- 🤖 AI-powered summarization with Gemini 2.5 Pro
- 🏷️ Automatic categorization of insurance plans:
  - Health, Dental, Vision Insurance
  - Life & Disability Insurance
  - Employee Assistance Programs
  - Supplemental Benefits (Accident, Critical Illness, etc.)
- 💾 Saves extracted summaries and categorized data as JSON
- ⚡ Rate limit handling and error recovery

## Quick Start

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
source ../LincHack/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your GEMINI_API_KEY to .env

# Run the server
python main.py
```

Server runs on `http://localhost:3001`

### API Endpoints

#### Upload PDF
```bash
POST /upload-pdf
Content-Type: multipart/form-data

# Example
curl -X POST "http://localhost:3001/upload-pdf" \
  -F "file=@benefits.pdf"
```

**Response:**
```json
{
  "success": true,
  "message": "PDF processed successfully in 12 chunks",
  "data": {
    "original_filename": "benefits.pdf",
    "total_pages": 57,
    "chunks_processed": 12,
    "summary_file": "path/to/summary.txt",
    "categorized_data_file": "path/to/categorized.json",
    "analysis": {
      "summary": "Document overview...",
      "total_plans_found": 18,
      "categories": {
        "dental_insurance": [...],
        "vision_insurance": [...],
        "disability_insurance": [...],
        ...
      },
      "recommendations": [...]
    }
  }
}
```

#### Health Check
```bash
GET /health
```

## Tech Stack

- **FastAPI** - Modern Python web framework
- **PyMuPDF (fitz)** - PDF text extraction
- **Google Gemini 2.5 Pro** - AI summarization and categorization
- **Python 3.9+**

## Configuration

### Environment Variables
- `GEMINI_API_KEY` - Your Google AI Studio API key

### Processing Limits
- Processes PDFs in 5-page chunks
- Handles up to 200K characters of summarized text
- 2-second delay between API calls to respect rate limits

## Output Files

Generated files are stored in:
- `extracted_data/` - Text summaries of each chunk
- `categorized_data/` - Final JSON analysis with all plans categorized

## Development

```bash
# Run backend in development mode
cd backend
python main.py

# Backend will auto-reload on file changes
```

## License

MIT
