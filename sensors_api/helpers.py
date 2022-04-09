import string
import random
import uuid


def api_key_generator(length=64) -> str:
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(length)
    )


def to_camel(value: str) -> str:
    return "".join(
        word.capitalize() if idx != 0 else word
        for idx, word in enumerate(value.split("_"))
    )


def uuid_generator() -> str:
    return str(uuid.uuid4())
