# PDF Upload & AI Integration Guide

## Overview
The HR Manager dashboard now supports automated benefits extraction from PDF documents. When you click "Add New Benefit/Policy", you can upload a PDF containing benefits information, which will be:
1. Processed by AI (Google Gemini)
2. Automatically categorized
3. Synced to Supabase database
4. Displayed in your benefits list

## Setup Instructions

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8+
- Supabase account with project set up
- Google Gemini API key

### 1. Frontend Setup (React)

```bash
# Install dependencies
npm install

# Create .env file if it doesn't exist
cat > .env << EOF
VITE_API_URL=http://localhost:3001/api
VITE_PYTHON_BACKEND_URL=http://localhost:8000
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
EOF

# Start React app
npm run dev
```

The React app will run on http://localhost:5173 (or 3000)

### 2. Express API Setup (Node.js)

```bash
# Install dependencies (if not already done)
npm install

# Create/update .env file with Supabase credentials
cat >> .env << EOF
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
EOF

# Start Express server
node server.js
```

The Express API will run on http://localhost:3001

### 3. Python Backend Setup (FastAPI)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with Gemini API key
cat > .env << EOF
GEMINI_API_KEY=your_gemini_api_key_here
EOF

# Start FastAPI server
python main.py
```

The FastAPI server will run on http://localhost:8000

**Get your Gemini API key from:** https://makersuite.google.com/app/apikey

### 4. Database Setup (Supabase)

Ensure your Supabase database has these tables:

```sql
-- Benefits table
CREATE TABLE benefits (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  cost NUMERIC DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Employees table
CREATE TABLE employees (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  department TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Employee benefits junction table
CREATE TABLE employee_benefits (
  id BIGSERIAL PRIMARY KEY,
  employee_id BIGINT REFERENCES employees(id) ON DELETE CASCADE,
  benefit_id BIGINT REFERENCES benefits(id) ON DELETE CASCADE,
  enrollment_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(employee_id, benefit_id)
);
```

## How to Use PDF Upload

### Step 1: Access the Benefits Page
1. Open the HR Manager dashboard
2. Click on "Manage Benefits and Policies" tab

### Step 2: Upload PDF
1. Click the "Add New Benefit/Policy (Upload PDF)" button
2. A modal will appear with a drag-and-drop zone
3. Either:
   - Click to browse and select a PDF file
   - Drag and drop a PDF file into the zone

### Step 3: Processing
Once uploaded, the system will:
1. **Upload** the PDF to the Python backend (progress: 0-50%)
2. **Process with AI** - Extract text and analyze with Google Gemini (50-90%)
3. **Categorize** - Organize benefits into categories (90-100%)
4. **Sync to Database** - Automatically add to Supabase

You'll see:
- Real-time progress bar
- Estimated processing time
- Current status messages
- A loading spinner during sync

### Step 4: Completion
After successful processing:
- A success message appears
- Number of benefits found is displayed
- Benefits list automatically refreshes
- New benefits appear in the dashboard

## Troubleshooting

### PDF Upload Fails
**Error:** "Failed to upload and process PDF"

**Solutions:**
1. Check if Python backend is running on port 8000:
   ```bash
   curl http://localhost:8000/health
   ```
2. Verify Gemini API key is set in `backend/.env`
3. Check browser console for detailed error messages

### Sync to Database Fails
**Error:** "Failed to sync to database"

**Solutions:**
1. Verify Express API is running on port 3001:
   ```bash
   curl http://localhost:3001/api/benefits
   ```
2. Check Supabase credentials in `.env`
3. Verify database tables exist (see Database Setup above)

### No Benefits Appear After Upload
**Solutions:**
1. Check backend/categorized_data/ for JSON files
2. Manually refresh the page
3. Check browser console and server logs for errors
4. Verify the PDF contains recognizable benefits information

### Python Backend Not Starting
**Error:** "ModuleNotFoundError" or import errors

**Solutions:**
```bash
cd backend
pip install --upgrade pip
pip install -r requirements.txt
```

### CORS Errors
If you see CORS errors in the browser console:
1. Verify both servers are running
2. Check that CORS is enabled in `backend/main.py` (already configured)
3. Ensure frontend is using correct backend URLs

## Development Tips

### Testing PDF Upload
Use sample benefits PDFs from `backend/test_pdfs/` (if available) or any employee benefits document.

### Viewing Processed Data
After uploading a PDF:
1. Check `backend/extracted_data/` for text extraction results
2. Check `backend/categorized_data/` for AI-analyzed JSON

### Manual Sync (Alternative)
If automatic sync fails, you can manually run:
```bash
./sync-benefits.sh
```

This script:
1. Reads the latest categorized JSON
2. Syncs to Supabase
3. Confirms success

### Environment Variables Summary

**Frontend (.env)**
- `VITE_API_URL` - Express API URL (default: http://localhost:3001/api)
- `VITE_PYTHON_BACKEND_URL` - FastAPI URL (default: http://localhost:8000)
- `VITE_SUPABASE_URL` - Your Supabase project URL
- `VITE_SUPABASE_ANON_KEY` - Your Supabase anonymous key

**Backend (backend/.env)**
- `GEMINI_API_KEY` - Your Google Gemini API key

**Root (.env for Express)**
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_ANON_KEY` - Your Supabase anonymous key

## Architecture Flow

```
┌─────────────────┐
│   React App     │  (Port 5173/3000)
│   (Frontend)    │
└────────┬────────┘
         │
         │ 1. Display UI
         │ 2. Handle PDF upload
         │ 3. Show progress
         │
         ├──────────────┐
         │              │
         ▼              ▼
┌────────────────┐  ┌──────────────────┐
│  Express API   │  │  FastAPI Server  │
│  (Port 3001)   │  │  (Port 8000)     │
└────────┬───────┘  └────────┬─────────┘
         │                   │
         │                   │ 2. Process PDF
         │                   │ 3. Extract text
         │ 4. Sync benefits  │ 4. AI analysis
         │                   │
         ▼                   ▼
┌─────────────────┐  ┌──────────────────┐
│    Supabase     │  │ Google Gemini AI │
│   (Database)    │  │                  │
└─────────────────┘  └──────────────────┘
```

## API Endpoints

### Python Backend (FastAPI)
- `POST /upload-pdf` - Upload and process PDF
- `GET /` - Health check
- `GET /health` - Detailed health check

### Express API
- `GET /api/benefits` - List all benefits
- `POST /api/benefits` - Add new benefit (manual)
- `DELETE /api/benefits/:id` - Delete benefit
- `POST /api/sync-benefits` - Sync from PDF analysis
- `GET /api/employees` - List employees
- `POST /api/employees` - Add employee
- `GET /api/employee-benefits` - List enrollments
- `POST /api/employee-benefits` - Enroll employee
- `DELETE /api/employee-benefits/:id` - Remove enrollment

## Performance Notes

- **Small PDFs (< 5 pages):** ~15-30 seconds
- **Medium PDFs (5-20 pages):** ~30-90 seconds
- **Large PDFs (> 20 pages):** 2-5 minutes

Processing time depends on:
- PDF page count
- Text complexity
- Gemini API response time
- Network speed

## Next Steps

1. Test with a sample benefits PDF
2. Review extracted data in `backend/categorized_data/`
3. Verify benefits appear in dashboard
4. Enroll employees in new benefits

## Support

For issues or questions:
1. Check server logs in all three terminals
2. Review browser console for frontend errors
3. Verify all environment variables are set
4. Ensure all services are running simultaneously
