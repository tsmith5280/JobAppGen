def compare_resume_to_job(api_key, resume_text, job_description, model, use_placeholder, client):
    if use_placeholder:
        return "Match Score: 82/100\n\n- Strong alignment in skills\n- Relevant work history\n- Could improve formatting for ATS"

    try:
        prompt = (
            "Evaluate the following resume against the job description.\n\n"
            "Return a match score out of 100, and list 2–3 key observations on how well the resume fits.\n\n"
            f"Resume:\n{resume_text}\n\n"
            f"Job Description:\n{job_description}"
        )
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a resume scoring assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error scoring resume: {str(e)}"
