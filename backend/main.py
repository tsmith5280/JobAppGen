from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.profile import router as profile_router
from routers.resume import router as resume_router
from routers.applications import router as applications_router
from dotenv import load_dotenv
load_dotenv()
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

app = FastAPI(title="Joblight API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Add port 3001 just in case
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

# Routers (attach after app is created)
from routers import generator
app.include_router(generator.router)
app.include_router(profile_router)
app.include_router(resume_router)
app.include_router(applications_router)
