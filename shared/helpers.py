import uuid


def to_camel(value: str) -> str:
    return "".join(word.capitalize() if idx != 0 else word for idx, word in enumerate(value.split("_")))


def generate_uuid() -> str:
    return str(uuid.uuid4())
