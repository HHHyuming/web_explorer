import os
from common import db_handler

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 用户初始化家目录
USER_HOME_DIR = r'D:\code\web_explorer\backend\data'
# 所有db认证相关配置
NormalDBConfig = {
    'explorer': {
        'db_name': 'explorer',
        'db_host': '127.0.0.1',
        'db_port': 3306,
        'db_user': 'root',
        'db_password': 'root',
        'charset': 'utf8',
    }
}
# 当前db池
db_connection_list = {
    'explorer': db_handler.MysqlPool(NormalDBConfig['explorer'])
}


# 日志配置
class LogConfig:
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0

    LOG_PATH = os.path.join(BASE_DIR, 'log')


class BaseConfig:
    DEBUG = False


class DevConfig(BaseConfig):
    DEBUG = True
    PORT = 8090


class ProductConfig(BaseConfig):
    DEBUG = False


config_map = {
    'default': DevConfig,
    'production': ProductConfig,
    'development': DevConfig,
}
