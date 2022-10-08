from fastapi import APIRouter

from src.news.analyze.news_recommendation_model import get_recommendations
from src.news.constants import Role
from src.news.schemas import NewsResponse
from src.news.services.glafbuh_parser import glafbuh_parser
from src.news.services.rb_parser import rb_parser

router = APIRouter()


@router.get('/relevant_news', response_model=NewsResponse)
async def get_relevant_news(role: Role) -> NewsResponse:
    news_glafbuh = glafbuh_parser()
    news_rb = rb_parser()
    relevant = get_recommendations(news_rb + news_glafbuh, role=role)
    response = NewsResponse(news=relevant)
    return response
