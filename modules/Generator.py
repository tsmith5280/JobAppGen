import openai
import os

openai_api_key = os.getenv("OPENAI_API_KEY")
premium_model = os.getenv("PREMIUM_MODEL", "gpt-4")
free_model = os.getenv("FREE_MODEL", "gpt-3.5-turbo")

def generate_resume(api_key, name, email, skills, experience, is_premium=False):
    openai.api_key = api_key
    model = premium_model if is_premium else free_model

    prompt = f"Generate a professional resume for:\nName: {name}\nEmail: {email}\nSkills: {skills}\nExperience: {experience}\n"
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=300
    )
    return response.choices[0].text.strip()

def generate_cover_letter(api_key, name, job_title, company, job_description, is_premium=False):
    openai.api_key = api_key
    model = premium_model if is_premium else free_model

    prompt = f"Generate a cover letter for:\nName: {name}\nJob Title: {job_title}\nCompany: {company}\nJob Description: {job_description}\n"
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=300
    )
    return response.choices[0].text.strip()
