from dotenv import load_dotenv
import os
from google import genai
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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
    
    prompt += f"""
    6. Provide the output in a structured JSON format.

    Professional Resume Structure Guidelines:
    - DO NOT use literal escape characters like "\\n" or "\\t". Use actual newlines.
    - Use a single # for the Candidate Name at the top.
    - Immediately below the name, provide contact info (Email | Phone | LinkedIn | GitHub) on a new line without any markdown header.
    - Use ## for major sections: PROFESSIONAL SUMMARY, CORE COMPETENCIES, PROFESSIONAL EXPERIENCE, EDUCATION, and CERTIFICATIONS.
    - Use ### for Job Titles and Company Names (e.g., ### Senior Software Engineer | Google).
    - Use bullet points (- ) for specific achievements and responsibilities.
    - Focus on quantifiable achievements (e.g., "Increased efficiency by 20%").
    - Ensure keywords from the JD are naturally integrated.
    - Use standard sentence case for descriptions, only use UPPERCASE for section headers (##).
    """
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

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt)
    print(response.text)
    return response.text
