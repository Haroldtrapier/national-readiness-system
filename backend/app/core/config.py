from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "National Readiness System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite:///./national_readiness.db"

    NWS_API_BASE: str = "https://api.weather.gov"
    NWS_USER_AGENT: str = "NationalReadinessSystem/1.0"
    USGS_EARTHQUAKE_API: str = "https://earthquake.usgs.gov/fdsnws/event/1"
    SPC_BASE_URL: str = "https://www.spc.noaa.gov"
    NHC_BASE_URL: str = "https://www.nhc.noaa.gov"

    HAZARD_REFRESH_MINUTES: int = 15
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
