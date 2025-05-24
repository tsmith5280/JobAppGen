from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from core.utils.resume_parser import parse_resume_file
from core.utils.auth import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/resume", tags=["resume"])

# Optional schema for returning parsed result
class ResumeParseResponse(BaseModel):
    full_name: str
    job_title: str
    skills: list[str]
    experience: str

@router.post("/upload", response_model=ResumeParseResponse)
def upload_resume(file: UploadFile = File(...), user=Depends(get_current_user)):
    try:
        parsed = parse_resume_file(file)
        return parsed
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume parsing failed: {str(e)}")
