from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str = 'BOT_TOKEN'
    local: bool = 'LOCAL'
    admins: str = 'ADMINS'
    # channel_name: str = '@channelname'
    # positions_limit: int = 100
    # warehouse_rate_to_show: int = 10
    # warehouse_rate_date_format: str = '%d.%m.%Y'

    class Config:
        env_file = '.env'


config = Settings()
