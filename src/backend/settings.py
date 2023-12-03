from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # TODO update to new_grants
    data_path: str = "/datadrive/uspto_json/grants"
    patents_index_path: str = "/datadrive/storage"


settings = Settings()
