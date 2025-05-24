def generate_resume(api_key, name, email, skills, experience, model, use_placeholder, client):
    if use_placeholder:
        return f"""Placeholder Resume\n==================\nName: {name}\nEmail: {email}\n\nSkills: {skills}\nExperience: {experience}\n\nNote: This is a placeholder response for development purposes."""

    try:
        prompt = f"""Generate a professional resume for:\nName: {name}\nEmail: {email}\nSkills: {skills}\nExperience: {experience}"""
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

def generate_cover_letter(api_key, name, job_title, company, job_description, model, use_placeholder, client):
    if use_placeholder:
        return f"""Placeholder Cover Letter\n========================\nDear Hiring Manager at {company},\n\nMy name is {name}, and I am excited to apply for the role of {job_title}.\nI believe my experience and skills align with the job description: {job_description}.\n\nNote: This is a placeholder response for development purposes."""

    try:
        prompt = f"""Generate a cover letter for:\nName: {name}\nJob Title: {job_title}\nCompany: {company}\nJob Description: {job_description}"""
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