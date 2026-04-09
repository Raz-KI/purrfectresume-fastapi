from dotenv import load_dotenv
import os
from google import genai
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
print("Gemini client initialized successfully.",os.getenv("GEMINI_API_KEY"))

generateCoverLetter = True
companyName = "Google"
def generate_resume(resume_text, job_description):

    prompt = f"""
    You are an expert career coach and ATS (Applicant Tracking System) specialist.
    
    Task:
    1. Analyze the provided Job Description (JD) and the existing Resume.
    2. Identify key skills, technologies, and keywords required by the JD.
    3. Rewrite the Resume to be highly optimized for this specific JD while maintaining truthfulness.
    4. Ensure the new resume has a high ATS score.
    """
    if generateCoverLetter:
        prompt += f"""`5. Write a professional, tailored Cover Letter for the role at {companyName or 'the company'}."""
    
    prompt += '''
    6. Provide the output in a structured JSON format.

    Your task:
- Rewrite the candidate's resume to perfectly match the job description
- Optimize for ATS keyword matching
- Keep content concise, impactful, and quantified where possible

STRICT OUTPUT RULES:
- Output ONLY valid JSON
- No markdown, no explanations, no extra text
- Follow the exact schema below
- Do not add or remove fields
- Ensure all lists are properly formatted
- Use British English spelling

JSON SCHEMA:
{
  "optimizedResume": {
    "name": "",
    "phone": "",
    "email": "",
    "linkedin": "",
    "github": "",
    "portfolio": "",
    "profile": "",
    "competencies": [],
    "experience": [
      {
        "role": "",
        "company": "",
        "dates": "",
        "bullets": []
      }
    ],
    "projects": [
      {
        "name": "",
        "bullets": []
      }
    ],
    "education": "",
    "achievements": []
  },
  "atsScore": 0,
  "keywordsFound": [],
  "keywordsMissing": [],
  "suggestions": [],
  "coverLetter": ""
}

CONTENT RULES:

PROFILE:
- 2–4 lines
- Tailored to the job description
- Include role, experience, and key strengths

CORE COMPETENCIES:
- 6–12 skills
- Extract from job description keywords
- Use short phrases only (e.g., "Python", "REST APIs", "AWS")

EXPERIENCE:
- Each role must include:
  - role, company, dates
  - 3–5 bullet points
- Bullet format:
  - Start with action verb
  - Include impact/result (numbers if possible)
  - Include relevant technologies

PROJECTS:
- 1–3 relevant projects
- Each with 2–4 bullet points
- Focus on technical implementation + impact

EDUCATION:
- Single line format:
  Degree | University | Year

ACHIEVEMENTS:
- 2–5 items
- Include awards, certifications, or measurable accomplishments

FORMATTING RULES:
- No special characters except standard punctuation
- No emojis
- No duplicate content
- Dates format: "Jan 2023 – Present" or "2021 – 2023"

    '''
    if generateCoverLetter:
        prompt += f"""
        Cover Letter Guidelines:
        - Use a professional, formal tone.
        - Address it to the Hiring Manager at ${companyName or 'the company'}.
        - Highlight 2-3 key achievements from the resume that directly match the JD.
        - Express genuine enthusiasm for the role and the company.
        - Keep it under 400 words.
        """
    prompt += f"""
    Job Description:
    {job_description}

    Existing Resume:
    {resume_text}

    Output Requirements:
    - optimizedResume: The full text of the optimized resume in Markdown format following the structure above.
    - atsScore: A number from 0 to 100 representing how well the optimized resume matches the JD.
    - keywordsFound: List of important keywords from the JD that are now in the resume.
    - keywordsMissing: List of keywords from the JD that couldn't be naturally included but are important.
    - suggestions: 3-5 specific tips for the user to further improve their application for this role.
  
    """
    # print(client.models.list())
    # for m in genai.list():
    #     print(m.name, m.supported_generation_methods)
    response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=prompt)
    print("###")
    print(response.txt)
    print("###")
    return response.text
