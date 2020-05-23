import os

from flask import Blueprint, request
import jwt

from common.Loghandler import MyLoggin
from common.MyResponse import MyResponse
from api.logic import get_cascade_path
from api import logic
from config import db_connection_list, USER_HOME_DIR, SECRET_KEY


explorer_db = db_connection_list['explorer']
blue_explorer = Blueprint('explorer', __name__, url_prefix='/explorer')
user_log = MyLoggin('explorer.log', file=True)


@blue_explorer.before_request
def check_user_legal():
    """
    jwt 验证
    :return:
    """
    token = request.headers.get('Authorization')
    try:
        payload = jwt.decode(token, SECRET_KEY)
    except Exception as e:
        user_log.logger.error('认证失败 ---- ip:%s ; referer%s'% (str(request.remote_addr),str(request.headers.get('referer'))))
        return MyResponse(code=800, msg='认证失败').response_data



@blue_explorer.route('/index')
def index():
    """
    主页，数据渲染
    :return:
    """
    return MyResponse(data=[{'xxx':'xxx'}]).response_data


@blue_explorer.route('/create_file', method=['POST'])
def create_file():
    req_params = request.get_json()
    file_list = req_params.get('file_list')
    file_name = req_params.get('file_name')
    desc = req_params.get('desc')
    base_path = USER_HOME_DIR
    for path in file_list:
        base_path = os.path.join(base_path,path)

    create_flag = logic.create_dir(base_path, file_name)
    if not create_flag:
        return MyResponse(msg='创建失败', code=600).response_data

    def record_to_db():
        file_name =
        file_type =
        file_size =
        author_name =
        desc_content

        sql = 'insert into space_t()'
        with explorer_db as db:




@blue_explorer.route('/get_user_dir_cascade')
def get_dir_cascade():
    user_name = request.args.get('user_name')
    file_path = os.path.join(USER_HOME_DIR, user_name)
    cascade_dir_list = get_cascade_path(file_path).data.pop('children')

    return MyResponse(data=cascade_dir_list).response_data
