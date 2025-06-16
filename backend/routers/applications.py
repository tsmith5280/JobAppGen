from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from datetime import datetime
from core.utils.supabase_client import get_supabase_client, Supabase # THIS LINE IS CHANGED

router = APIRouter(
    prefix="/applications",
    tags=["applications"],
)

class Application(BaseModel):
    id: str
    job_title: str
    company_name: str
    status: str
    application_date: datetime

class ApplicationStats(BaseModel):
    applications_sent: int
    interviews: int
    offers: int

@router.get("/", response_model=List[Application])
async def get_recent_applications(
    supabase: Supabase = Depends(get_supabase_client)
):
    """
    Fetches the 4 most recent applications for the authenticated user
    to display on the dashboard.
    """
    user = (await supabase.auth.get_user()).user # Use await for async client
    if not user:
        return [] # Or raise HTTPException
    
    response = (
        supabase.from_("applications")
        .select("id, job_title, company_name, status, application_date")
        .eq("user_id", user.id)
        .order("application_date", desc=True)
        .limit(4) # Fetching 4 for a 2x2 grid layout
        .execute()
    )
    return response.data

@router.get("/stats", response_model=ApplicationStats)
async def get_application_stats(
    supabase: Supabase = Depends(get_supabase_client)
):
    """
    Fetches aggregate application statistics for the authenticated user.
    """
    user = (await supabase.auth.get_user()).user # Use await for async client
    if not user:
        return ApplicationStats(applications_sent=0, interviews=0, offers=0)

    # Supabase returns the count in a different way for different versions.
    # We will perform individual queries for robustness.
    sent_count_res = supabase.from_("applications").select("id", count="exact").eq("user_id", user.id).execute()
    interview_count_res = supabase.from_("applications").select("id", count="exact").eq("user_id", user.id).eq("status", "Interview").execute()
    offer_count_res = supabase.from_("applications").select("id", count="exact").eq("user_id", user.id).eq("status", "Offer").execute()

    return {
        "applications_sent": sent_count_res.count or 0,
        "interviews": interview_count_res.count or 0,
        "offers": offer_count_res.count or 0,
    }