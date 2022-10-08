from typing import Optional

from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.news.api import router as news_router


class ErrorMessage(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: Optional[list[ErrorMessage]]


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)


# api routers
api_router.include_router(news_router)


@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


def init_routers(app: FastAPI) -> None:
    """Initialize all routers in application."""
    app.include_router(api_router, prefix="/api")
