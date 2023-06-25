from pydantic import BaseModel, Field
from typing import Optional

# Model for JWT Token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None