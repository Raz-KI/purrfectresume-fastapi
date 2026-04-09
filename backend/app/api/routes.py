from fastapi import APIRouter, Form
# from app.services.resume_parser import extract_text
# from app.services.llm_service import generate_resume
# from app.services.file_generator import generate_pdf, generate_docx
# from app.services.extract_data_from_response import extract_data_from_response

from services.resume_parser import extract_text                           # 
from services.llm_service import generate_resume                          # Comment this when running on local
from services.file_generator import generate_pdf, generate_docx           #
from services.extract_data_from_response import extract_data_from_response#

from fastapi.responses import StreamingResponse
from docxtpl import DocxTemplate
from pydantic import BaseModel
from typing import List, Optional

class ResumeRequest(BaseModel):
    optimizedResume: str
    coverLetter: str
    filename: str

class ResumeContent(BaseModel):
    optimized_resume: str
    cover_letter: Optional[str] = None
    ats_score: Optional[int] = None
    keywords_found: Optional[List[str]] = []
    keywords_missing: Optional[List[str]] = []
    suggestions: Optional[List[str]] = []

class DownloadRequest(BaseModel):
    content: ResumeContent

# final_resume = {}

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

    global final_resume
    final_resume = final_data[0]
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
def download_pdf(req: DownloadRequest):
    pdf_buffer = generate_pdf(req.content.optimized_resume)

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=resume.pdf"}
    )
@router.post("/download-docx")
def download_docx():
    data = final_resume
    print("This is the fix",data)
    doc = DocxTemplate("backend/app/template.docx")

    context = {
        "NAME": data["name"],
        "PHONE": data["phone"],
        "EMAIL": data["email"],
        "LINKEDIN": data["linkedin"],
        "GITHUB": data["github"],
        "PORTFOLIO": data["portfolio"],
        "PROFILE": data["profile"],
        "COMPETENCIES": " • ".join(data["competencies"]),
        "EXPERIENCE": data["experience"],
        "PROJECTS": data["projects"],
        "EDUCATION": data["education"],
        "ACHIEVEMENTS": data["achievements"]
    }

    doc.render(context)
    doc.save("ATS_Resume.docx")
    return {"status": "ok"}