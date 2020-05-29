import os
from datetime import datetime, timedelta
from zipfile import ZipFile

from werkzeug.utils import secure_filename
from flask import Blueprint, request, g, send_from_directory



from common.Loghandler import MyLoggin
from common.MyResponse import MyResponse
from utils.common_fun import decode_jwt
from api.logic import get_cascade_path
from api import logic
from config import db_connection_list, USER_HOME_DIR, SECRET_KEY


explorer_db = db_connection_list['explorer']
blue_explorer = Blueprint('explorer', __name__, url_prefix='/explorer')
explorer_log = MyLoggin('explorer.log', file=True)


@blue_explorer.before_request
def check_user_legal():
    """
    jwt 验证
    :return:
    """
    token = request.headers.get('Authorization')
    try:
        payload = decode_jwt(token)
        print(payload)
        g.user = payload['user_name']

    except Exception as e:
        explorer_log.logger.error('认证失败 ---- ip:%s ; referer%s'% (str(request.remote_addr),str(request.headers.get('referer'))))
        return MyResponse(code=800, msg='认证失败').response_data



@blue_explorer.route('/index')
def index():
    """
    主页，数据渲染
    :return:
    """
    def user_id():
        sql = 'select id from user_t where user_name=%s'
        with explorer_db as db:
            db.cursor.execute(sql, (g.user,))
            data = db.cursor.fetchall()
            return data[0]['id']

    def get_index_data():
        sql = 'select `file_name`, `update_time`, `file_type`, `file_size`, \
              `create_time`,`author_name`,`desc_content`,`user_id`,`path`,`level` from space_t ' \
              'where user_id=%s'
        condition_id = user_id()
        # print(condition_id)
        with explorer_db as db:

            db.cursor.execute(sql, (condition_id,))
            all_data = db.cursor.fetchall()
            return all_data
    result = get_index_data()
    # print(result)
    if result:
        return MyResponse(data=result).response_data
    else:
        return MyResponse(msg='暂无数据', code=500).response_data


@blue_explorer.route('/create_folder', methods=['POST'])
def create_folder():
    req_params = request.get_json()

    file_list = req_params.get('file_path', '')
    file_name = req_params.get('file_name')
    desc = req_params.get('desc')

    base_path = os.path.join(USER_HOME_DIR, g.user)
    if file_list:
        db_path = f'{g.user}'
    else:
        db_path = f'{g.user}\\{file_name}'
    for path in file_list:
        base_path = os.path.join(base_path, path)
        db_path += f'\\{path}'
    # 创建目录或文件
    create_flag = logic.create_dir(base_path, file_name)

    if not create_flag:
        return MyResponse(msg='创建失败,文件已存在', code=600).response_data

    # 信息入DB
    def insert_create_folder(data):
        sql = 'insert into space_t(`file_name`, `update_time`, `file_type`, `file_size`, \
              `create_time`,`author_name`,`desc_content`,`user_id`,`path`,`level`)  \
              values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        with explorer_db as db:
            try:
                db.cursor.execute(sql, data)
                db.conn.commit()
                return True
            except Exception as e:
                explorer_log.logger.error('error message ---- %s' %str(e))

    def select_user_id(user_name):
        """
        查询用户id
        :return:
        """
        sql = 'select id from user_t where user_name=%s'

        with explorer_db as db:
            db.cursor.execute(sql, (user_name,))
            user_data = db.cursor.fetchall()
            return user_data

    def before_insert_data():
        data = [file_name]
        update_time = datetime.now().strftime("%Y-%m-%d %X")
        file_type = 'dir'
        file_size = 0
        create_time = datetime.now().strftime("%Y-%m-%d %X")
        author_name = g.user
        desc_content = desc
        user_id = select_user_id(g.user)[0]['id']
        current_path = db_path
        level = len(db_path.split('\\'))
        data.append(update_time)
        data.append(file_type)
        data.append(file_size)
        data.append(create_time)
        data.append(author_name)
        data.append(desc_content)
        data.append(user_id)
        data.append(current_path)
        data.append(level)
        insert_create_folder(data)

    def update_hot_data():
        # 热点数据缓存

        pass
    try:
        before_insert_data()
        return MyResponse(msg='创建成功').response_data
    except Exception as e:
        explorer_log.logger.error(e)
        return MyResponse(msg='创建失败').response_data


@blue_explorer.route('/delete_file', methods=['POST'])
def delete_file():
    json_data = request.get_json()
    delete_list = json_data.get('delete_list')
    print(delete_list)
    def delete_for_db(path, file_name):
        sql = 'delete from space_t where path=%s and file_name=%s'
        with explorer_db as db:
            db.cursor.execute(sql, (path, file_name))
            db.conn.commit()

    for file_item in delete_list:
        file_path = file_item['path']
        delete_path = os.path.join(USER_HOME_DIR, file_path)
        delete_for_db(file_path, file_item['file_name'])
        file_type = file_item['file_type']
        flag = logic.delete_file(delete_path, file_type)
        if not flag:
            return MyResponse(msg='删除失败').response_data
    else:
        return MyResponse(msg='删除成功').response_data


@blue_explorer.route('/upload_file', methods=['POST'])
def upload_file():

    save_path = request.form.get('path')
    file_list = request.files.getlist('file')
    base_dir = os.path.join(USER_HOME_DIR, g.user)
    try:
        if save_path:
            save_path_list = save_path.split(',')
            for path in save_path_list:
                base_dir = os.path.join(base_dir, path)
        for single_file in file_list:
            file_name = secure_filename(single_file.filename)
            end_path = os.path.join(base_dir, file_name)
            single_file.save(end_path)
    except Exception as e:
        return MyResponse(msg='上传失败').response_data
    return MyResponse(msg='上传成功').response_data

@blue_explorer.route('/download_file', methods=['POST'])
def download_file():


    return MyResponse(msg='下载成功').response_data

@blue_explorer.route('/get_user_dir_cascade')
def get_dir_cascade():
    user_name = request.args.get('user_name')
    file_path = os.path.join(USER_HOME_DIR, user_name)
    res = get_cascade_path(file_path).data
    if 'children' in res:
        cascade_dir_list = res.pop('children')
    else:
        cascade_dir_list = []
    return MyResponse(data=cascade_dir_list).response_data


@blue_explorer.route('/message')
def show_serve_info():
    print(id(explorer_db))
    explorer_log.logger.info('test for explorer router')

    return str(id(explorer_db))
