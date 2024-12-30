from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    deepseek_api_key: str
    deepseek_api_base_url: str = "https://api.deepseek.com"

    class Config:
        env_file = ".env"

settings = Settings()
