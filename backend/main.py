from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF
import google.generativeai as genai
import os
import tempfile
import json
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Benefits PDF Analyzer", version="1.0.0")

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-pro')
else:
    print("Warning: GEMINI_API_KEY not found in environment variables")
    model = None

# Storage directories
UPLOAD_DIR = "uploads"
EXTRACTED_DIR = "extracted_data"
CATEGORIZED_DIR = "categorized_data"

# Create directories if they don't exist
for directory in [UPLOAD_DIR, EXTRACTED_DIR, CATEGORIZED_DIR]:
    os.makedirs(directory, exist_ok=True)

def extract_text_from_pdf_pages(pdf_path: str, start_page: int, end_page: int) -> str:
    """
    Extract text from specific pages of PDF using PyMuPDF
    """
    try:
        doc = fitz.open(pdf_path)
        text_content = ""
        
        for page_num in range(start_page, min(end_page, len(doc))):
            page = doc.load_page(page_num)
            text = page.get_text()
            text_content += f"\\n--- Page {page_num + 1} ---\\n{text}\\n"
        
        doc.close()
        return text_content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text from PDF: {str(e)}")

def get_pdf_page_count(pdf_path: str) -> int:
    """
    Get total number of pages in PDF
    """
    try:
        doc = fitz.open(pdf_path)
        page_count = len(doc)
        doc.close()
        return page_count
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading PDF: {str(e)}")

def save_extracted_text(text: str, filename: str) -> str:
    """
    Save extracted text to a document file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{filename}_{timestamp}.txt"
    output_path = os.path.join(EXTRACTED_DIR, output_filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"Extracted Text from {filename}\\n")
        f.write(f"Extracted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
        f.write("=" * 50 + "\\n\\n")
        f.write(text)
    
    return output_path

def summarize_text_chunk(text: str, chunk_number: int, total_chunks: int) -> str:
    """
    Use Gemini to summarize a chunk of text from the PDF
    """
    if not model:
        raise HTTPException(status_code=500, detail="Gemini API not configured")
    
    prompt = f"""
    This is chunk {chunk_number} of {total_chunks} from an employee benefits document.
    
    Please summarize ALL insurance plans and benefits information in this section, including:
    - Health insurance plans (medical, prescription)
    - Dental insurance plans (DHMO, PPO, self-funded)
    - Vision insurance plans
    - Life insurance plans
    - Disability insurance plans (STD, LTD)
    - Accident insurance
    - Critical illness insurance
    - Hospital indemnity insurance
    - Employee assistance programs
    - Any other benefits mentioned
    
    For each plan found, include:
    - Plan names and types
    - Key benefits and features
    - Coverage details
    - Cost information
    - Eligibility requirements
    
    IMPORTANT: Include plans mentioned in disclosures, footnotes, or fine print sections.
    
    Keep the summary concise but comprehensive.
    
    Text:
    {text}
    """
    
    try:
        print(f"Summarizing chunk {chunk_number}/{total_chunks} with Gemini...")
        response = model.generate_content(prompt)
        summary = response.text
        print(f"Successfully summarized chunk {chunk_number}")
        return summary
    except Exception as e:
        error_msg = str(e)
        print(f"Gemini API error on chunk {chunk_number}: {error_msg}")
        
        # If API fails, return the original text
        return f"[Failed to summarize chunk {chunk_number}: {error_msg}]\\n\\n{text[:500]}..."

def categorize_insurance_plans(text: str) -> Dict[str, Any]:
    """
    Use Gemini to categorize insurance plans from the extracted text
    """
    if not model:
        raise HTTPException(status_code=500, detail="Gemini API not configured")
    
    # For better results, process the entire summarized text since it's already condensed
    # Limit to 30000 chars to stay within Gemini token limits
    MAX_TEXT_LENGTH = 30000
    
    if len(text) > MAX_TEXT_LENGTH:
        print(f"Text too long ({len(text)} chars), truncating to {MAX_TEXT_LENGTH} chars")
        text = text[:MAX_TEXT_LENGTH] + "\n\n[Note: Document truncated to fit within API limits. Some plans from later sections may be summarized less completely.]"
    else:
        print(f"Text length is {len(text)} chars, processing full text")
    
    prompt = f"""
    Analyze the following insurance document text and categorize ALL different insurance plans mentioned. 
    
    CRITICAL: You MUST find and include ALL plans, especially:
    - Dental plans (DHMO, PPO, Self-funded, DentalConnect, etc.)
    - Vision plans (VisionConnect, discount programs, etc.)
    - Health insurance plans
    - Life insurance plans
    - Disability insurance (STD, LTD)
    - Employee Assistance Programs (EAP, EmployeeConnect, etc.)
    - Supplemental plans (Accident, Critical Illness, Hospital Indemnity)
    - Any other benefits
    
    Please categorize plans into these categories:
    
    1. Health Insurance Plans (Medical, Hospital, Prescription)
    2. Dental Insurance Plans (DHMO, PPO, Self-funded, etc.) - MUST INCLUDE ALL DENTAL PLANS MENTIONED
    3. Vision Insurance Plans (Insurance plans and discount programs) - MUST INCLUDE ALL VISION PLANS MENTIONED  
    4. Life Insurance Plans
    5. Disability Insurance Plans (Short-term, Long-term)
    6. Employee Assistance Programs
    7. Retirement Plans (401k, Pension)
    8. Other Benefits (Flexible Spending, HSA, Accident, Critical Illness, Hospital Indemnity, etc.)
    
    IMPORTANT: 
    - Include plans even if briefly mentioned in disclosures, footnotes, or fine print
    - Include ALL plan variations (DHMO, PPO, discount programs, etc.)
    - Read through the ENTIRE document before categorizing
    - If a dental or vision plan is mentioned ANYWHERE, it MUST be included in the output
    
    For each plan found, provide:
    - Plan Name
    - Category
    - Key Features/Benefits  
    - Cost Information (if available)
    - Eligibility Requirements (if mentioned)
    - Coverage Details
    
    Return the response in JSON format with the following structure:
    {{
        "summary": "Brief overview of the document",
        "total_plans_found": number,
        "categories": {{
            "health_insurance": [list of health plans],
            "dental_insurance": [list of ALL dental plans found - this MUST NOT be empty if any dental plans are mentioned],
            "vision_insurance": [list of ALL vision plans found - this MUST NOT be empty if any vision plans are mentioned],
            "life_insurance": [list of life plans],
            "disability_insurance": [list of disability plans],
            "employee_assistance": [list of EAP programs],
            "retirement_plans": [list of retirement plans],
            "other_benefits": [list of other benefits]
        }},
        "recommendations": [
            "List of recommendations for employees based on the available plans"
        ]
    }}
    
    Document Text:
    {text}
    """
    
    try:
        print(f"Sending prompt to Gemini (text length: {len(text)} chars)")
        response = model.generate_content(prompt)
        print(f"Received response from Gemini")
        
        # Try to parse the response as JSON
        try:
            # Extract JSON from response if it's wrapped in markdown code blocks
            response_text = response.text
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(response_text)
            print("Successfully parsed JSON response")
            return result
        except json.JSONDecodeError as je:
            print(f"JSON decode error: {str(je)}")
            # If JSON parsing fails, return the raw response
            return {
                "summary": "Analysis completed but response format needs adjustment",
                "raw_response": response.text,
                "total_plans_found": "Unable to parse",
                "categories": {},
                "recommendations": ["Please review the raw response for detailed analysis"]
            }
    except Exception as e:
        error_msg = str(e)
        print(f"Gemini API error: {error_msg}")
        import traceback
        traceback.print_exc()
        
        # Check if it's a rate limit error
        if "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
            raise HTTPException(
                status_code=429, 
                detail="Gemini API rate limit exceeded. The free tier has strict limits. Please try again in a minute or upgrade your API tier."
            )
        elif "400" in error_msg:
            raise HTTPException(
                status_code=400,
                detail=f"Bad request to Gemini API. The document might be too large or contain invalid content: {error_msg}"
            )
        else:
            raise HTTPException(status_code=500, detail=f"Error with Gemini analysis: {error_msg}")

def save_categorized_data(data: Dict[str, Any], filename: str) -> str:
    """
    Save categorized insurance data to a JSON file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{filename}_categorized_{timestamp}.json"
    output_path = os.path.join(CATEGORIZED_DIR, output_filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return output_path

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload PDF, extract text in chunks, and summarize with Gemini
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        print(f"Received file: {file.filename}")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_pdf_path = temp_file.name
        
        print(f"Saved temporary file to: {temp_pdf_path}")
        
        # Get total number of pages
        total_pages = get_pdf_page_count(temp_pdf_path)
        print(f"PDF has {total_pages} pages")
        
        # Process in chunks of 5 pages
        PAGES_PER_CHUNK = 5
        total_chunks = (total_pages + PAGES_PER_CHUNK - 1) // PAGES_PER_CHUNK
        print(f"Will process in {total_chunks} chunks of {PAGES_PER_CHUNK} pages each")
        
        # Create summary file
        base_filename = os.path.splitext(file.filename)[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_filename = f"{base_filename}_summary_{timestamp}.txt"
        summary_path = os.path.join(EXTRACTED_DIR, summary_filename)
        
        # Initialize summary file
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(f"Benefits Document Summary\\n")
            f.write(f"Original File: {file.filename}\\n")
            f.write(f"Total Pages: {total_pages}\\n")
            f.write(f"Processed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
            f.write("=" * 70 + "\\n\\n")
        
        # Process each chunk
        all_summaries = []
        for chunk_idx in range(total_chunks):
            start_page = chunk_idx * PAGES_PER_CHUNK
            end_page = min(start_page + PAGES_PER_CHUNK, total_pages)
            
            print(f"\\nProcessing chunk {chunk_idx + 1}/{total_chunks} (pages {start_page + 1}-{end_page})...")
            
            # Extract text from this chunk
            chunk_text = extract_text_from_pdf_pages(temp_pdf_path, start_page, end_page)
            print(f"Extracted {len(chunk_text)} characters from pages {start_page + 1}-{end_page}")
            
            # Summarize with Gemini
            summary = summarize_text_chunk(chunk_text, chunk_idx + 1, total_chunks)
            all_summaries.append(summary)
            
            # Append to summary file
            with open(summary_path, 'a', encoding='utf-8') as f:
                f.write(f"\\n{'=' * 70}\\n")
                f.write(f"CHUNK {chunk_idx + 1} (Pages {start_page + 1}-{end_page})\\n")
                f.write(f"{'=' * 70}\\n\\n")
                f.write(summary)
                f.write("\\n\\n")
            
            print(f"Appended summary for chunk {chunk_idx + 1} to {summary_path}")
            
            # Small delay between API calls to avoid rate limits
            if chunk_idx < total_chunks - 1:
                import time
                print("Waiting 2 seconds before next API call...")
                time.sleep(2)
        
        print(f"\\nAll chunks processed! Summary saved to: {summary_path}")
        
        # Now analyze all summaries together for final categorization
        print("\\nGenerating final categorization from all summaries...")
        combined_summary = "\\n\\n".join(all_summaries)
        categorized_data = categorize_insurance_plans(combined_summary)
        
        # Save categorized data
        categorized_file_path = save_categorized_data(categorized_data, base_filename)
        print(f"Saved categorized data to: {categorized_file_path}")
        
        # Clean up temporary file
        os.unlink(temp_pdf_path)
        print("Process complete!")
        
        return JSONResponse(content={
            "success": True,
            "message": f"PDF processed successfully in {total_chunks} chunks",
            "data": {
                "original_filename": file.filename,
                "total_pages": total_pages,
                "chunks_processed": total_chunks,
                "summary_file": summary_path,
                "categorized_data_file": categorized_file_path,
                "analysis": categorized_data
            }
        })
        
    except HTTPException as he:
        # Re-raise HTTP exceptions
        print(f"HTTP Exception: {he.detail}")
        raise
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        # Clean up temporary file if it exists
        if 'temp_pdf_path' in locals():
            try:
                os.unlink(temp_pdf_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.get("/")
async def root():
    """
    Health check endpoint
    """
    return {
        "message": "Benefits PDF Analyzer API", 
        "version": "1.0.0",
        "status": "running",
        "gemini_configured": model is not None
    }

@app.get("/health")
async def health_check():
    """
    Detailed health check
    """
    return {
        "status": "healthy",
        "gemini_api": "configured" if model else "not configured",
        "directories": {
            "uploads": os.path.exists(UPLOAD_DIR),
            "extracted_data": os.path.exists(EXTRACTED_DIR),
            "categorized_data": os.path.exists(CATEGORIZED_DIR)
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)
