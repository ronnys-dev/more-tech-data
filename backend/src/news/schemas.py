from typing import List

from pydantic import BaseModel


class NewsResult(BaseModel):
    url: str
    trend: str
    insight: str


class NewsResponse(BaseModel):
    news: List[NewsResult]
