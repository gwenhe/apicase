from enum import Enum
from datetime import datetime
from typing import (
    List, Dict, Set, Tuple, Optional, Union
)
from pydantic import (
    BaseModel as Base, BaseSettings, PyObject, RedisDsn, PostgresDsn, AmqpDsn, Field,
)


def to_camel(string: str) -> str:
    """
    蟒蛇字符转换为小驼峰
    :param string:
    :return:
    """
    s = ''.join(word.capitalize() for word in string.split('_'))
    return s[0].lower() + s[1:]


class BaseModel(Base):
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = False
        # alias_generator = to_camel  有bug，不能用
        smart_union = False
