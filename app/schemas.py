from typing import List, Optional, Any, Literal
from pydantic import BaseModel

class Joke(BaseModel):
    id: int
    type: str
    setup: str
    punchline: str

class JokesList(BaseModel):
    count: int
    items: List[Joke]
    note: Optional[str]

class Error(BaseModel):
    error: Literal["bad_request", "not_found", "upstream_error", "upstream_timeout"]
    message: str
    details: Optional[Any]
