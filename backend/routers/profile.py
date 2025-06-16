from fastapi import APIRouter, Depends, HTTPException
from ..core.utils.supabase_client import get_supabase_client, Supabase
from ..core.services import profile_service

router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("/")
async def get_profile_route(supabase: Supabase = Depends(get_supabase_client)):
    user = (await supabase.auth.get_user()).user
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    profile = await profile_service.get_profile(supabase, user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return profile

@router.patch("/")
async def update_profile_route(
    profile_data: profile_service.ProfileUpdate,
    supabase: Supabase = Depends(get_supabase_client)
):
    user = (await supabase.auth.get_user()).user
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
        
    return await profile_service.upsert_profile(supabase, user.id, profile_data)