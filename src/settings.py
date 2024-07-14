from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "N8's Website"
    app_username: str
    app_password: str

    model_config = SettingsConfigDict(env_file=".env")
    