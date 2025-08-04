from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import List, Union, Any


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
        json_encoders={},
        # Desabilita parsing automático de JSON para evitar conflitos
        env_parse_none_str="",
    )
    
    project_name: str = "Ser Recicla API"
    version: str = "1.0.0"
    environment: str = Field(default="development", alias="ENVIRONMENT")
    
    secret_key: str = Field(default="your_secret_key", alias="SECRET_KEY")
    debug: bool = Field(default=False, alias="DEBUG")
    
    database_url: str = Field(default="sqlite:///./test.db", alias="DATABASE_URL")
    
    jwt_secret_key: str = Field(default="your_jwt_secret_key", alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=15, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=15, alias="REFRESH_TOKEN_EXPIRE_DAYS")
    
    cors_origins: Union[str, List[str]] = Field(
        default="http://localhost:3000",
        alias="CORS_ORIGINS"
    )
    
    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v: Any) -> List[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        elif isinstance(v, list):
            return v
        return ["http://localhost:3000"]


settings = Settings()
