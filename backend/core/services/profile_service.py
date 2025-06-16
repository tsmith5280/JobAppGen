from typing import Dict, Any, List
from pydantic import BaseModel
from ..core.utils.supabase_client import Supabase

class ProfileUpdate(BaseModel):
    full_name: str
    job_title: str
    skills: List[str]
    experience: str

async def get_profile(supabase: Supabase, user_id: str) -> Dict[str, Any] | None:
    response = (
        await supabase.from_("profiles")
        .select("*")
        .eq("id", user_id)
        .single()
        .execute()
    )
    return response.data if response.data else None

async def upsert_profile(supabase: Supabase, user_id: str, profile_data: ProfileUpdate) -> Dict[str, Any]:
    response = (
        await supabase.from_("profiles")
        .upsert({
            "id": user_id,
            "full_name": profile_data.full_name,
            "job_title": profile_data.job_title,
            "skills": profile_data.skills,
            "experience": profile_data.experience
        })
        .execute()
    )
    return response.data[0]