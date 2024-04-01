import json
from dataclasses import dataclass
from pathlib import Path

from src.bot.settings import BASE_DIR


@dataclass
class Resource:
    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            self.__setattr__(attr, value)

    def add_resource(self, resource_name, resource):
        self.__setattr__(resource_name, resource)


def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError as e:
        print(e)


def load_image_resources(resource_obj: Resource = None) -> Resource:
    resource_path = Path(f'{BASE_DIR}/src/bot/resources/images')
    resources = {}
    for file_path in resource_path.iterdir():
        if file_path.is_file():
            resources.update({file_path.stem: file_path})
    if resource_obj:
        resource_obj.add_resource('images', resources)
    else:
        resource_obj = Resource(images=resources)
    return resource_obj


def load_resources() -> Resource:
    resource_path = Path(f'{BASE_DIR}/src/bot/resources')
    resources = {}
    for file_path in resource_path.iterdir():
        if file_path.suffix == '.json' and file_path.is_file():
            resources.update({file_path.stem: read_json_file(file_path)})

    resource_obj = Resource(**resources)
    return load_image_resources(resource_obj)
