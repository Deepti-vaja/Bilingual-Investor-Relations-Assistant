from pydantic import BaseModel, Field
from typing import Literal

class ChatMessage(BaseModel):
    """
    Schema for an individual chat message, used for type safety and validation.
    """
    role: Literal["user", "AI"] = Field(..., description="The role of the message sender.")
    content: str = Field(..., description="The content of the message.")

class InferenceRequest(BaseModel):
    """
    Schema representing an incoming query from a user.
    """
    query: str = Field(..., min_length=1, description="The textual query asked by the user.")
