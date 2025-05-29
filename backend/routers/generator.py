from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

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
    profile = data.profile
    target = data.target

    def match_score(profile, job):
        skills = set([s.lower() for s in profile.skills])
        job_text = job.description.lower()
        matched = [s for s in skills if s in job_text]
        score = int((len(matched) / max(len(skills), 1)) * 100)
        return score, matched

    score, matched = match_score(profile, target)

    resume = f"""
{profile.full_name}
{profile.job_title}

Skills: {', '.join(profile.skills)}

Experience:
{profile.experience}

Targeting: {target.job_title} at {target.company}
Job Description: {target.description}
"""

    return {
        "resume": resume.strip(),
        "score": score,
        "matched_skills": matched,
        "recommendation": "⚠️ Consider updating your profile — skill match is low." if score < 70 else ""
    }
