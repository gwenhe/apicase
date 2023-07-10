__version__ = '0.1.6'
__description__ = '接口自动化用例、测试的一站式解决方案。'

import requests
from apicase.schema import BaseModel
from apicase.client.router import APIRouter
from apicase.client.reuquest import APIRequest, HttpSession
from apicase.client.reuquest import session
from apicase.assertion.comparators import assertJSON, AssertJson
from apicase.assertion.diff import DiffJson
from apicase.common.enumeration import (
    BodyTypeEnum,
)
from apicase.common.schema import (
    RequestSchema,
)
from apicase.common.exception import (
    JsonAssertError
)
from apicase.common.logger import log
from apicase.setting import Settings, BaseSettingSchema

bt = BodyTypeEnum
