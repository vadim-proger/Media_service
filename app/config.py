from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DB_HOST: str
    DB_USER: str
    DB_SECRET_KEY: str
    DB_NAME: str
    DB_PORT: int
    UPLOAD_DIR: str

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_SECRET_KEY}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
