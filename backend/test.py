# def Singleton(cls):
#     _instance = {}
#
#     def _singleton(*args, **kargs):
#         if cls not in _instance:
#             _instance[cls] = cls(*args, **kargs)
#         return _instance[cls]
#
#     return _singleton
#
#
# @Singleton
# class A(object):
#     a = 1
#
#     def __init__(self, x=0):
#         self.x = x
#
#
# a1 = A(2)
# a2 = A(3)
#
# print(a1)
# print(a2)
#
# print(a1.x)
# print(a2.x)

import logging
import os
import platform
import time
import re
import zipfile
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler

def main():
    #日志打印格式
    log_fmt = r'%(asctime)s\tFile \"%(filename)s\",line %(lineno)s\t%(levelname)s: %(message)s'
    formatter = logging.Formatter(log_fmt)
    #创建TimedRotatingFileHandler对象
    log_file_handler = TimedRotatingFileHandler(filename="ds_update", when="S", interval=1, backupCount=15)
    #log_file_handler.suffix = "%Y-%m-%d_%H-%M.log"
    #log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$")
    log_file_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger()
    log.addHandler(log_file_handler)
    #循环打印日志
    log_content = "test.py log"
    count = 0
    while count < 30:
        log.error(log_content)
        time.sleep(0.5)
        count = count + 1
    log.removeHandler(log_file_handler)


if __name__ == "__main__":
    # main()
    import datetime
    #
    # res = datetime.datetime.fromtimestamp(1590026941.05686)
    # re2 = res.strftime("%Y-%m-%d %X")
    # print(re2)

    # import jwt
    # exp_field = datetime.datetime.now() + datetime.timedelta(seconds=1)
    # print('before valid', exp_field, time.mktime(exp_field.timetuple()))
    # pay_load = {'exp': exp_field}
    # token = jwt.encode(pay_load, '123').decode('utf8')
    # # print(token)
    # time.sleep(2)
    # res = jwt.decode(token,'123')
    # print(res)
    # class Li(list):
    #     pass
    # li = Li()
    # a= [1,2,3]
    # li.next =a
    # print(li.next)
    # li.next.clear()
    #
    # v = [1]
    # if v and isinstance(v, list):
    #     print('-------------')
    # print(li.pop())
    # def download_all():
    #     zipf = zipfile.ZipFile('Name.zip','w', zipfile.ZIP_DEFLATED)
    #     root_path = r'D:\code\web_explorer\backend\log'
    #     for root,dirs, files in os.walk(root_path):
    #         for file in files:
    #             os.chdir(root)  # 定位到文件夹
    #             zipf.write(file)
    #     zipf.close()
    #     return zipf
    #
    # download_all()
    # import time
    # import datetime
    # print(time.time())
    # print(datetime.datetime.now().strftime('%Y%m%d%H%M%S') )
    #
    # import uuid
    # print(uuid.uuid1(),type(str(uuid.uuid1())))
    # print(os.path.dirname('admin\\abc'))
    # print(os.path.basename('admin\\abc'))
    # li = [1,2,3,4,5]
    # for i in enumerate(li):
    #     print(i)
    #
    # print('\\'.join(['admin']))
    import os

    # os.remove(r'D:\code\web_explorer\backend\static\admin3\data.txt')
    while True:
        for i in range(10):
            print(i)
            if i ==3:
                break
