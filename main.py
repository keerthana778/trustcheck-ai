from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import fitz
import os

# Team Service Imports
from services.bedrock_services import generate_response
from services.verify_service import map_question_to_evidence, verify_answer
from services.report_service import generate_pdf
from services.scanner_service import execute_full_scan

app = FastAPI(title="TrustCheck AI - Final Integrated System")

# Global variable to hold data so the PDF button knows what to print
LATEST_AUDIT_RESULTS = []

@app.get("/")
def root():
    return {"status": "TrustCheck Backend Integrated & Running 🚀"}

# --- PERSON 2: AI ANALYSIS (RAG) ---
@app.post("/analyze-document")
async def analyze_document(file: UploadFile = File(...)):
    """Upload the PDF Security Policy to be analyzed by NVIDIA AI."""
    content = await file.read()
    doc = fitz.open(stream=content, filetype="pdf")
    text = "".join([page.get_text() for page in doc])
    
    # Context-aware prompt for NVIDIA RAG
    prompt = f"Using this document context, summarize the security risks: {text[:4000]}"
    response = generate_response(prompt)
    
    return {"analysis": response.strip()}

# --- PERSON 3 & 4: AUDIT & VERIFICATION (PDF UPLOAD VERSION) ---
@app.post("/verify")
async def verify(file: UploadFile = File(...)):
    """Upload a PDF Questionnaire to audit the infrastructure."""
    global LATEST_AUDIT_RESULTS
    
    # 1. Read the uploaded PDF file
    content = await file.read()
    doc = fitz.open(stream=content, filetype="pdf")
    raw_text = "".join([page.get_text() for page in doc])
    
    # 2. Extract Questions: Split the text by newlines and remove empty blanks
    # This turns the PDF text into a clean Python list!
    pdf_questions = [line.strip() for line in raw_text.split("\n") if len(line.strip()) > 5]

    # 3. Get the Mock AWS Infrastructure Reality
    scan = execute_full_scan()

    results = []
    for q in pdf_questions:
        # Cross-reference the uploaded question with the Mock Scan
        evidence = map_question_to_evidence(q, scan)
        verification = verify_answer(q, "Yes", evidence)
        
        results.append({
            "question": q,
            "answer": "Yes", # Simulating the AI claimed 'Yes'
            "status": verification["status"],
            "explanation": verification["explanation"]
        })
        
    # Save the results temporarily for the PDF endpoint
    LATEST_AUDIT_RESULTS = results
    return results

@app.get("/download-report")
def download_report():
    """Generates and downloads the PDF report of the latest audit."""
    global LATEST_AUDIT_RESULTS
    
    # Prevent crashing if they click download before verifying
    if not LATEST_AUDIT_RESULTS:
        return {"error": "Please run the /verify endpoint with a PDF first!"}
        
    file_path = generate_pdf(LATEST_AUDIT_RESULTS)
    return FileResponse(file_path, media_type="application/pdf", filename="TrustCheck_Report.pdf")