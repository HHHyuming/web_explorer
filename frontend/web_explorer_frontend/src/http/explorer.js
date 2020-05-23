import {request} from './request'

export function add_file(file_path, file_name, desc='') {
  request({
    url: '',
    method: 'post',
    data:{
      file_path: file_path,
      file_name: file_name,
      des: desc
    }
  })

}

export function get_usr_dir_cascade(user_name) {
  return request({
    url: '/explorer/get_user_dir_cascade',
    method: 'get',
    params:{
      user_name,
    }
  })
}

export function index_table_data() {
  return request({

  })

}
