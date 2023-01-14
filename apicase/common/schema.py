from pydantic import BaseModel, Field
from typing import Optional, Union, Dict, List, Any
from apicase.common.enumeration import (
    BodyTypeEnum, ComparatorEnum
)


class RequestSchema(BaseModel):
    url: str = Field(..., description='请求路径')
    method: str = Field(..., description='请求方法')
    body_type: BodyTypeEnum = Field(BodyTypeEnum.NULL, description='请求体类型')
    data: Union[str, Dict, List, bytes] = Field(None, description='请求体')
    files: Dict = Field({}, description='上传的文件')
    path_params: Dict = Field({}, description='路径参数')
    query_params: Dict = Field({}, description='查询参数')
    headers: Dict = Field({}, description='请求头')
    cookies: Dict = Field({}, description='请求cookie')
    timeout: float = Field(None, description='请求超时时间')
    other: Dict = Field(None, description='其他')
    description: str = None


class JSONAssertSchema(BaseModel):
    expression: str = Field(...)
    comparator: ComparatorEnum
    value: Any = Field(...)
