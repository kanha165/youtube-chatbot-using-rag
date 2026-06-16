from pydantic import BaseModel


class VideoRequest(BaseModel):
    url: str


class ChatRequest(BaseModel):
    question: str


class VideoResponse(BaseModel):
    success: bool
    message: str


class ChatResponse(BaseModel):
    answer: str