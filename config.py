from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_STR: str = "/api/v1"
    PROJECT_NAME: str = "Task manager"

    DB_HOST: str = Field("localhost", env="DB_HOST")
    DB_PORT: int = Field(5432, env="DB_PORT")
    DB_USER: str = Field("postgres", env="DB_USER")
    DB_PASSWORD: str = Field("postgres", env="DB_PASSWORD")
    DB_NAME: str = Field("tasks", env="DB_NAME")

    HOST: str = Field("localhost", env="HOST")

    @property
    def DATABASE_URI(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"


settings = Settings()