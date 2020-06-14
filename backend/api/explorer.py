import copy
import os, platform
import time
import uuid
from datetime import datetime, timedelta
from io import BytesIO
import zipfile

from werkzeug.utils import secure_filename
from flask import Blueprint, request, g, send_from_directory, send_file, make_response, Response

import config
from common.Loghandler import MyLogger
from common.MyResponse import MyResponse
from utils.common_fun import decode_jwt
from api.logic import get_cascade_path
from api import logic
from config import db_connection_list, USER_HOME_DIR, SECRET_KEY


explorer_db = db_connection_list['explorer']
blue_explorer = Blueprint('explorer', __name__, url_prefix='/explorer')
explorer_log = MyLogger.get_logger('explorer', 'explorer.log')

# 鉴权
@blue_explorer.before_request
def check_user_legal():
    """
    jwt 验证
    :return:
    """
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
    path = request.path
    token = request.headers.get('Authorization')
    if request.method == 'OPTIONS':
        return
    # try:
    payload = decode_jwt(token)
    g.user = payload['user_name']
    g.user_id = select_user_id(g.user)[0]['id']
# except Exception as e:
#     explorer_log.error(e)
#     print(request.method, token)
    # explorer_log.logger.error('认证失败 ---- ip:%s ; referer%s'% (str(request.remote_addr),str(request.headers.get('referer'))))
    # return MyResponse(code=800, msg='认证失败').response_data


# 首页数据
@blue_explorer.route('/index')
def index():
    """
    主页，数据渲染
    :return:
    """
    user_name = request.args.get('user_name')
    path_level = 1
    path = user_name

    def get_index_data():
        sql = 'select `file_name`, `update_time`, `file_type`, `file_size`, \
              `create_time`,`author_name`,`desc_content`,`user_id`,`path`,`level`, `hash_name` from space_t ' \
              'where user_id = {0} and (path = "{1}" or level = "{2}") '.format(g.user_id, path, path_level)

        # print(condition_id)
        with explorer_db as db:
            # print(sql)
            db.cursor.execute(sql)
            all_data = db.cursor.fetchall()
            return all_data
    result = get_index_data()
    # print(result)
    if result:
        return MyResponse(data=result).response_data
    else:
        return MyResponse(msg='暂无数据', code=500).response_data


# 创建文件夹
@blue_explorer.route('/create_folder', methods=['POST'])
def create_folder():
    req_params = request.get_json()

    file_list = req_params.get('file_path', '')
    file_name = req_params.get('file_name')
    desc = req_params.get('desc')

    base_path = os.path.join(USER_HOME_DIR, g.user)
    if file_list:
        db_path = f'{g.user}'
        file_list.append(file_name)
    else:
        db_path = f'{g.user}\\{file_name}'
    for path in file_list:
        base_path = os.path.join(base_path, path)
        db_path += f'\\{path}'
    # 创建目录或文件


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

    def before_insert_data():
        data = [file_name]
        update_time = datetime.now().strftime("%Y-%m-%d %X")
        file_type = 'dir'
        file_size = 0
        create_time = datetime.now().strftime("%Y-%m-%d %X")
        author_name = g.user
        desc_content = desc
        user_id = g.user_id
        current_path = db_path
        level = len(db_path.split('\\')) - 1
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


# 删除文件夹
@blue_explorer.route('/delete_file', methods=['POST'])
def delete_file():
    json_data = request.get_json()
    delete_list = json_data.get('delete_list')

    def delete_for_db(path, hash_name, file_type, level):
        path = path.replace('\\','\\\\') if platform.system() == 'Windows' else path
        if file_type == 'dir':
            sql = 'delete from space_t where locate("{0}",path) and `level` > {1}'\
                .format(path,level)
        else:
            sql = 'delete from space_t where hash_name="{0}"'.format(hash_name)
        with explorer_db as db:
            db.cursor.execute(sql)
            db.conn.commit()

    for file_item in delete_list:
        file_path = file_item['path']
        delete_for_db(file_path, file_item['hash_name'],file_item['file_type'],file_item['level'])
        file_type = file_item['file_type']
        if file_item['file_type'] != 'dir':
            delete_path = os.path.join(config.STATIC_FOLDER, g.user, file_item['hash_name'])
            flag = logic.delete_file(delete_path, file_type)

    else:
        return MyResponse(msg='删除成功').response_data


# 上传文件
@blue_explorer.route('/upload_file', methods=['POST'])
def upload_file():

    save_path = request.form.get('path')
    size_list = request.form.getlist('size')
    file_list = request.files.getlist('file')
    base_dir = os.path.join(USER_HOME_DIR, g.user)

    file_tuple = list(zip(file_list, size_list))

    # record
    def insert_info_to_db(data):

        sql = 'insert into space_t(`file_name`, `update_time`, `file_type`, `file_size`, \
              `create_time`,`author_name`,`desc_content`,`user_id`,`path`,`level`,`hash_name`)  \
              values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        with explorer_db as db:
            try:
                db.cursor.execute(sql, data)
                db.conn.commit()
                return True
            except Exception as e:
                db.conn.rollback()
                explorer_log.logger.error('error message ---- %s' % str(e))
    # try:
    if save_path:
        save_path_list = save_path.split(',')
        for path in save_path_list:
            base_dir = os.path.join(base_dir, path)

        db_path = g.user + config.SPLICER + save_path.replace(',', config.SPLICER) if platform.system() == 'Windows' else \
            g.user + '/' + save_path.replace(',', '/')
    else:
        db_path = g.user
    for single_file, file_size in file_tuple:
        file_name = secure_filename(single_file.filename)
        # db
        now_time = datetime.now().strftime('%Y-%m-%d %X')
        file_type = file_name.rsplit('.')[-1]
        if file_type == file_name:
            file_name = single_file.filename.rsplit('.')[0]
        level = len(db_path.split('\\'))
        # 文件名
        real_name = datetime.now().strftime('%Y%m%d%H%M') + str(uuid.uuid4()) + '.' + file_type
        # print(file_name, real_name)
        single_file.filename = real_name
        params = [file_name, now_time, file_type, file_size, now_time, g.user, '',
                g.user_id, db_path, level, real_name]
        # 入 db
        insert_info_to_db(params)
        # 保存文件
        static_path = os.path.join(config.STATIC_FOLDER, g.user, real_name)
        single_file.save(static_path)
    # except Exception as e:
    #     return MyResponse(msg='上传失败').response_data
    return MyResponse(msg='上传成功').response_data


# 下载文件
@blue_explorer.route('/download_file', methods=['GET','POST'])
def download_file():
    """
    >=150M 大文件，直接给静态资源地址
    小文件
    :return:
    # TODO 功能完善
    """
    def file_wrapper(oo):

        while True:
            data = oo.read(1024)
            if not data:
                break
            yield data

    def select_file_name(current_arg,zip_file=None):
        sql = 'select `hash_name`,`file_name`,`path` from space_t ' \
              'where user_id = {0} and (locate("{1}",path)) and file_name in ("{2}") '\
            .format(g.user_id,current_arg['path'],current_arg['file_name'])

        if zip_file:
            path_arg = current_arg['path'].replace('\\','\\\\') if platform.system() == 'Windows' else current_arg['path']
            sql = 'select `hash_name`, `file_name`,`path` from space_t ' \
                  'where user_id = {0} and (locate("{1}",path) and `level` > {2}) and file_type != "dir" ' \
                .format(g.user_id, path_arg, current_arg['level'])
        print(sql)
        with explorer_db as db:
            db.cursor.execute(sql)
            result = db.cursor.fetchall()
            print(result)
        return result

    json_data = request.get_json()
    if len(json_data) > 1 or json_data[0]['file_type'] == 'dir':
        zip_name = datetime.now().strftime('%Y-%m-%d') + '.zip'
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for full_path in json_data:
                current_path = os.path.join(config.STATIC_FOLDER, g.user)
                # 查找该目录下的所有文件
                if full_path['file_type'] == 'dir':
                        file_list = select_file_name(full_path,zip_file=True)
                        for file in file_list:
                            arg1 = os.path.join(current_path, file['hash_name'])
                            arg2 = os.path.join(file['path'], file['file_name'])
                            zf.write(arg1,arg2)
                            # with open(os.path.join(current_path,file['hash_name']),'r',encoding='utf8') as f:
                            #     zf.writestr(file['file_name'], f.read())
                # 查找当前文件
                else:
                    file = select_file_name(full_path)[0]
                    arg1 = os.path.join(current_path, file['hash_name'])
                    arg2 = os.path.join(file['path'], file['file_name'])
                    zf.write(arg1, arg2)
                    # with open(os.path.join(current_path, file['hash_name']), 'r', encoding='utf8') as f:
                    #     zf.writestr(file['file_name'], f.read())


            # def generate():
            #     for row in range(5000):
            #         line = []
            #         for col in range(500):
            #             line.append(str(col))
            #
            #         if row % 1000 == 0:
            #             print('row-----', row)
            #         yield ','.join(line) + '\n'

            # make_response(bytes or str or io.pathlink,) Response(maybe generate,)
        memory_file.seek(0)
        response = Response(file_wrapper(memory_file))
        response.headers['Content-type'] = 'application/octet-stream'
        response.headers["Content-disposition"] = 'attachment; filename=%s' % zip_name
        return response

    else:
        print(json_data)
        result = select_file_name(json_data[0])[0]
        real_file_name,file_name  = result['hash_name'], result['file_name']
        path = os.path.join(config.STATIC_FOLDER, g.user,real_file_name)
        response = make_response(send_file(path, attachment_filename=file_name))
        return response
        pass

    # f = open(r'D:\code\web_explorer\backend\data\admin\tt\123\explorer.log')
    # response = make_response(f.read())
    # response.headers['content-type'] = 'application/octet-stream'
    # response.headers["Content-disposition"] = 'attachment; filename=%s' % 'test.py.zip'
    # return response

    # return MyResponse(msg='下载成功').response_data


# 获取级联数据
@blue_explorer.route('/get_user_dir_cascade')
def get_dir_cascade():
    user_name = request.args.get('user_name')
    file_path = os.path.join(USER_HOME_DIR, user_name)
    res = get_cascade_path(file_path).data
    # print('级联数据',res)
    if 'children' in res:
        cascade_dir_list = res.pop('children')
    else:
        cascade_dir_list = []
    return MyResponse(data=cascade_dir_list).response_data


@blue_explorer.route('/new_cascade')
def new_cascade_path():
    data = []

    "condition path=path or level=len(path)-1"
    "name path "
    def sql_data():
        sql = 'select file_name,path,`level` from space_t where user_id=%s and file_type=%s'

        with explorer_db as db:
            db.cursor.execute(sql, (g.user_id, 'dir'))
            all_data = db.cursor.fetchall()

            return all_data

    result = sql_data()
    if not result:
        return MyResponse().response_data
    max_level = max(result, key=lambda x: x['level'])['level']

    while result:
        for i, _ in enumerate(result):
            if result[i]['level'] == max_level:
                current_node = {'label':result[i]['file_name'], 'value': result[i]['file_name'],
                                'path': result[i]['path']}
                for sub, _ in enumerate(data):
                    sub_node = data[sub]
                    if os.path.dirname(sub_node['path']) == current_node['path']:
                        if 'children' not in current_node:
                            current_node['children'] = []
                        sub_node.pop('path') if 'path' in sub_node else 0
                        current_node['children'].append(sub_node)

                else:
                    data.append(current_node)
                    result.pop(i)

                def delete_item():
                    flag = True
                    while flag:
                        res = None
                        for delete_index, _ in enumerate(data):
                            if 'path' not in data[delete_index]:
                                res = data.pop(delete_index)
                        if res is None:
                            break

                delete_item()

        if result:
            max_level = max(result, key=lambda x: x['level'])['level']
    else:
        for i in data:
            i.pop('path')
    # print(data)
    return MyResponse(data=data).response_data


@blue_explorer.route('/level_path')
def get_level_path(path):

    "condition path=path or level=len(path)-1"
    "name path "
    condition_path = '\\'.join(path)
    path_level = len(path) - 1
    def query_data():

        pass


@blue_explorer.route('/change_directory', methods=['POST','GET'])
def change_directory():
    # 更换目录
    origin_change_path = request.get_json().get('change_path')
    # print(origin_change_path)
    if isinstance(origin_change_path,list):
        # print(*origin_change_path)
        origin_change_path = os.path.join(g.user,*origin_change_path)

    def get_dir_data(arg_path):
        level = arg_path.count('/')
        if platform.system() == 'Windows':
            arg_path = arg_path.replace('\\', '\\\\')
            level = arg_path.count('\\\\')

        sql = 'select `file_name`, `update_time`, `file_type`, `file_size`, \
              `create_time`,`author_name`,`desc_content`,`user_id`,`path`,`level`, `hash_name` from space_t ' \
              'where user_id = {0} and (locate("{1}",path) and `level` > {2})  '.format(g.user_id,arg_path,level)
        if level == 0:
            sql = 'select `file_name`, `update_time`, `file_type`, `file_size`, \
                          `create_time`,`author_name`,`desc_content`,`user_id`,`path`,`level`, `hash_name` from space_t ' \
                  'where user_id = {0} and (locate("{1}",path) and `level` < 2)  '.format(g.user_id, arg_path,
                                                                                            arg_path)
        with explorer_db as db:
            # print(sql)
            db.cursor.execute(sql)
            res_data = db.cursor.fetchall()
        return res_data
    if not origin_change_path:
        condition_path = g.user
    else:
        condition_path = os.path.join(origin_change_path)
    # print(condition_path)
    result = get_dir_data(condition_path)
    # print(result)
    return MyResponse(data=result).response_data


@blue_explorer.route('/search')
def search_content():
    search_name = request.args.get('search_name')

    def select_data(name):
        sql = 'select `file_name`, `update_time`, `file_type`, `file_size`, \
              `create_time`,`author_name`,`desc_content`,`user_id`,`path`,`level`, `hash_name` from space_t ' \
              'where locate("{0}",file_name)'.format(name)
        with explorer_db as db:
            db.cursor.execute(sql)
            data = db.cursor.fetchall()
            return data

    res = select_data(search_name)
    return MyResponse(data=res).response_data


@blue_explorer.route('/message')
def show_serve_info():
    """
    test API
    :return:
    """
    print(id(explorer_db))
    explorer_log.logger.info('test.py for explorer router')

    return str(id(explorer_db))
