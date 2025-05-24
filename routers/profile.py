from fastapi import APIRouter, Depends, HTTPException
from core.utils.auth import get_current_user
from core.utils.profile_api import get_user_profile, upsert_user_profile

router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/")
def fetch_profile(user=Depends(get_current_user)):
    user_id = user["id"]
    profile = get_user_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.post("/")
def save_profile(data: dict, user=Depends(get_current_user)):
    user_id = user["id"]
    result = upsert_user_profile(user_id, data)
    return {"status": "success", "profile": result}
