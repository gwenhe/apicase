# from typing import Union, List, Any
# import jmespath
# from apicase.common.exception import JsonAssertError
# from apicase.common.enumeration import ComparatorEnum
# from apicase.common.schema import JSONAssertSchema
# from deepdiff import DeepDiff
# from typing import Optional, Union
# import json
#
#
# class Asserter(object):
#     """
#     断言基类
#     """
#
#     def _assert(self):
#         pass
#
#
# class JSONAsserter(Asserter):
#     """
#     Json 断言器
#     """
#     assert_list = List[JSONAssertSchema]
#     assert_results_list = List
#
#     def __init__(self, a_list: list, response_json: Union[dict, list], equal_type: bool = True, ):
#         self.a_list = a_list
#         self.equal_type = equal_type
#         self.init_data()
#         self.json_assert(response_json)
#
#     def init_data(self):
#         assert_list = []
#         for i in self.a_list:
#             assert_list.append(
#                 JSONAssertSchema(expression=i[0], comparator=i[1], value=i[2])
#             )
#         self.assert_list = assert_list
#
#     def json_assert(self, response_json: Union[dict, list]):
#         """
#         json 断言
#         :param response_json:
#         """
#         assert_results_list = []
#         for i in self.assert_list:
#             value = i.value
#             comparator = i.comparator
#             assert_value = jmespath.search(i.expression, response_json)
#             if comparator is ComparatorEnum.EQUAL:
#                 assert_results_list.append([assert_value, assert_value == value, i])
#             if comparator is ComparatorEnum.GREATER:
#                 assert_results_list.append([assert_value, assert_value > value, i])
#             if comparator is ComparatorEnum.LESS:
#                 assert_results_list.append([assert_value, assert_value < value, i])
#         self.assert_results_list = assert_results_list
#         self._assert()
#
#     def _assert(self):
#         error_list = []
#         for i in self.assert_results_list:
#             if not i[1]:
#                 error_list.append(i)
#         error_str = ''
#         for i in error_list:
#             assert_example = i[2]
#             value = str(assert_example.value)
#             assert_value = str(i[0])
#             comparator = assert_example.comparator
#             expression = assert_example.expression
#             error_str += '\n\t JSON.{expression} {comparator} {value} \tBut: {assert_value} not {comparator} {value}' \
#                 .format(expression=expression,
#                         comparator=comparator.value,
#                         value=value,
#                         assert_value=assert_value,
#                         )
#         raise JsonAssertError('JSON 断言失败' + error_str)
#
#
# class ResponseAsserter(Asserter):
#     pass
#
#
# class CustomAsserter(Asserter):
#
#     def __init__(self, a_list, response):
#         self.a_list = a_list
#         self.response = response
#
#     def _assert(self):
#         for i in self.a_list:
#             i(self.response)
