from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    prompt: str

@app.post("/chat")
async def chat_with_coach(message: Message):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert job search coach named Virel. Answer questions clearly and only give help related to resumes, cover letters, job interviews, and job hunting."},
            {"role": "user", "content": message.prompt}
        ]
    )
    return {"response": response.choices[0].message.content}