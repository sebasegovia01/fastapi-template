from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[int] = None
    userId: str
    userPhoneNumber: str
