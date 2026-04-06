from fastapi import APIRouter, UploadFile, File, Form
from app.services.resume_parser import extract_text
from app.services.llm_service import generate_resume
from app.services.file_generator import generate_pdf, generate_docx
from app.services.extract_data_from_response import extract_data_from_response
from fastapi.responses import StreamingResponse

from pydantic import BaseModel

class ResumeRequest(BaseModel):
    content: str

router = APIRouter()

@router.post("/generate-resume")
async def generate_resume_endpoint(
    resume: str = Form(...),
    job_description: str = Form(...),
    companyName: str = Form(None),  # optional
    generateCoverLetter: bool = Form(False)  # optional
):
    print("Recieved resume and job desc. Generating resume now...")
    # 1. Extract resume text
    # resume_text = await extract_text(resume)

    # 2. Generate ATS resume using LLM
    llm_response = generate_resume(resume, job_description)

    # 3. Get all the relevant data from the response
    final_data = extract_data_from_response(llm_response)

    return {
        "message": "Resume generated",
        "content": {
            "optimized_resume": final_data[0],
            "ats_score": final_data[1],
            "keywords_found": final_data[2],
            "keywords_missing": final_data[3],
            "suggestions": final_data[4],
            "cover_letter": final_data[5]
        }
    }
@router.post("/download-pdf")
def download_pdf(req: ResumeRequest):
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