from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ETH_RPC_URL: str
    ETH_CHAIN_ID: int = 1

    class Config:
        env_file = ".env"


settings = Settings()