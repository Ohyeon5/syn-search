import asyncio
import os

import async_timeout
import openai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from llama_index import (
    ServiceContext,
    StorageContext,
    load_index_from_storage,
    set_global_service_context,
)
from llama_index.embeddings import AzureOpenAIEmbedding
from llama_index.llms import AzureOpenAI

from .models import InferenceRequest
from .settings import settings

GENERATION_TIMEOUT_SEC = 60

load_dotenv()
llm = AzureOpenAI(
    engine="gpt-35-turbo",
    model="gpt-35-turbo",
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("OPENAI_BASE_URL"),
)

embed_model = AzureOpenAIEmbedding(
    azure_deployment="text-embedding-ada-002",
    model="text-embedding-ada-002",
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("OPENAI_BASE_URL"),
    embed_batch_size=1,
)

service_context = ServiceContext.from_defaults(
    llm=llm,
    embed_model=embed_model,
)

set_global_service_context(service_context)

app = FastAPI()

# Load vector db
storage_context = StorageContext.from_defaults(persist_dir=settings.patents_index_path)
patent_index = load_index_from_storage(storage_context)


@app.get("/api")
async def index():
    return {"message": "Welcome to vlib api!"}


@app.post("/openai_streaming")
async def openai_streaming(request: InferenceRequest) -> StreamingResponse:
    client = openai.AsyncAzureOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("OPENAI_BASE_URL"),
    )
    try:
        chat_completion = await client.chat.completions.create(
            model=request.model_name,
            messages=[{"role": "user", "content": request.input_text}],
            stream=True,
        )

        return StreamingResponse(
            stream_generator(chat_completion), media_type="text/event-stream"
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
def chat(request: InferenceRequest):
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


async def astreamer(generator):
    try:
        for i in generator:
            yield (i)
            await asyncio.sleep(0.1)
    except asyncio.CancelledError:
        print("cancelled")


@app.post("/q_and_a")
async def q_and_a(request: InferenceRequest) -> StreamingResponse:
    try:
        query_engine = patent_index.as_query_engine(
            streaming=True, similarity_top_k=request.top_k_similar
        )
        response_stream = query_engine.query(request.input_text)
        return StreamingResponse(
            astreamer(response_stream.response_gen), media_type="text/event-stream"
        )
    except openai.OpenAIError:
        raise HTTPException(status_code=500, detail="OpenAI call failed")


def post_processing(chunk):
    print("CHUNK!!!!")
    print(chunk)
    reply = chunk.choices[0].delta.content
    print(reply)
    if reply is None:
        return ""
    return str(reply)
