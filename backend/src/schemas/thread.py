from pydantic import BaseModel
from typing import List
from src.schemas.message import APIMessage
from datetime import datetime


class APIThread(BaseModel):
    id: int
    title: str | None
    created_at: datetime
    messages: List[APIMessage]
    created_at: datetime


class RestGetThreadsJSONResponse(BaseModel):
    threads: list[APIThread]
