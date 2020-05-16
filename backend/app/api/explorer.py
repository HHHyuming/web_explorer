import os
from flask import Blueprint

import config

explorer = Blueprint('explorer', __name__)


@explorer.route('/get_file_list')
def get_file_list():
    """
    获取当前用户家目录下的，--所有文件
    :return:
    """

    return 'get file list'
