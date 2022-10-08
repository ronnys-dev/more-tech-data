from typing import List

from pydantic import BaseModel


class NewsResponse(BaseModel):
    news: List[str]
