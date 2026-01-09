from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        case_sensitive = False
    )
    open_weather_map_api_key: str
    database_url: str = "sqlite:///weather_app.db"  
    weather_api_base_url: str = "https://api.openweathermap.org/data/2.5"
    weather_api_timeout: float = 10.0

settings = Settings()