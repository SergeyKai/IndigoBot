from .resource import load_resources
from .validators import validate_phone_number as phone_valid
from .validators import normalize_phone_number


def validate_phone_number(phone_number):
    normalized_phone_number = normalize_phone_number(phone_number)
    if phone_valid(normalized_phone_number):
        return normalized_phone_number
    else:
        return False
