from fastapi import FastAPI
from src.core.middleware import ExceptionMiddleware


def init_middleware(app: FastAPI) -> None:
    """Initialize all middlewares in application."""
    app.add_middleware(ExceptionMiddleware)
