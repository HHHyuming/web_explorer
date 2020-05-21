import logging
import os
from logging.handlers import TimedRotatingFileHandler
import time
from config import LogConfig, BASE_DIR


class MyLoggin(object):

    def __init__(self, name, level=LogConfig.DEBUG, file=None, stream=None):
        self.name = name
        self.level = level
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)
        if stream:
            self.__setStreamHandler__()
        if file:
            self.__setFileHandler__()

    def __setFileHandler__(self):
        log_path = os.path.join(LogConfig.LOG_PATH, self.name)
        fh = TimedRotatingFileHandler(filename=log_path, when='D', interval=1, backupCount=15)
        fh.suffix = '%Y-%m-%d.log'
        # fh.setLevel(self.level)
        formatter = logging.Formatter('%(asctime)s ----- %(filename)s ----- [line:%(lineno)d] ----- %(levelname)s -----'
                                      ' %(message)s', '%Y-%m-%d %H:%M:%S')

        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def __setStreamHandler__(self):
        pass


if __name__ == '__main__':
    # log_api = MyLoggin(name='test')
    # # print(log_api.handlers)
    # # log_api.error('xxx')
    # # log_api.info('asdsadd')
    # for i in range(10):
    #     log_api.logger.error('xxxxxxxxxxx')
    #     time.sleep(0.5)
    pass