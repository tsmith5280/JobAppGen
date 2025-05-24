from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from core.utils.auth import get_current_user
from core.utils.profile_api import get_user_profile, upsert_user_profile

router = APIRouter(prefix="/profile", tags=["profile"])

# --- Schema ---
class ProfileData(BaseModel):
    full_name: str
    job_title: str
    skills: list[str]
    experience: str

# --- Routes ---
@router.get("/", response_model=ProfileData)
def fetch_profile(user=Depends(get_current_user)):
    user_id = user["id"]
    profile = get_user_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.post("/", response_model=dict)
def save_profile(data: ProfileData, user=Depends(get_current_user)):
    user_id = user["id"]
    result = upsert_user_profile(user_id, data.dict())
    return {"status": "success", "profile": result}
