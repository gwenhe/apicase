__version__ = '0.1.0'
__description__ = '接口自动化用例、测试的一站式解决方案。'


from apicase.schema import BaseModel
from apicase.client.router import APIRouter
from apicase.client.reuquest import session
from apicase.assertion import JSONAsserter
from apicase.common.enumeration import BodyTypeEnum

bt = BodyTypeEnum
