from pydantic import BaseModel
from typing import Any
class Event(BaseModel):
    user_id: int
    timestamp: str
    metadata: Any
