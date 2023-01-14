from enum import Enum


class BodyTypeEnum(Enum):
    NULL = None
    JSON = 'JSON'
    TEXT = 'TEXT'
    XML = 'XML'
    FORM_URLENCODED = 'x-www-form-urlencoded'
    FORM_DATA = 'form-data'


class ComparatorEnum(Enum):
    EQUAL = '='
    GREATER = '>'
    LESS = '<'
