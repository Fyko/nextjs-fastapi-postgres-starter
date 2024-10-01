from pydantic import BaseModel

class APIUser(BaseModel):
    id: int
    name: str
