import json
import re

def extract_data_from_response(llm_response):
    data = json.loads((re.sub(r"```json|```", "", llm_response).strip()))
    # data = json.loads(llm_response)

    optimized_resume = data["optimizedResume"]
    ats_score = data["atsScore"]
    keywords_found = data["keywordsFound"]
    keywords_missing = data["keywordsMissing"]
    suggestions = data["suggestions"]
    cover_letter = data.get("coverLetter")

    return optimized_resume, ats_score, keywords_found, keywords_missing, suggestions, cover_letter