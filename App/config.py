from pydantic_settings import BaseSettings,SettingsConfigDict


_base_model_config =  SettingsConfigDict(
        env_file = "./.env",
        env_ignore_empty=True,
        extra="ignore",
    )

class DatabaseSettings(BaseSettings):
    POSTGRES_SERVER :str
    POSTGRES_PORT : int
    POSTGRES_USER :str
    POSTGRES_PASSWORD : str
    POSTGRES_DB : str
    POSTGRES_URL :str

    model_config = _base_model_config

class JWTSettings(BaseSettings):
    JWT_SECRET_KEY : str
    JWT_ALGORITHM : str

    model_config = _base_model_config

settings = DatabaseSettings()
security_settings = JWTSettings()