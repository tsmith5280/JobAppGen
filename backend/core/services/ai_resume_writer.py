import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_resume_with_gpt(profile: dict, target: dict):
    prompt = f"""
You are a professional resume writer. Create a tailored resume for the user based on their profile and the target job.

User Profile:
- Name: {profile['full_name']}
- Current Title: {profile['job_title']}
- Skills: {', '.join(profile['skills'])}
- Experience: {profile['experience']}

Target Job:
- Title: {target['job_title']}
- Company: {target['company']}
- Description: {target['description']}

The resume should highlight relevant skills, experience, and include a professional summary at the top. Do not include a cover letter.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional resume writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=800,
    )
    return response["choices"][0]["message"]["content"]
