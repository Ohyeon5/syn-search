import os

import openai
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import InferenceRequest

GENERATION_TIMEOUT_SEC = 60

load_dotenv()
app = FastAPI()

origins = [
    "http://localhost:5173",
    "localhost:5173",
    "https://proud-water-0f0a39703.4.azurestaticapps.net",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
async def index():
    return {"message": "Welcome to vlib api!"}


@app.post("/api/chat")
async def chat(request: InferenceRequest):
    client = openai.AzureOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("OPENAI_BASE_URL"),
    )
    chat_completion = client.chat.completions.create(
        model=request.model_name,
        messages=[{"role": "user", "content": request.input_text}],
    )
    return chat_completion


def post_processing(chunk):
    return chunk
