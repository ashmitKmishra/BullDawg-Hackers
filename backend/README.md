# PDF Processing Backend

## Requirements
- FastAPI for the backend API
- PyMuPDF for PDF text extraction
- Google Generative AI (Gemini) for categorization
- python-multipart for file uploads

## Installation
```bash
pip install fastapi uvicorn pymupdf google-generativeai python-multipart
```

## Environment Variables
Create a `.env` file in the backend directory:
```
GEMINI_API_KEY=your_gemini_api_key_here
```
