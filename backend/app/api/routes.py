from fastapi import APIRouter, UploadFile, File, Form
from app.services.resume_parser import extract_text
from app.services.llm_service import generate_resume
from app.services.file_generator import generate_files

router = APIRouter()

@router.post("/generate-resume")
async def generate_resume_endpoint(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    # 1. Extract resume text
    resume_text = await extract_text(resume)
    
    # 2. Generate ATS resume using LLM
    ats_resume = generate_resume(resume_text, job_description)

    # 3. Generate files
    # pdf_path, docx_path = generate_files(ats_resume)
    docx_path = generate_files(ats_resume)

    return {
        "message": "Resume generated",
        "pdf": "pdf",
        "docx": "docx"
    }