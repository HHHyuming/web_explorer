from flask import Blueprint, request

from common.MyResponse import MyResponse
from config import db_connection_list

explorer_db = db_connection_list['explorer']
blue_explorer = Blueprint('explorer', __name__, url_prefix='/explorer')


@blue_explorer.before_request
def check_user_legal():
    """
    jwt 验证
    :return:
    """
    
    return '中间件'


@blue_explorer.route('/index')
def index():
    """
    主页，数据渲染
    :return:
    """
    return MyResponse(data=[{'xxx':'xxx'}]).response_data


@blue_explorer.route('/create_file')
def create_file():
    req_params = request.get_json()
    file_path = req_params.get('file_path')
    file_name = req_params.get('file_name')
    desc = req_params.get('desc')
