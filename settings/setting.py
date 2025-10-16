from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field


class DB_settings(BaseSettings):
    db_name: str
    db_port: int
    db_host: SecretStr
    db_user: str
    db_password: SecretStr
    db_echo: bool = False
    db_pool_size: int = Field(gt=0)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def get_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password.get_secret_value()}@{self.db_host.get_secret_value()}:{self.db_port}/{self.db_name}"
    
class Redis_settings(BaseSettings):
    redis_port: int
    redis_host: str
    redis_db: int = Field(ge=0, lt=16)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def get_url(self):
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    
class Email_settings(BaseSettings):
    email_password: SecretStr
    email_login: str
    email_port: int
    email_host: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

class S3_Client(BaseSettings):
    s3_access_key: str
    s3_secret_key: SecretStr
    s3_endpoint_url: str
    s3_bucket_name: str
    s3_region_name: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class Settings(BaseSettings): 
    db_settings: DB_settings = DB_settings()
    redis_settings: Redis_settings = Redis_settings()
    email_settings: Email_settings = Email_settings()
    s3_client: S3_Client = S3_Client()
    jwt_secret: SecretStr
    secret_key: SecretStr
    frontend_url: str
    backend_url: str
    access_token_expries: int
    refresh_token_expries: int
    expries_cookie: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()