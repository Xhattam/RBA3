from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    hf_token: SecretStr
    hf_api_url: str
    qwen_model_name: str


settings = Settings()  # noqa - F401


