# 設定ファイルを読み込むための設定ファ
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    secret_key: str
    sqlalchemy_database_url: str

    model_config = SettingsConfigDict(env_file=".env")


# .envの設定値を含む、settingインスタンスが取得できる
# @lru_cache()とすることで設定値の取得をキャッシュする
@lru_cache()
def get_settings():
    return Settings()
