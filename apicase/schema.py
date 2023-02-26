import warnings
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

    def dict(
            self,
            *,
            include: Optional[Union['AbstractSetIntStr', 'MappingIntStrAny']] = None,
            exclude: Optional[Union['AbstractSetIntStr', 'MappingIntStrAny']] = None,
            by_alias: bool = False,
            skip_defaults: Optional[bool] = None,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = True,
    ) -> 'DictStrAny':
        """
        Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

        重写覆盖父类转字典方法，差异内容如下：
            exclude_none（排除等于none的字段） 修改为默认等于True，大多数接口传null代表修改为空，实际不修改某一内容应不传递参数
        """
        if skip_defaults is not None:
            warnings.warn(
                f'{self.__class__.__name__}.dict(): "skip_defaults" is deprecated and replaced by "exclude_unset"',
                DeprecationWarning,
            )
            exclude_unset = skip_defaults

        return dict(
            self._iter(
                to_dict=True,
                by_alias=by_alias,
                include=include,
                exclude=exclude,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
            )
        )
