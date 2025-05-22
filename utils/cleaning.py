import re

def clean_resume_output(text):
    """Remove assistant commentary from resume output."""
    pattern = r"\n?In this resume,? I .*?$"
    return re.sub(pattern, "", text, flags=re.IGNORECASE | re.DOTALL).strip()

def extract_resume_commentary(text):
    """Pull out the AI commentary from the resume, if it exists."""
    match = re.search(r"(In this resume,? I .*)", text, flags=re.IGNORECASE)
    return match.group(1).strip() if match else None
