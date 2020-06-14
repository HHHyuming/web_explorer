import os
import traceback
import time
import datetime


from flask import Blueprint, request


from api.logic import get_cascade_path
from common.LoadStaticResource import StaticResource
from config import db_connection_list, DEFAULT_EXP_TIME, SECRET_KEY, USER_HOME_DIR
from common.MyResponse import MyResponse
from common.Loghandler import MyLogger
from utils.common_fun import generate_by_caesar_code, caesar_decode, generate_jwt_code
from api import logic

blue_user_action = Blueprint('user_action', __name__, url_prefix='/user')
explorer_db = db_connection_list['explorer']
user_log = MyLogger.get_logger('user', 'user.log')


@blue_user_action.route('/register', methods=['POST'])
def user_register_fun():
    """
    用户注册 api 实现1
    :return:
    """
    request_data = request.get_json()
    register_user_name = request_data.get('user_name')
    register_user_password = request_data.get('user_password')
    register_sec_password = request_data.get('sec_password')

    def user_is_exists():
        sql = 'select user_name from user_t where user_name=%s'
        with explorer_db as db:
            db.cursor.execute(sql, (register_user_name,))
            result = db.cursor.fetchall()
        return True if result else False

    def user_register_init(user_name, user_password, permission):
        sql = 'insert into user_t(`user_name`, `user_password`,`permission`, `create_time`, `update_time`) ' \
              'values (%s,%s,%s,%s,%s)'
        # user_id_sql = 'select id from user_t where user_name = %s '
        # space_sql = 'insert into space_t(`file_name`, `file_type`, `file_size`, `author_name`, `desc_content`, ' \
        #             '`user_id`, `create_time`, `update_time`, `level`, `path`)'
        create_time = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %X")
        update_time = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %X")
        logic.init_user_data(register_user_name)
        with explorer_db as db:
            try:
                db.cursor.execute(sql, (user_name, user_password, permission,create_time, update_time))
                db.conn.commit()
            except Exception as e:
                # 错误回滚
                traceback.print_exc()
                user_log.logger.error('用户注册失败 traceback---: %s' % str(traceback.format_exc()))
                db.conn.rollback()
                return False
        return True

    def judge_numbers_of_user():
        sql = 'select count(id) as all_user from user_t group by id'
        with explorer_db as db:
            db.cursor.execute(sql)
            res = db.cursor.fetchall()
            print(res)
            if len(res) > 5:
                return True

    if register_sec_password != register_user_password:
        return MyResponse(msg='密码不一致，请重新输入', code=600).response_data

    if user_is_exists():
        msg = '该用户已存在,请重试'
        return MyResponse(msg=msg, code=700).response_data
    elif len(register_user_password) < 4:
        msg = '密码长度必须大于6'
        return MyResponse(msg=msg, code=600).response_data

    password = generate_by_caesar_code(password=register_user_password)

    if judge_numbers_of_user():
        return MyResponse(msg='注册用户数已达上限', code=700).response_data
    # 用户生成默认space
    register_flag = user_register_init(user_name=register_user_name, user_password=password,
                                       permission='select;insert;update;delete')
    if not register_flag:
        msg = '用户数据初始化失败'
        return MyResponse(msg=msg, code=700).response_data
    # 设置静态资源路径
    StaticResource([register_user_name]).load()
    msg = '注册成功'
    token = generate_jwt_code(register_user_name)
    data = {'token': token}
    return MyResponse(msg=msg, data=data).response_data


@blue_user_action.route('login', methods=['POST'])
def user_login():
    """
    用户登录 api 实现
    前端axios 发送请求 POST --- content-type application/json ---- request.json
                      GET ---- content-type query_string ----- request.args
    jwt 验证
    三部分 ：头部，载荷(包含exp过期时间字段), 密钥
    :return:
    """
    user_data = request.get_json()
    user_name = user_data.get('user_name')
    user_password = user_data.get('user_password')

    def user_is_exists():
        sql = 'select user_name, user_password from user_t where user_name=%s'
        with explorer_db as db:
            db.cursor.execute(sql, (user_name,))
            result = db.cursor.fetchall()
        return result if result else False
    valid_data = user_is_exists()
    a = valid_data[0]['user_password']

    if valid_data and caesar_decode(valid_data[0]['user_password']) == user_password and user_name == user_name:
        # 生成jwt
        # exp_time = datetime.datetime.utcnow() + datetime.timedelta(hours=DEFAULT_EXP_TIME)
        # pay_load = {'exp': exp_time, 'user_name': user_name}
        # token = jwt.encode(pay_load, SECRET_KEY).decode('utf8')
        token = generate_jwt_code(user_name)

        return MyResponse(data={'token': token}).response_data
    return MyResponse(msg='用户名或密码错误，请重试').response_data


@blue_user_action.route('/message')
def show_serve_info():
    print(id(explorer_db))
    user_log.logger.info('test.py for user router')
    return str(id(explorer_db))


@blue_user_action.route('/get_file')
def get_file():
    from flask import send_from_directory,Response
    path = r'C:\Users\Administrator\Pictures\Camera Roll'

    return send_from_directory(path, 'bear.jpg', as_attachment=True)
    # return 'sadsd'