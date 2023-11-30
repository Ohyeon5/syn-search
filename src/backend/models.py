from pydantic import BaseModel


class InferenceRequest(BaseModel):
    model_name: str
    input_text: str
