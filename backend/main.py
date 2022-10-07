import uvicorn  # type: ignore
from config.logging import init_logging
from config.middlewares import init_middleware
from config.routers import init_routers
from config.settings import SERVER_HOST, SERVER_PORT
from fastapi import FastAPI

init_logging()


def init_webapi() -> FastAPI:
    """Create the Web API framework."""
    webapi = FastAPI(
        title="Fast Api microservice",
        docs_url="/swagger",
        openapi_url="/docs/openapi.json",
        redoc_url="/docs",
    )
    init_middleware(app=webapi)
    init_routers(app=webapi)
    return webapi


app = init_webapi()


if __name__ == "__main__":
    uvicorn.run("main:app", host=SERVER_HOST, port=SERVER_PORT, reload=True)
