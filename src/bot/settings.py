from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

BASE_DIR = Path(__file__).parent.parent.parent


@dataclass
class DBConfig:
    DB_URL = f'sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3'


@dataclass
class BotConfig:
    TOKEN: str = os.getenv('TOKEN')


print(BASE_DIR)
