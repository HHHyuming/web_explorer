import os
import base64

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
        index = caesar_list.index(i)
        new_code += caesar_list[index+step]

    code = base64.b64encode(new_code.encode('utf8'))
    return code.decode('utf8')


def caesar_decode(password, step=4):
    caesar_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                   'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                   'z']
    new_code = ''
    password = base64.b64decode(password.encode('utf8')).decode('utf8')

    for i in password:
        index = caesar_list.index(i)
        new_code += caesar_list[index-step]

    return new_code


if __name__ == '__main__':
    # res = generate_by_caesar_code('abcdef')
    # print(res)
    # print(caesar_decode(res))
    pass