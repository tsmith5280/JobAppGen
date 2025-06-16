import openai
import os
import json
from typing import Dict, Any

# It's assumed OPENAI_API_KEY is loaded into the environment where this app runs.
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_resume_with_gpt(profile: Dict[str, Any], target: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates tailored resume components by calling the OpenAI API.

    This function constructs a detailed prompt for an AI to act as a resume writer,
    requesting a structured JSON output containing a professional summary and
    tailored experience bullet points.

    Args:
        profile: A dictionary containing the user's professional info.
        target: A dictionary containing the target job's info.

    Returns:
        A dictionary with structured resume components. On failure, it returns
        a dictionary containing an 'error' key.
    """
    
    skills_str = ', '.join(profile.get('skills', []))
    experience_str = str(profile.get('experience', '')) 

    prompt = f"""
You are an expert resume writer API. Your task is to generate tailored resume components based on the provided user profile and target job.

**User Profile Analysis:**
- Current Title: {profile.get('job_title', 'N/A')}
- Skills: {skills_str}
- Experience: {experience_str}

**Target Job Analysis:**
- Title: {target.get('job_title', 'N/A')}
- Company: {target.get('company', 'N/A')}
- Description: {target.get('description', 'N/A')}

**Instructions:**
Generate a professional summary and 3-5 experience bullet points that align the user's profile with the target job.

**Output Format:**
Respond with a single, minified JSON object with two keys: "professional_summary" (string) and "experience_bullets" (array of strings). Do not include any text or markdown formatting outside of the JSON object.
"""

    try:
        response = openai.ChatCompletion.create(
            # gpt-4-turbo-preview is recommended for speed and JSON mode support.
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides output in valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        
        response_content = response["choices"][0]["message"]["content"]
        return json.loads(response_content)

    except json.JSONDecodeError as e:
        # The AI failed to return valid JSON. This is a critical failure to log.
        print(f"JSONDecodeError: {e}\nRaw AI Response: {response_content}") 
        return {"error": "AI response was not in valid JSON format."}
    except Exception as e:
        # Handle API errors, network issues, etc.
        print(f"An unexpected OpenAI API error occurred: {e}")
        return {"error": "An error occurred while communicating with the AI service."}