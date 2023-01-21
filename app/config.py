from pydantic import BaseSettings
from env import SSHConfig, DBConfig
import platform

current_os = platform.system()

class Settings(BaseSettings):
    API_VERSION: str = '1.0.0'
    MIN_DB_POOL_SIZE: int = 1
    MAX_DB_POOL_SIZE: int = 5
    allowed_origins = [
        'http://localhost:8080',
        'https://debbs-kitchen.xfilesgenerator.com',
        'https://debbskitchen.net'
    ]

class LocalConfig(Settings, SSHConfig, DBConfig):
    ENV = 'local'

class ProdConfig(Settings, DBConfig):
    ENV = 'prod'


def get_settings():
    print(current_os)
    if current_os == 'Darwin':
        return LocalConfig()
    elif current_os == 'Linux':
        return ProdConfig()
    else:
        raise RuntimeError('Invalid current_os')
