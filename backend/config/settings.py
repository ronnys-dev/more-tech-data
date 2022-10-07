import os

from starlette.config import Config

config = Config("../.env")


# application
DEBUG = config("DEBUG", cast=bool, default=True)
TLS = config("TLS", default="off")
SERVER_HOST = config("SERVER_HOST", default="localhost")
SERVER_PORT = config("SERVER_PORT", cast=int, default="8000")
SITE_URL = (
    f"https://{SERVER_HOST}" if TLS == "on" else f"http://{SERVER_HOST}:{SERVER_PORT}"
)
ENVIRONMENT = config("ENVIRONMENT", default="development")  # development/production
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# logging
LOG_LEVEL = config("LOG_LEVEL", default="WARNING")
JSON_LOGS = config("JSON_LOGS", cast=bool, default=False)
