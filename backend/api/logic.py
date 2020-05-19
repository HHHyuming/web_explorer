import os

from flask import request
from config import USER_HOME_DIR


def init_user_data(user_name):
    user_current_dir = os.path.join(USER_HOME_DIR, user_name)
    if os.path.exists(user_current_dir):
        return False
    os.mkdir(user_current_dir)
    return

def gain_root_level_info(user_name):
    """
    数据格式形如 {'dir_name':'xxx',level_size:'xxx','root_dir':none}
                {'dir_name':'xxx2',level_size:'xxx','root_dir':xxx}
                {'dir_name':root,dir_list:{'dir_name':'root2',size:123,dir_list:{}},size:123}
    :param user_name:
    :return:
    """
    data_list = []
    dir_list = []
    user_current_dir = os.path.join(USER_HOME_DIR, user_name)
    # user_current_dir = r'D:\code\web_explorer\backend'
    file_list = os.listdir(user_current_dir)
    for file in file_list:
        current_test_path = os.path.join(user_current_dir, file)
        create_time = os.stat(current_test_path).st_ctime
        update_time = os.stat(current_test_path).st_mtime
        if os.path.isfile(current_test_path):
            file_name, file_type = current_test_path.rsplit('.')
            size = os.stat(current_test_path).st_size

            item = {'name': file, 'file_type': file_type, 'size': size, 'create_time': create_time,
                    'update_time': update_time, 'author': user_name, 'desc': ''}
            data_list.append(item)
        if os.path.isdir(current_test_path):
            item = {'name': file, 'file_type': None, 'size': None, 'create_time': create_time,
                    'update_time': update_time, 'author': user_name, 'desc': ''}
            size = gain_current_level_file_info(current_test_path, item)
            item['size'] = size
            dir_list.append(item)
    return dir_list, data_list


def gain_current_level_file_info(file_path, dir_item):
    size = 0
    file = dir_item['name']
    real_path = os.path.join(file_path, file)
    for root_dir, current_dir, file_list in os.walk(real_path):

        for real_file in file_list:
            size += os.stat(os.path.join(root_dir, real_file)).st_size
    return size


def create_file(file_path):
    pass

def create_dir(dir_path):
    pass



if __name__ == '__main__':
    # import time
    # print(time.strftime("%Y-%m-%d %X",time.localtime(os.stat(r'D:\code\web_explorer\backend').st_size)))
    # print(os.stat(r'D:\code\web_explorer\backend\api\explorer.py').st_size)
    # for root_dir, current_dir, file_list in os.walk(r'D:\code\web_explorer\backend'):
    #     if not ('.idea' in root_dir or '__pycache__' in root_dir):
    #         print(root_dir)
    #         print('-----------')
    #         print(list(filter(lambda x: x not in '.idea' and x not in '__pycache__', current_dir)))
    #         print('------------')
    #         print(file_list)
    # print(os.stat(r'D:\code\web_explorer\backend\api').st_ctime)
    # print(os.path.getctime(r'D:\code\web_explorer\backend\api'))
    # print(os.path.getctime(r'D:\code\web_explorer\backend\api\explorer.py'))
    # print(os.path.getctime(r'D:\code\web_explorer\backend\api\logic.py'))
    # print(os.path.getctime(r'D:\code\web_explorer\backend\api\login.py'))
    # print(os.path.isdir(r'D:\code\web_explorer\backend\api'))
    # print(os.path.isfile(r'D:\code\web_explorer\backend\api\explorer.py'))

    # is ok
    size_of = gain_current_level_file_info(r'D:\code\web_explorer\backend', {'name':'api'})
    print(round(size_of/1024, 2))

    #
    print(gain_root_level_info('yuming'))
    pass