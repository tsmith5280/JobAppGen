from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

from ..core.utils.supabase_client import get_supabase_client, Supabase
from ..core.services import application_service

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
async def get_applications_route(supabase: Supabase = Depends(get_supabase_client)):
    user = (await supabase.auth.get_user()).user
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return await application_service.get_recent_applications(supabase, user.id)

@router.get("/stats", response_model=ApplicationStats)
async def get_stats_route(supabase: Supabase = Depends(get_supabase_client)):
    user = (await supabase.auth.get_user()).user
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return await application_service.get_application_stats(supabase, user.id)

@router.post("/", response_model=Application, status_code=201)
async def create_application_route(
    application_data: application_service.ApplicationCreate,
    supabase: Supabase = Depends(get_supabase_client)
):
    user = (await supabase.auth.get_user()).user
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return await application_service.create_application(supabase, user.id, application_data)