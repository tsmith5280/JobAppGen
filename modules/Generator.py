import os
from dotenv import load_dotenv
import openai

load_dotenv()

# Get API settings
openai_api_key = os.getenv("OPENAI_API_KEY")
premium_model = os.getenv("PREMIUM_MODEL", "gpt-4")
free_model = os.getenv("FREE_MODEL", "gpt-3.5-turbo")
use_placeholder = os.getenv("USE_PLACEHOLDER", "false").lower() == "true"

# Create OpenAI client only if needed
if not use_placeholder:
   api_key = openai_api_key or os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set.")
client = openai.OpenAI(api_key=api_key)


def generate_resume(api_key, name, email, skills, experience, model):
    if use_placeholder:
        return (
            f"Placeholder Resume\n"
            f"==================\n"
            f"Name: {name}\nEmail: {email}\n\n"
            f"Skills: {skills}\nExperience: {experience}\n\n"
            f"Note: This is a placeholder response for development purposes."
        )

    try:
        prompt = (
            f"Generate a professional resume for:\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Skills: {skills}\n"
            f"Experience: {experience}\n"
        )

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating resume: {str(e)}"

def generate_cover_letter(api_key, name, job_title, company, job_description, model):
    if use_placeholder:
        return (
            f"Placeholder Cover Letter\n"
            f"========================\n"
            f"Dear Hiring Manager at {company},\n\n"
            f"My name is {name}, and I am excited to apply for the role of {job_title}. "
            f"I believe my experience and skills align with the job description: {job_description}.\n\n"
            f"Note: This is a placeholder response for development purposes."
        )

    try:
        prompt = (
            f"Generate a cover letter for:\n"
            f"Name: {name}\n"
            f"Job Title: {job_title}\n"
            f"Company: {company}\n"
            f"Job Description: {job_description}\n"
        )

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating cover letter: {str(e)}"
