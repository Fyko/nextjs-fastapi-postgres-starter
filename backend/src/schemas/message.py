from pydantic import BaseModel
from typing import List
from datetime import datetime
import enum
from sqlalchemy import Integer, Enum

class MessageSender(enum.Enum):
    human = "human"
    system = "system"

class APIMessage(BaseModel):
    id: int
    thread_id: int
    sender: MessageSender
    content: str
    created_at: datetime

class RestPostCreateMessageJSONRequest(BaseModel):
    content: str
