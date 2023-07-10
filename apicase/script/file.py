# import os
# from config.ext import pytest_cache_dir
# import uuid
#
# """
# 废弃
# """
#
#
# class FakerFile(object):
#     """
#     文件
#     """
#
#     @staticmethod
#     def creat_file(suffix: str, unit: str, size: float, file_name: str = None) -> str:
#         """
#         生成指定位数uuid
#         :param suffix: 文件格式：例png、pdf、word
#         :param unit: 文件大小单位 'b'、'kb'、'mb'、'g'
#         :param size: 文件大小
#         :param file_name: 自定义文件名字，可随机
#         :return: 文件路径
#         """
#         file_directory = os.path.join(pytest_cache_dir, 'temp_file')
#         if file_name:
#             """
#             避免文件重复，为该文件生成一个uuid目录
#             """
#             uid = uuid.uuid4().hex[:8]
#             file_directory = os.path.join(file_directory, uid)
#         else:
#             uid = uuid.uuid4().hex[:8]
#             file_name = uid
#         if not os.path.exists(file_directory):
#             os.mkdir(file_directory)
#
#         file_name = file_name + '.' + suffix
#         file_path = os.path.join(file_directory, file_name)
#         numbers = {
#             'b': 1,
#             'kb': 1024,
#             'mb': 1024 * 1024,
#             'g': 1024 * 1024 * 1024,
#         }
#         multiples = numbers.get(unit, None)
#         assert multiples is not None
#
#         file = open(file_path, 'w')
#         file.seek(int(multiples * size))
#         file.write(' ')
#         file.close()
#         return file_path
#
# # if __name__ == '__main__':
# #     FakerFile().creat_file(suffix='xls', unit='mb', size=1.5)
#
# # FakerFile().creat_file('bmp', 'mb', 100)
