import asyncio

import os
import async_timeout
import openai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from models import InferenceRequest

GENERATION_TIMEOUT_SEC = 60

load_dotenv()
app = FastAPI()


@app.get("/api")
async def index():
    return {"message": "Welcome to vlib api!"}


@app.post("/openai_streaming")
async def openai_streaming(request: InferenceRequest) -> StreamingResponse:
    try:
        subscription = await openai.ChatCompletion.acreate(
            model=request.model_name,
            api_key=request.api_key,
            organization=request.org_id,
            messages=request.input_text,
            stream=True,
            **request.generation_cfg,
        )

        return StreamingResponse(
            stream_generator(subscription), media_type="text/event-stream"
        )
    except openai.OpenAIError:
        raise HTTPException(status_code=500, detail="OpenAI call failed")


async def stream_generator(subscription):
    async with async_timeout.timeout(GENERATION_TIMEOUT_SEC):
        try:
            async for chunk in subscription:
                # post_processing can be any function that takes the chunk and returns a string
                yield post_processing(chunk)
        except asyncio.TimeoutError:
            raise HTTPException(status_code=504, detail="Stream timed out")


@app.post("/chat")
async def chat(request: InferenceRequest):
    client = openai.AzureOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),  
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("OPENAI_BASE_URL")
        )

    chat_completion = client.chat.completions.create(
        model=request.model_name,
        messages=[{"role": "user", "content": request.input_text}],
    )
    return chat_completion


def post_processing(chunk):
    return chunk
