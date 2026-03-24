from dotenv import load_dotenv
import os
from google import genai

load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))



# openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_resume(resume_text, job_description):
    prompt = f"""
    You are an expert ATS resume optimizer.

    Job Description:
    {job_description}

    Candidate Resume:
    {resume_text}

    Task:
    - Rewrite the resume to match the job description
    - Optimize for ATS keywords
    - Keep it professional and concise
    - Use bullet points
    """

    response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=prompt)

    return response.text


    # return response['choices'][0]['message']['content']
    # return response