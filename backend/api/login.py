from flask import Blueprint, request

from config import db_connection_list
from common.MyResponse import MyResponse
from utils.common_fun import generate_by_caesar_code, caesar_decode
from api import logic

blue_user_action = Blueprint('user_action', __name__, url_prefix='/user')

explorer_db = db_connection_list['explorer']


@blue_user_action.route('/register')
def user_register_fun():
    """
    用户注册
    :return:
    """

    register_user_name = request.form.get('user_name')
    register_user_password = request.form.get('user_password')
    permission_id = request.form.get('admin')
    if not permission_id:
        permission_id = 2

    def user_is_exists():
        sql = 'select user_name from user_t where user_name=%s'
        with explorer_db as db:
            db.cursor.execute(sql, (register_user_name,))
            result = db.cursor.fetchall()
        return True if result else False

    def user_register_init(user_name, user_password, permission):
        sql = 'insert into user_t(`user_name`, `user_password`,`permission`) ' \
              'values (%s,%s,%s)'

        with explorer_db as db:
            try:
                db.cursor.execute(sql, (user_name, user_password, permission))
            except Exception as e:
                # 错误回滚
                db.conn.rollback()

    def flow_line():
        """
        流水线
        :return:
        """

    if user_is_exists():
        msg = '该用户已存在,请重试'
        return MyResponse(msg=msg).response_data
    elif len(register_user_password) < 6:
        msg = '密码长度必须大于6'
        return MyResponse(msg=msg).response_data

    password = generate_by_caesar_code(password=register_user_password)

    # 用户生成默认space
    init_flag = logic.init_user_data(register_user_name)
    if not init_flag:
        msg = '初始化失败'
        return MyResponse(msg=msg).response_data




    return 'register success'