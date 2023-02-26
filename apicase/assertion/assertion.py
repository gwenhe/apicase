from typing import Union, List, Any
import jmespath
from apicase.common.exception import JsonAssertError
from apicase.common.enumeration import ComparatorEnum, CheckResultEnum
from apicase.common.schema import JSONAssertSchema


class Asserter(object):

    def _assert(self):
        pass


class JSONAsserter(Asserter):
    """
    json 断言器
    """
    assert_list = List[JSONAssertSchema]
    assert_results_list = List

    def __init__(self, assert_list: List[JSONAssertSchema], response_json: Union[dict, list],
                 equal_type: bool = True, ):
        self.assert_list = assert_list
        self.equal_type = equal_type
        # self.init_data()
        self.json_assert(response_json)

    # def init_data(self):
    #     """
    #     将断言列表转换为JSONAssertSchema 格式
    #     :return:
    #     """
    #     assert_list = []
    #     for i in self.a_list:
    #         assert_list.append(
    #             JSONAssertSchema(jmespath=i[0], comparator=i[1], expectations=i[2])
    #         )
    #     self.assert_list = assert_list

    def json_assert(self, response_json: Union[dict, list]):
        """
        json断言
        :param response_json: 请求响应json
        :return:
        """
        assert_results_list = []
        for i in self.assert_list:
            i.value = jmespath.search(i.jmespath, response_json)
            try:
                i.comparator(i.value, i.expectations)
            except AssertionError:
                i.check = CheckResultEnum.FAIL
            else:
                i.check = CheckResultEnum.PASS
            assert_results_list.append(i)
        self.assert_results_list = assert_results_list
        # self._assert()

    # def _assert(self):
    #     error_list = []
    #     for i in self.assert_results_list:
    #         if not i.check:
    #             error_list.append(i)
    #     error_str = ''
    # for i in error_list:
    #     assert_example = i[2]
    #     value = str(assert_example.value)
    #     assert_value = str(i[0])
    #     comparator = assert_example.comparator
    #     expression = assert_example.expression
    #     error_str += '\n\t JSON.{expression} {comparator} {value} \t' \
    #                  'But: {assert_value} not {comparator} {value}'.format(expression=expression,
    #                                                                        comparator=comparator.value,
    #                                                                        value=value,
    #                                                                        assert_value=assert_value,
    #                                                                        )
    # raise JsonAssertError('JSON 断言失败' + error_str)
    # print('断言通过', str(self.assert_results_list))


class ResponseAsserter(Asserter):
    pass


class CustomAsserter(Asserter):

    def __init__(self, a_list, response):
        self.a_list = a_list
        self.response = response

    def _assert(self):
        for i in self.a_list:
            i(self.response)
