from pydantic import BaseSettings


class Configs(BaseSettings):
    secret_key: str
    mongodb: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


get_configs = (lambda: Configs())
