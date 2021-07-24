from typing import Dict, Any, Optional, List

from pydantic import BaseModel


class Post(BaseModel):
    id: int
    title: str
    body: str
    user: Dict[str, Any]
    comments: Optional[List[Dict[str, Any]]]


class CreatePostParams(BaseModel):
    title: str
    body: str
    userId: int


class EditPostParams(BaseModel):
    title: str
    body: str

