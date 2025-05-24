from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.profile import router as profile_router
from routers.resume import router as resume_router
from routers.applications import router as applications_router

app = FastAPI(title="Joblight API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Consider narrowing this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Joblight API is live."}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Routers
app.include_router(profile_router)
app.include_router(resume_router)
app.include_router(applications_router)
