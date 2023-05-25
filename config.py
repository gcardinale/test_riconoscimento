from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    log_level: str = "DEBUG"
    endpoint: str 
    auth_token: str
    model_path:str 

    class Config:
        if 'DEV' in os.environ:
            env_file = "local.env"
        else:
            # Use a different env file or no file at all
            env_file = ".env"


settings = Settings()
