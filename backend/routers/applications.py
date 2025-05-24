from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List

from core.utils.auth import get_current_user
from core.utils.applications_api import get_user_applications, insert_application

router = APIRouter(prefix="/applications", tags=["applications"])

# --- Schemas ---
class ApplicationIn(BaseModel):
    job_title: str
    company: str
    status: str
    date: str  # Consider using datetime.date if you want tighter control
    notes: str

class ApplicationOut(ApplicationIn):
    id: int  # Optional: if your DB returns an ID field

# --- Routes ---
@router.get("/", response_model=List[ApplicationIn])
def fetch_applications(user=Depends(get_current_user)):
    user_id = user["id"]
    apps = get_user_applications(user_id)
    return apps

@router.post("/", response_model=dict)
def add_application(data: ApplicationIn, user=Depends(get_current_user)):
    user_id = user["id"]
    try:
        result = insert_application(user_id, **data.dict())
        return {"status": "success", "data": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert application: {str(e)}")
