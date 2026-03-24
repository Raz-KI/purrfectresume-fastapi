from fastapi import APIRouter, UploadFile, File, Form
from app.services.resume_parser import extract_text
from app.services.llm_service import generate_resume
from app.services.file_generator import generate_pdf, generate_docx
from fastapi.responses import StreamingResponse

from pydantic import BaseModel

class ResumeRequest(BaseModel):
    content: str

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
    # pdf = generate_pdf(ats_resume)
    # docx = generate_docx(ats_resume)

    return {
        "message": "Resume generated",
        "content": ats_resume
    }
@router.post("/download-pdf")
def download_pdf(req: ResumeRequest):
    print("hi")
    print(req.content)
    print("hi")
    pdf_buffer = generate_pdf(req.content)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=resume.pdf"}
    )
@router.post("/download-docx")
def download_docx(req: ResumeRequest):
    docx_buffer = generate_docx(req.content)

    return StreamingResponse(
        docx_buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=resume.docx"}
    )