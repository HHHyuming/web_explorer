import traceback

from flask import Blueprint, request

from config import db_connection_list
from common.MyResponse import MyResponse
from common.Loghandler import MyLoggin
from utils.common_fun import generate_by_caesar_code, caesar_decode
from api import logic

blue_user_action = Blueprint('user_action', __name__, url_prefix='/user')
explorer_db = db_connection_list['explorer']
user_log = MyLoggin('user')


@blue_user_action.route('/register')
def user_register_fun():
    """
    用户注册 api 实现1
    :return:
    """
    register_user_name = request.form.get('user_name')
    register_user_password = request.form.get('user_password')

    def user_is_exists():
        sql = 'select user_name from user_t where user_name=%s'
        with explorer_db as db:
            db.cursor.execute(sql, (register_user_name,))
            result = db.cursor.fetchall()
        return True if result else False

    def user_register_init(user_name, user_password, permission):
        sql = 'insert into user_t(`user_name`, `user_password`,`permission`, `create_time`, `update_time`) ' \
              'values (%s,%s,%s)'
        user_id_sql = 'select id from user_t where user_name = %s '
        space_sql = 'insert into space_t(`file_name`, `file_type`, `file_size`, `author_name`, `desc_content`, ' \
                    '`user_id`, `create_time`, `update_time`, `level`, `path`)'

        logic.init_user_data(register_user_name)
        dir_list, data_list = logic.gain_root_level_info(user_name)
        insert_list = []
        with explorer_db as db:
            try:
                db.cursor.execute(sql, (user_name, user_password, permission))
                db.cursor.execute(user_id_sql, (user_name,))
                user_id = db.cursor.fetchall()
                for item in (dir_list + data_list):
                    file_name = item['name']
                    file_type = item['file_type']
                    file_size = item['size']
                    author_name = item['author']
                    desc_content = item['desc']
                    create_time = item['create_time']
                    update_time = item['update_time']
                    level = item['level']
                    path = item['path']
                    insert_list.append([file_name, file_type, file_size, author_name, desc_content, user_id,
                                        create_time, update_time, level, path])
                db.cursor.executemany(space_sql, insert_list)
            except Exception as e:
                # 错误回滚
                # traceback.print_exc()
                user_log.error('用户注册失败 traceback---: %s' % str(traceback.format_exc()))
                db.conn.rollback()
                return False
            return True

    def judge_numbers_of_user():
        sql = 'select count(user_id) from space_t group by user_id'
        with explorer_db as db:
            db.cursor.execute(sql)
            res = db.cursor.fetchall()
            if res[0] > 5:
                return True

    if user_is_exists():
        msg = '该用户已存在,请重试'
        return MyResponse(msg=msg, code=600).response_data
    elif len(register_user_password) < 6:
        msg = '密码长度必须大于6'
        return MyResponse(msg=msg, code=600).response_data

    password = generate_by_caesar_code(password=register_user_password)

    if judge_numbers_of_user():
        return MyResponse(msg='注册用户数已达上限').response_data
    # 用户生成默认space
    register_flag = user_register_init(user_name=register_user_name, user_password=password,
                                       permission='select')
    if not register_flag:
        msg = '用户数据初始化失败'
        return MyResponse(msg=msg, code=600).response_data

    msg = '注册成功'
    return MyResponse(msg=msg).response_data


@blue_user_action.route('login')
def user_login():
    """
    用户登录 api 实现
    :return:
    """
    user_name = request.form.get('user_name')
    user_password = request.form.get('user_password')
