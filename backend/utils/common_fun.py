import datetime
import os
import base64

import jwt

from config import DEFAULT_EXP_TIME, SECRET_KEY


def calc_dir_size(path):
    """

    :param path:
    :return:
    """

    "{dir_name:xxx,file_list:[],parent_node:none,child_dir_node:[]}"
    dir_list = []

    return


def generate_by_caesar_code(password, step=4):
    caesar_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                   'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                   'z']
    new_code = ''
    for i in password:
        if i.upper() in caesar_list:
            index = caesar_list.index(i.upper())
            new_code += caesar_list[index % len(caesar_list) + step]
        else:
            new_code += i
    code = base64.b64encode(new_code.encode('utf8'))
    return code.decode('utf8')


def caesar_decode(password, step=4):
    caesar_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                   'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                   'z']
    new_code = ''
    password = base64.b64decode(password.encode('utf8')).decode('utf8')

    for i in password:
        if i.upper() in caesar_list:
            index = caesar_list.index(i.upper())
            new_code += caesar_list[index % len(caesar_list) - step]
        else:
            new_code += i
    return new_code


def generate_jwt_code(user_name):
    exp_time = datetime.datetime.utcnow() + datetime.timedelta(hours=DEFAULT_EXP_TIME)
    pay_load = {'exp': exp_time, 'user_name': user_name}
    token = jwt.encode(pay_load, SECRET_KEY).decode('utf8')
    return token


def decode_jwt(token):
    # print(token)
    payload = jwt.decode(token.encode('utf8'), SECRET_KEY)
    return payload


if __name__ == '__main__':
    res = generate_by_caesar_code('admin')
    print(res)
    print(caesar_decode(res))
    """ZWhxbXI =
    ehqmr
    admin"""
    print(caesar_decode('ZWhxbXI='))
    pass