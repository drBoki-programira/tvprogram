from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    database: str
    user: str
    password: str
    host: str
    port: int


settings = DBSettings()

CHANNELS = ['hbo',
            'hbo-2',
            'hbo-3',
            'cinestar-tv-action-thriller',
            'cinestar-tv-fantasy',
            'cinestar-tv-comedy',
            'cinestar-tv-premiere-1',
            'cinestar-tv-premiere-2']

START_URL = 'https://naslovi.net/tv-program/'

SELECTORS = ['.time', '.category', '.title', '.descr']
