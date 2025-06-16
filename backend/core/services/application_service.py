from typing import List, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from ..core.utils.supabase_client import Supabase

class ApplicationCreate(BaseModel):
    job_title: str
    company_name: str
    status: str
    application_date: datetime

async def get_recent_applications(supabase: Supabase, user_id: str) -> List[Dict[str, Any]]:
    response = (
        await supabase.from_("applications")
        .select("id, job_title, company_name, status, application_date")
        .eq("user_id", user_id)
        .order("application_date", desc=True)
        .limit(4)
        .execute()
    )
    return response.data

async def get_application_stats(supabase: Supabase, user_id: str) -> Dict[str, int]:
    sent_res = await supabase.from_("applications").select("id", count="exact").eq("user_id", user_id).execute()
    interview_res = await supabase.from_("applications").select("id", count="exact").eq("user_id", user_id).eq("status", "Interview").execute()
    offer_res = await supabase.from_("applications").select("id", count="exact").eq("user_id", user_id).eq("status", "Offer").execute()

    return {
        "applications_sent": sent_res.count or 0,
        "interviews": interview_res.count or 0,
        "offers": offer_res.count or 0,
    }

async def create_application(supabase: Supabase, user_id: str, application_data: ApplicationCreate) -> Dict[str, Any]:
    response = (
        await supabase.table("applications")
        .insert({**application_data.dict(), "user_id": user_id})
        .execute()
    )
    return response.data[0]