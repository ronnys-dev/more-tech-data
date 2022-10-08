from fastapi import APIRouter

from src.news.constants import Role

router = APIRouter()


@router.get('relevant_news')
async def get_relevant_news(role: Role):
    return {'hello': 'world'}
