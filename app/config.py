from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    KEYCLOAK_URL:str
    KEYCLOAK_REALM:str
    KEYCLOAK_CLIENT_ID:str
    KEYCLOAK_CLIENT_SECRET:str


    model_config = SettingsConfigDict(env_file=".env")


    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()