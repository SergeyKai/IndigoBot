import re


def normalize_phone_number(phone_number: str):
    phone_number = re.sub(r'\D', '', phone_number)
    if len(phone_number) == 10:
        phone_number = '+7' + phone_number
    return phone_number


def validate_phone_number(phone_number: str):
    pattern = re.compile(r'^\+7\d{10}$')
    if pattern.match(phone_number):
        return True
    else:
        return False
