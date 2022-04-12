from enum import Enum


class StatusEnum(str, Enum):
    ON = "ON"
    OFF = "OFF"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class ParameterEnum(str, Enum):
    TEMPERATURE = "temperature"
    PRESSURE = "pressure"
