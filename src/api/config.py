from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_core import MultiHostUrl
from sqlalchemy.orm import declarative_base
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from pydantic_core.core_schema import ValidationInfo

__all__ = [
    "settings",
    "DeclarativeBase",
    "Database",
    "db",
]


class Settings(BaseSettings):
    API_STR: str = "/api"
    APP_VERSION: str = "0.1.0"
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    PROJECT_NAME: str

    LOGGING_LEVEL: str
    LOGGING_FORMAT: str = "[%(asctime)s: %(levelname)9s] %(message)s"
    LOGGING_AS_JSON: bool = False

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @classmethod
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # DB
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB_NAME: str
    DATABASE_URI: MultiHostUrl | None = None

    @field_validator("DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_uri(cls, v: str | None, values: ValidationInfo) -> MultiHostUrl:
        if isinstance(v, str):
            return PostgresDsn(v)
        return PostgresDsn(
            f"postgresql+asyncpg://"
            f"{values.data['POSTGRES_USER']}:"
            f"{values.data['POSTGRES_PASSWORD']}@"
            f"{values.data['POSTGRES_HOST']}:"
            f"{values.data['POSTGRES_PORT']}/"
            f"{values.data['POSTGRES_DB_NAME']}"
        )

    LOG_CONFIG: dict | None = None

    @field_validator("LOG_CONFIG", mode="before")
    @classmethod
    def assemble_log_config(cls, v: str | None, values: ValidationInfo) -> dict:
        log_level = values.data["LOGGING_LEVEL"]
        log_format = values.data["LOGGING_FORMAT"]
        log_as_json = values.data["LOGGING_AS_JSON"]
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "()": "json_logging.JSONLogFormatter" if log_as_json else "uvicorn.logging.DefaultFormatter",
                    "fmt": log_format,
                    # "fmt": "%(levelprefix)s %(asctime)s %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    # "use_colors": None,
                },
                "access": {
                    "()": "json_logging.JSONLogFormatter" if log_as_json else "uvicorn.logging.AccessFormatter",
                    "fmt": log_format,
                    # "fmt": '%(levelprefix)s %(asctime)s %(client_addr)s - "%(request_line)s" %(status_code)s',
                    # noqa: E501
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",
                },
                "access": {
                    "formatter": "access",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                "uvicorn": {"handlers": ["default"], "level": log_level},
                "uvicorn.error": {"level": log_level},
                "uvicorn.access": {"handlers": ["access"], "level": log_level, "propagate": False},
                "app-logger": {"handlers": ["default"], "level": log_level},
            },
        }

    class Config:
        case_sensitive = True


settings = Settings()

DeclarativeBase = declarative_base()


class Database:
    def __init__(self):
        self.__session = None
        self.engine = create_async_engine(
            str(settings.DATABASE_URI),
        )

    def connect(self):
        self.__session = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )

    async def disconnect(self):
        await self.engine.dispose()

    @staticmethod
    async def get_db_session():
        async with db.__session() as session:
            yield session


db = Database()
