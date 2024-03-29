import json
from dataclasses import dataclass
from pathlib import Path

from src.bot.settings import BASE_DIR


@dataclass
class Resource:
    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            self.__setattr__(attr, value)


def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError as e:
        print(e)


def load_resources():
    resource_path = Path(f'{BASE_DIR}/src/bot/resources')
    resources = {}
    for file_path in resource_path.iterdir():
        if file_path.suffix == '.json' and file_path.is_file():
            resources.update({file_path.stem: read_json_file(file_path)})
    return Resource(**resources)
