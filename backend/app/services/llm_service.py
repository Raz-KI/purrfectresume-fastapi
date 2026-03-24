# import openai
import os

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

    # response = openai.ChatCompletion.create(
    #     model="gpt-4o-mini",
    #     messages=[{"role": "user", "content": prompt}]
    # )
    response = "You are selected"

    # return response['choices'][0]['message']['content']
    return response