<<<<<<< HEAD
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import shutil
import os

app = FastAPI()   # 🔥 THIS LINE IS IMPORTANT

# CORS (required for frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

questions = []

# Upload policy files
@app.post("/upload-policy")
async def upload_policy(files: List[UploadFile] = File(...)):
    for file in files:
        with open(f"{UPLOAD_DIR}/{file.filename}", "wb") as f:
            shutil.copyfileobj(file.file, f)
    return {"message": "uploaded"}

# Upload questionnaire
@app.post("/upload-questionnaire")
async def upload_questionnaire(file: UploadFile = File(...)):
    global questions

    content = (await file.read()).decode("utf-8", errors="ignore")
    questions = content.split("\n")

    return {"message": "questions stored"}

# Generate answers
@app.get("/generate-answers")
def generate_answers():
    answers = []
    for q in questions:
        if q.strip():
            answers.append({
                "question": q,
                "answer": "Sample AI answer",
                "confidence": 0.85
            })
    return answers

# Scan AWS
@app.post("/scan-aws")
def scan():
    return {"status": "scan done"}

# Download report
@app.get("/download-report")
def download_report():
    from fastapi.responses import FileResponse

    path = "report.txt"
    with open(path, "w") as f:
        f.write("Sample report")

    return FileResponse(path, filename="report.txt")
=======
from fastapi import FastAPI
<<<<<<< HEAD
from fastapi.responses import FileResponse
from services.verify_service import map_question_to_evidence, verify_answer
from services.report_service import generate_pdf

app = FastAPI()


@app.post("/verify")
def verify():
    questions = [
    # 🔐 Encryption
    {"question": "Is all customer data encrypted at rest?", "answer": "Yes"},
    {"question": "Are all S3 buckets encrypted by default?", "answer": "Yes"},
    {"question": "Is data encrypted in transit using TLS 1.3?", "answer": "Yes"},
    {"question": "Are backup data stores also encrypted?", "answer": "Yes"},

    # 🔑 IAM & MFA
    {"question": "Is MFA enabled for all IAM users?", "answer": "Yes"},
    {"question": "Do all privileged users have MFA enabled?", "answer": "Yes"},
    {"question": "Are there any users without MFA?", "answer": "No"},
    {"question": "Is root account MFA enabled?", "answer": "Yes"},

    # 🔒 Access Control
    {"question": "Is public access blocked for all S3 buckets?", "answer": "Yes"},
    {"question": "Are least privilege policies enforced?", "answer": "Yes"},
    {"question": "Are unused IAM users removed regularly?", "answer": "Yes"},

    # 📜 Logging & Monitoring
    {"question": "Is CloudTrail logging enabled across all regions?", "answer": "Yes"},
    {"question": "Are logs protected from tampering?", "answer": "Yes"},
    {"question": "Is log file validation enabled?", "answer": "Yes"},

    # 🔐 Password Policy
    {"question": "Is the minimum password length at least 12 characters?", "answer": "Yes"},
    {"question": "Are password complexity requirements enforced?", "answer": "Yes"},
    {"question": "Do passwords expire periodically?", "answer": "Yes"},

    # ⚠️ Edge / Trick Cases
    {"question": "Are any S3 buckets left unencrypted?", "answer": "No"},
    {"question": "Are any IAM users missing MFA?", "answer": "No"},
    {"question": "Is any bucket publicly accessible?", "answer": "No"},
    {"question": "Are there any security misconfigurations?", "answer": "No"},

    # 🧠 Logical / Indirect Questions
    {"question": "Is your AWS environment fully compliant with encryption policies?", "answer": "Yes"},
    {"question": "Do all systems meet internal security standards?", "answer": "Yes"},
    {"question": "Is your infrastructure audit-ready?", "answer": "Yes"},

    # 🚨 Exceptional Cases
    {"question": "If encryption fails, is fallback security applied?", "answer": "Yes"},
    {"question": "If MFA is disabled temporarily, is it logged?", "answer": "Yes"},
    {"question": "Are security incidents detected within 24 hours?", "answer": "Yes"}
]

    scan = {
    "s3_buckets": [
        {"name": "acme-customer-data", "encrypted": True, "public_access_blocked": True},
        {"name": "acme-internal-logs", "encrypted": False, "public_access_blocked": False}
    ],
    "iam": {
        "users": [
            {"username": "admin-user", "mfa_enabled": True},
            {"username": "developer-user", "mfa_enabled": False}
        ],
        "root_mfa_enabled": True,
        "password_policy": {"min_length": 8}
    },
    "cloudtrail": {
        "logging_active": True,
        "multi_region": True,
        "log_validation": True
    }
}

    results = []

    for q in questions:
        evidence = map_question_to_evidence(q["question"], scan)
        verification = verify_answer(q["question"], q["answer"], evidence)

        results.append({
            "question": q["question"],
            "answer": q["answer"],
            "status": verification["status"],
            "explanation": verification["explanation"]
        })

    return results


@app.get("/download-report")
def download_report():
    data = verify()
    file_path = generate_pdf(data)
    return FileResponse(file_path, media_type="application/pdf", filename="report.pdf")
=======
from pydantic import BaseModel
from services.bedrock_services import generate_response

app = FastAPI()

class Query(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"status": "TrustCheck backend running 🚀"}

@app.post("/ask-ai")
def ask_ai(query: Query):
    response = generate_response(query.prompt)
    return {"response": response}
>>>>>>> a0578f6375831ceb0460556cb8cf5c86cc0a5410
>>>>>>> bf570bd3f3d364223ad72f373dbfb41b01d34a32
