import re


def normalize_phone_number(phone_number: str):
    """
    Функция для форматирования номера телефона
    :param phone_number: str: номер телефона
    :return: str: номер телефона в формате +79998883322
    """
    phone_number = re.sub(r'\D', '', phone_number)
    if len(phone_number) == 10:
        phone_number = '+7' + phone_number
    return phone_number


def validate_phone_number(phone_number: str):
    """
    Функция для проверки корректности номера телефона
    :param phone_number: str: номер телефона
    :return: bool
    """
    pattern = re.compile(r'^\+7\d{10}$')
    if pattern.match(phone_number):
        return True
    else:
        return False
