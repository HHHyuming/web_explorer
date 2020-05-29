import {request} from './request'
import qs from 'qs'
let xx = {headers:{'Content-Type':'multipart/form-data'},};


export function download_file(data_list) {
  return request({
    url: '/explorer/download_file',
    method: 'post',
    data:data_list
  })
}


export function upload_file(form_data) {

  return request({
    url: '/explorer/upload_file',
    method: 'post',
    data:form_data
  })
}

export function delete_file(delete_list) {
  return request({
    url: '/explorer/delete_file',
    method: 'post',
    data:{
      delete_list:delete_list
    }
  })
}

export function index_data() {
  return request({
    url: '/explorer/index',
    method: 'get',

  })
}

export function add_file(file_path, file_name, desc='') {
  return request({
    headers:{'Content-Type':'application/json'},
    url: '/explorer/create_folder',
    method: 'post',
    data:{
      file_path: file_path,
      file_name: file_name,
      desc: desc
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
