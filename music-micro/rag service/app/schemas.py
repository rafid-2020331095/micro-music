from pydantic import BaseModel
from typing import Optional


class UploadResponse(BaseModel):
    song_id: str
    title: Optional[str]
    chunks_stored: int


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    answer: str
    source_chunks: list
