import os
from flask import request


from config import USER_HOME_DIR


def init_user_data(user_name):
    user_current_dir = os.path.join(USER_HOME_DIR, user_name)
    if os.path.exists(user_current_dir):
        return False
    if not os.path.exists(user_current_dir):
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
    file_list = os.listdir(user_current_dir)
    for file in file_list:
        current_test_path = os.path.join(user_current_dir, file)
        create_time = os.stat(current_test_path).st_ctime
        update_time = os.stat(current_test_path).st_mtime
        if os.path.isfile(current_test_path):
            file_name, file_type = current_test_path.rsplit('.')
            size = os.stat(current_test_path).st_size

            item = {'name': file, 'file_type': file_type, 'size': size, 'create_time': create_time,
                    'update_time': update_time, 'author': user_name, 'desc': '', 'level': 1,
                    'path': user_name + '/' + file}
            data_list.append(item)
        if os.path.isdir(current_test_path):
            item = {'name': file, 'file_type': None, 'size': None, 'create_time': create_time,
                    'update_time': update_time, 'author': user_name, 'desc': '', 'level': 1,
                    'path': user_name + '/' + file}
            size = gain_current_level_file_info(user_current_dir, item)
            item['size'] = size
            dir_list.append(item)
    return dir_list, data_list


def gain_current_level_file_info(file_path, file):
    size = 0

    real_path = os.path.join(file_path, file)
    for root_dir, current_dir, file_list in os.walk(real_path):
        for real_file in file_list:
            size += os.stat(os.path.join(root_dir, real_file)).st_size
    return size


def create_dir(file_path, file_name):

    path = os.path.join(file_path, file_name)
    if not os.path.exists(path):
        os.mkdir(path)
        return True


def get_cascade_path(root_file_path):
    """

    返回符合element ui cascade 级联数据
    :param root_file_path: 'xxx/xxxx/xxx/user_name'
    :return:
    """

    class Node:
        """
        node --> list dir
        """
        def __init__(self, data):
            self.data = data
            self.next = None
            self.tail = None

        def __str__(self):
            return str(self.data)

    dir_item_stack = [Node({'name': os.path.basename(root_file_path), 'path': root_file_path})]
    root_node = Node(data='')
    root_node.next = dir_item_stack[0]
    root_node.tail = dir_item_stack[0]
    while dir_item_stack:
        calc_dir = dir_item_stack.pop()
        calc_file_path = calc_dir.data['path']
        dir_list = os.listdir(calc_file_path)
        temp_list = []
        for file in dir_list:
            current_path = os.path.join(calc_file_path, file)
            # 数据链路
            x = Node({'name': file, 'path': current_path})
            dir_item_stack.append(x)
            temp_list.append(x)
        else:
            if temp_list:
                pub = Node(data=[*temp_list])
            else:
                pub = Node(data='')
            calc_dir.next = pub
            root_node.tail = pub
            temp_list.clear()

    data_stack = [root_node.next]

    while data_stack:
        master_node = data_stack.pop()

        if master_node.next or master_node.data:

            if isinstance(master_node.next.data, list):
                if bool(master_node.next):
                    # print(master_node.data, master_node.next, type(master_node.next))
                    # print(master_node.data)
                    master_node.data['children'] = []
                    for node in master_node.next.data:
                        v = node.data.pop('name')
                        node.data.pop('path')
                        node.data['label'] = v
                        node.data['value'] = v
                        master_node.data['children'].append(node.data)
                        data_stack.append(node)
    return root_node.next





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
    # size_of = gain_current_level_file_info(r'D:\code\web_explorer\backend', {'name':'api'})
    # print(round(size_of/1024, 2))

    #
    # d1, d2 = gain_root_level_info('yuming')
    # print(d1)
    # print(d2)
    res = get_cascade_path(r'D:\code\web_explorer\backend\data\admin')
    print(res)