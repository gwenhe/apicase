"""
Built-in validate comparators.
"""

import re
from apicase.common.schema import JSONAssertSchema
from typing import Any


def _cast_to_int(expect_value):
    try:
        return int(expect_value)
    except Exception:
        raise AssertionError("%r can't cast to int" % str(expect_value))


def equals(check_value, expect_value):
    assert check_value == expect_value


def less_than(check_value, expect_value):
    assert check_value < expect_value


def less_than_or_equals(check_value, expect_value):
    assert check_value <= expect_value


def greater_than(check_value, expect_value):
    assert check_value > expect_value


def greater_than_or_equals(check_value, expect_value):
    assert check_value >= expect_value


def not_equals(check_value, expect_value):
    assert check_value != expect_value


# def string_equals(check_value, expect_value):
#     assert builtin_str(check_value) == builtin_str(expect_value)


# def length_equals(check_value, expect_value):
#     assert isinstance(expect_value, integer_types)
#     expect_len = _cast_to_int(expect_value)
#     assert len(check_value) == expect_len


def length_greater_than(check_value, expect_value):
    assert isinstance(expect_value, int)
    expect_len = _cast_to_int(expect_value)
    assert len(str(check_value)) > expect_len


# def length_greater_than_or_equals(check_value, expect_value):
#     assert isinstance(expect_value, integer_types)
#     expect_len = _cast_to_int(expect_value)
#     assert len(check_value) >= expect_len
#
#
# def length_less_than(check_value, expect_value):
#     assert isinstance(expect_value, integer_types)
#     expect_len = _cast_to_int(expect_value)
#     assert len(check_value) < expect_len
#
#
# def length_less_than_or_equals(check_value, expect_value):
#     assert isinstance(expect_value, integer_types)
#     expect_len = _cast_to_int(expect_value)
#     assert len(check_value) <= expect_len
#
#
# def contains(check_value, expect_value):
#     assert isinstance(check_value, (list, tuple, dict, basestring))
#     assert expect_value in check_value
#
#
# def contained_by(check_value, expect_value):
#     assert isinstance(expect_value, (list, tuple, dict, basestring))
#     assert check_value in expect_value


def type_match(check_value, expect_value):
    def get_type(name):
        if isinstance(name, type):
            return name
        elif isinstance(name, str):
            try:
                return __builtins__[name]
            except KeyError:
                raise ValueError(name)
        else:
            raise ValueError(name)

    assert isinstance(check_value, get_type(expect_value))


# def regex_match(check_value, expect_value):
#     assert isinstance(expect_value, basestring)
#     assert isinstance(check_value, basestring)
#     assert re.match(expect_value, check_value)
#
#
# def startswith(check_value, expect_value):
#     assert builtin_str(check_value).startswith(builtin_str(expect_value))
#
#
# def endswith(check_value, expect_value):
#     assert builtin_str(check_value).endswith(builtin_str(expect_value))
#
#
# def _cast_to_int(expect_value):
#     try:
#         return int(expect_value)
#     except Exception:
#         raise AssertionError("%r can't cast to int" % str(expect_value))


class AssertJson:
    """
    工具类
    """

    @staticmethod
    def equals(jmespath, expect_value):
        """
        相等
        """
        return JSONAssertSchema(jmespath=jmespath, expectations=expect_value, comparator=equals)

    @staticmethod
    def less_than(jmespath, expect_value):
        """
        小于
        """
        return JSONAssertSchema(jmespath=jmespath, expectations=expect_value, comparator=less_than)

    @staticmethod
    def less_than_or_equals(jmespath, expect_value):
        """
        小于或等于
        """
        return JSONAssertSchema(jmespath=jmespath, expectations=expect_value, comparator=less_than_or_equals)

    @staticmethod
    def greater_than(jmespath, expect_value):
        """
        大于
        """
        return JSONAssertSchema(jmespath=jmespath, expectations=expect_value, comparator=greater_than)

    @staticmethod
    def greater_than_or_equals(jmespath, expect_value):
        """
        大于或等于
        """
        return JSONAssertSchema(jmespath=jmespath, expectations=expect_value, comparator=greater_than_or_equals)

    @staticmethod
    def not_equals(jmespath, expect_value):
        """
        不等于
        """
        return JSONAssertSchema(jmespath=jmespath, expectations=expect_value, comparator=not_equals)

    @staticmethod
    def length_greater_than(jmespath, expect_value: int):
        """
        长度大于
        """
        return JSONAssertSchema(jmespath=jmespath, expectations=expect_value, comparator=length_greater_than)

    @staticmethod
    def type_match(jmespath, expect_value: Any):
        """
        类型匹配
        """
        return JSONAssertSchema(jmespath=jmespath, expectations=expect_value, comparator=type_match)


assertJSON = AssertJson()
