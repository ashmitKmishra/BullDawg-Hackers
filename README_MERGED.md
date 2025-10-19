# BullDawg Hackers - Integrated Benefits Management System

This branch (`Backend+HR`) merges two independent systems into one unified platform:

1. **Step1_RecommendationSystem** - AI-powered PDF benefits analyzer
2. **HR-manager** - HR management interface with Supabase integration

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Frontend (React)                  │
│              HR Management Dashboard                 │
│              - Benefits Management                   │
│              - Employee Management                   │
│              - AI Chatbot Interface                  │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐   ┌────────▼────────┐
│  Express API   │   │  FastAPI        │
│  (Node.js)     │   │  (Python)       │
│  Port: 3001    │   │  Port: 3001     │
│                │   │                 │
│  - Benefits    │   │  - PDF Upload   │
│  - Employees   │   │  - Text Extract │
│  - Enrollment  │   │  - AI Analysis  │
└───────┬────────┘   └────────┬────────┘
        │                     │
        │                     │
┌───────▼─────────────────────▼────────┐
│           Supabase Database           │
│                                       │
│  Tables:                              │
│  - benefits                           │
│  - employees                          │
│  - employee_benefits                  │
└───────────────────────────────────────┘
```

## 📂 Project Structure

```
BullDawg-Hackers/
├── backend/                    # Python FastAPI server
│   ├── main.py                # PDF processing & AI analysis
│   ├── sync_to_supabase.py   # Sync categorized data to Supabase
│   ├── requirements.txt       # Python dependencies
│   ├── categorized_data/      # AI-analyzed benefits (JSON)
│   ├── extracted_data/        # Raw PDF text
│   └── uploads/               # Uploaded PDF files
│
├── api/                        # Node.js Express API
│   └── index.js               # Supabase CRUD operations
│
├── src/                        # React frontend
│   ├── App.jsx                # Main HR dashboard
│   ├── components/
│   │   ├── AIChatbot.jsx     # AI assistant
│   │   ├── PDFUpload.jsx     # PDF upload component (Step1)
│   │   ├── LoginButton.jsx   # Auth0 login (Step1)
│   │   └── ...
│   └── ...
│
├── server.js                   # Express server entry point
├── .env                        # Environment variables
├── package.json               # Node.js dependencies
└── vite.config.js             # Vite configuration
```

## 🔧 Setup Instructions

### 1. Install Dependencies

#### Frontend & API (Node.js)
```bash
npm install
```

#### Backend (Python)
```bash
cd backend
source ../LincHack/bin/activate  # Activate virtual environment
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the root directory:

```env
# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key

# Supabase Configuration
SUPABASE_URL=https://oidsjsddvsxlzofjycqc.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key

# Database Configuration
DATABASE_URL=postgresql://postgres:password@db.oidsjsddvsxlzofjycqc.supabase.co:5432/postgres

# Server Configuration
PORT=3001
```

Also create `backend/.env`:
```env
GEMINI_API_KEY=your_gemini_api_key
SUPABASE_URL=https://oidsjsddvsxlzofjycqc.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 3. Database Setup (Supabase)

The system uses three tables:

#### `benefits`
```sql
CREATE TABLE benefits (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  cost TEXT,
  category TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### `employees`
```sql
CREATE TABLE employees (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  department TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### `employee_benefits`
```sql
CREATE TABLE employee_benefits (
  id BIGSERIAL PRIMARY KEY,
  employee_id BIGINT REFERENCES employees(id) ON DELETE CASCADE,
  benefit_id BIGINT REFERENCES benefits(id) ON DELETE CASCADE,
  enrollment_date TIMESTAMPTZ DEFAULT NOW()
);
```

## 🚀 Running the System

### Option 1: Run All Services

#### Terminal 1 - Frontend (React + Vite)
```bash
npm run dev
# Runs on http://localhost:3000
```

#### Terminal 2 - API Server (Express)
```bash
npm run server
# Runs on http://localhost:3001
```

#### Terminal 3 - Backend (FastAPI - when needed)
```bash
source LincHack/bin/activate
cd backend
python main.py
# Runs on http://localhost:3001
```

### Option 2: Development Workflow

1. **For HR Dashboard**: Run frontend + Express API
   ```bash
   # Terminal 1
   npm run dev
   
   # Terminal 2
   npm run server
   ```

2. **For PDF Analysis**: Run frontend + Python backend
   ```bash
   # Terminal 1
   npm run dev
   
   # Terminal 2
   source LincHack/bin/activate
   cd backend
   python main.py
   ```

## 📊 Workflow: PDF to Database

### Step 1: Upload & Analyze PDF
```bash
# Start Python backend
cd backend
source ../LincHack/bin/activate
python main.py
```

Upload PDF through the frontend or API:
- PDF → Text Extraction → AI Analysis → `categorized_data/*.json`

### Step 2: Sync to Supabase
```bash
# Run sync script
cd backend
python sync_to_supabase.py
```

This reads the latest `categorized_data/*.json` file and syncs all benefits to Supabase.

### Step 3: Access via HR Dashboard
The Express API and frontend now display the synced benefits data.

## 🔑 Key Features

### From Step1_RecommendationSystem
- ✅ PDF upload and text extraction (PyMuPDF)
- ✅ AI-powered analysis (Google Gemini)
- ✅ Benefits categorization
- ✅ Auth0 authentication (available in components)
- ✅ Chunked processing for large PDFs

### From HR-manager
- ✅ Benefits management CRUD
- ✅ Employee management
- ✅ Benefit enrollment tracking
- ✅ AI chatbot interface
- ✅ Supabase integration
- ✅ RESTful API

### New (Merged)
- ✅ `sync_to_supabase.py` - Bridge between PDF analysis and database
- ✅ Unified environment configuration
- ✅ Combined dependency management

## 🔄 Data Flow

```
1. HR uploads PDF
   ↓
2. Python Backend processes (main.py)
   - Extracts text
   - AI analyzes with Gemini
   - Saves to categorized_data/
   ↓
3. Run sync script (sync_to_supabase.py)
   - Reads latest JSON
   - Inserts into Supabase
   ↓
4. Express API serves data
   ↓
5. Frontend displays in HR dashboard
```

## 📝 API Endpoints

### Express API (Port 3001)
- `GET /api/benefits` - List all benefits
- `POST /api/benefits` - Add new benefit
- `DELETE /api/benefits/:id` - Remove benefit
- `GET /api/employees` - List all employees
- `POST /api/employees` - Add employee
- `GET /api/employee-benefits` - List enrollments
- `POST /api/employee-benefits` - Enroll employee
- `DELETE /api/employee-benefits/:id` - Remove enrollment

### FastAPI (Port 3001 - when running)
- `POST /upload-pdf` - Upload and analyze PDF
- `GET /` - API info
- `GET /health` - Health check

## 🛠️ Development Notes

### Port Configuration
Both backends use port 3001. Run only one at a time:
- Use Express API for normal HR operations
- Use FastAPI when uploading/analyzing PDFs

### Virtual Environment
Python backend requires the `LincHack` virtual environment:
```bash
source LincHack/bin/activate
```

### Dependencies
- **Node.js packages**: Auth0, Supabase client, Express, Vite, React
- **Python packages**: FastAPI, PyMuPDF, Google Generative AI, Supabase client

## 🔐 Security Notes

⚠️ **Current Status**: `.env` files and API keys are tracked for development convenience.

**Before production:**
1. Remove `.env` from git: `git rm --cached .env backend/.env`
2. Add to `.gitignore`
3. Use environment-specific secrets management
4. Rotate all API keys

## 📚 Documentation

- **Gemini API**: https://ai.google.dev/
- **Supabase**: https://supabase.com/docs
- **Auth0**: https://auth0.com/docs
- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/

## 🐛 Troubleshooting

### "Module not found" errors
```bash
npm install
cd backend && pip install -r requirements.txt
```

### Port already in use
```bash
# Kill process on port 3001
lsof -ti:3001 | xargs kill -9
```

### Supabase connection issues
- Verify SUPABASE_URL and SUPABASE_ANON_KEY in `.env`
- Check database tables exist
- Ensure RLS policies allow access

### PyMuPDF installation fails
```bash
pip install PyMuPDF --no-build-isolation
# or
brew install mupdf && pip install PyMuPDF
```

## 🎯 Next Steps

1. **Integrate Auth0** into HR dashboard
2. **Add PDF upload** button in HR interface
3. **Automate sync** - trigger sync_to_supabase.py after PDF processing
4. **Add role-based** access control
5. **Deploy** to production (Vercel + Railway/Render)

## 👥 Contributors

- Built during LincHack 2025
- Team: BullDawg Hackers

---

**Branch**: Backend+HR  
**Last Updated**: October 19, 2025  
**Status**: ✅ Merged & Tested
