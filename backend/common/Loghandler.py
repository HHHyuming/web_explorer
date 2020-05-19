import logging
import os
from logging.handlers import TimedRotatingFileHandler

from config import LogConfig, BASE_DIR


class MyLoggin(logging.Logger):

    def __init__(self, name, level=LogConfig.DEBUG, file=None, stream=None):
        self.name = name
        self.level = level
        if stream:
            self.__setStreamHandler__()
        if file:
            self.__setFileHandler__()

    def __setFileHandler__(self, level=None):

        file_name = LogConfig.LOG_PATH + self.name + '.log'
        file_handler = TimedRotatingFileHandler(filename=file_name, when='D', interval=1, backupCount=15)
        file_handler.suffix = '%Y_%m_%d.log'
        if not level:
            file_handler.setLevel(self.level)
        else:
            file_handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s ----- %(filename)s ----- [line:%(lineno)d] ----- %(levelname)s -----'
                                      ' %(message)s', '%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        self.file_handler = file_handler
        self.addHandler(file_handler)

    def __setStreamHandler__(self, level=None):
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        stream_handler.setFormatter(formatter)
        if not level:
            stream_handler.setLevel(self.level)
        else:
            stream_handler.setLevel(level)
        self.addHandler(stream_handler)

    def reset_name(self, name):
        self.name = name
        # removeHandler 从列表中移除
        self.removeHandler(self.file_handler)
        self.__setFileHandler__()
