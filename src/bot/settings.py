from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

BASE_DIR = Path(__file__).parent.parent.parent


@dataclass
class DBConfig:
    """ конфигурации для БД """
    DB_URL = f'sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3'


@dataclass
class BotConfig:
    """ конфигурации для бота """
    TOKEN: str = os.getenv('TOKEN')
    ADMIN_ID: str = os.getenv('ADMIN_ID')

    BROKER = 'redis://localhost:6379/1'


class TaskConfig:
    enable_utc = True
    timezone = 'Europe/London'
