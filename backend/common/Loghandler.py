#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import logging.handlers
import os
import re
import time
import codecs

import config


class MultiProcessSafeDailyRotatingFileHandler(logging.handlers.BaseRotatingHandler):
    """
    - Multi process safe
    - Rotate at midnight only, when _compute_fn() result changed 
    - Utc not supported
    """

    def __init__(self, logfile, encoding=None, delay=False, utc=False, backupCount=7, **kwargs):
        self.utc = utc
        self.suffix = "%Y-%m-%d"
        self.backupCount = backupCount
        self.baseFilename = logfile
        self.extMatch = r"^\d{4}-\d{2}-\d{2}$"
        self.extMatch = re.compile(self.extMatch)
        self.currentFileName = self._compute_fn()
        logging.handlers.BaseRotatingHandler.__init__(
            self, self.baseFilename, 'a', encoding, delay)

    def shouldRollover(self, record):
        if self.currentFileName != self._compute_fn():
            return True
        return False

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        self.currentFileName = self._compute_fn()
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)

    def _compute_fn(self):
        """返回带时间结尾的filename，是否需要滚动的依据"""
        return self.baseFilename + "." + time.strftime(self.suffix, time.localtime())

    def getFilesToDelete(self):
        """
        Determine the files to delete when rolling over.

        More specific than the earlier method, which just used glob.glob().
        """
        dirName, baseName = os.path.split(self.baseFilename)
        fileNames = os.listdir(dirName)
        result = []
        prefix = baseName + "."
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                suffix = fileName[plen:]
                if self.extMatch.match(suffix):
                    result.append(os.path.join(dirName, fileName))
        result.sort()
        if len(result) < self.backupCount:
            result = []
        else:
            result = result[:len(result) - self.backupCount]
        return result

    def _open(self):
        """覆盖FileHandler的_open, 最终在FileHandler中的emit调用"""
        if self.encoding is None:
            stream = open(self.currentFileName, self.mode)
        else:
            stream = codecs.open(self.currentFileName,
                                 self.mode, self.encoding)
        # 删除已有的软链
        if os.path.exists(self.baseFilename):
            try:
                os.remove(self.baseFilename)
            except OSError:
                pass
        try:
            os.symlink(self.currentFileName, self.baseFilename)
        except OSError:
            pass
        return stream


class MyLogger:

    def __init__(self):
        pass

    @staticmethod
    def get_logger(log_name="ping", log_file=None, log_level=logging.DEBUG):
        log_file = os.path.join(config.LOG_PATH, log_file)
        logger = logging.getLogger(log_name)
        if logger.handlers == []:
            # 按天输出一周日志文件
            fileHandler = MultiProcessSafeDailyRotatingFileHandler(log_file, backupCount=7)
            formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(process)d'
                                          ' - %(thread)d - %(message)s', '%Y-%m-%d %H:%M:%S')
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)
        logger.setLevel(log_level)
        return logger


if __name__ == '__main__':
    logger = MyLogger.get_logger()
    logger.info('test.py')
