import os, platform
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
# JWT 配置
DEFAULT_EXP_TIME = 24
SECRET_KEY = 'abcdefg'

# 静态资源配置，对外开放
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')

# 日志配置

LOG_PATH = os.path.join(BASE_DIR, 'log')


SPLICER = '/' if platform.system() == 'Linux' else '\\'

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


if __name__ == '__main__':
    a = b'eyJleHAiOjE1OTAwNjIzNTR9'
    import base64
    print(base64.urlsafe_b64decode(a))