from typing import Optional

from pydantic import BaseModel, Field


class InferenceRequest(BaseModel):
    model_name: str
    input_text: str
    api_key: Optional[str]
    org_id: Optional[str] = None
    generation_cfg: Optional[dict] = None
    top_k_similar: int = Field(
        description="Number of documents to query from vector db", default=3
    )
