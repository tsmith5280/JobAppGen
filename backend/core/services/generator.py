from core.utils.auth import get_current_user
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from core.services.ai_resume_writer import generate_resume_with_gpt

router = APIRouter()

class Profile(BaseModel):
    full_name: str
    job_title: str
    skills: List[str]
    experience: str

class TargetJob(BaseModel):
    job_title: str
    company: str
    description: str

class ResumeRequest(BaseModel):
    profile: Profile
    target: TargetJob

@router.post("/generate_resume/")
def generate_resume(data: ResumeRequest):
    profile_dict = data.profile.dict()
    target_dict = data.target.dict()

    resume_text = generate_resume_with_gpt(profile_dict, target_dict)

    # Basic match score logic (you can keep or improve this later)
    skills = set([s.lower() for s in profile_dict["skills"]])
    job_text = target_dict["description"].lower()
    matched = [s for s in skills if s in job_text]
    score = int((len(matched) / max(len(skills), 1)) * 100)

    return {
        "resume": resume_text,
        "score": score,
        "matched_skills": matched,
        "recommendation": "⚠️ Consider updating your profile — skill match is low." if score < 70 else ""
    }
