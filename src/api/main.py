import logging
import argparse

import uvicorn
import json_logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# Project
from config import db, settings
from api.router import api_router

logger = logging.getLogger("app-logger")


app = FastAPI(title=settings.PROJECT_NAME, version=settings.APP_VERSION)


if settings.LOGGING_AS_JSON:
    json_logging.init_fastapi(enable_json=True)
    json_logging.init_request_instrument(app)
    logger.info(f"Will use json_logging as logs formatter")


@app.on_event("startup")
async def app_startup():
    from utils import get_embedding_model

    get_embedding_model()
    logger.info(f"Done get_embedding_model")
    db.connect()


@app.on_event("shutdown")
async def app_shutdown():
    await db.disconnect()


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_STR)

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--log-level",
        action="store",
        dest="log_level",
        help="Logging level",
        default="DEBUG",
        type=str,
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        dest="reload",
        help="Enable auto-reload (code change watch dog)",
        default=False,
    )

    options = parser.parse_args()
    logger.warning(f"parsed args: options={options}")

    # run worker

    uvicorn.run(
        app,
        port=8010,
        host="0.0.0.0",
        log_config=settings.LOG_CONFIG,
        log_level=options.log_level.lower(),
        workers=1,
        reload=options.reload,
        timeout_keep_alive=180,
    )
