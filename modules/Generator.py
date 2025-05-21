def generate_resume(api_key, name, email, skills, experience, model, use_placeholder, client):
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


def generate_cover_letter(api_key, name, job_title, company, job_description, model, use_placeholder, client):
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
