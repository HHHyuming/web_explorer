import {request} from './request'
import qs from 'qs'
let xx = {headers:{'Content-Type':'multipart/form-data'},};

export function search_content(content) {
  return request({
    url:'/explorer/search',
    method:'get',
    params:{search_name:content}
  })

}

export function change_directory(change_path) {
  console.log('request params -------',change_path)
  return request({
    url:'/explorer/change_directory',
    method:'post',
    data:{change_path:change_path}
  })
}

export function new_cascade() {
  return request({
    url:'/explorer/new_cascade',
    method:'get',
    params:{
    }
  })

}

export function download_file(data_list) {
  console.log(data_list)
  return request({
    url: '/explorer/download_file',
    method: 'post',
    data:data_list,
    responseType: 'blob'
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
  console.log('delete list---',delete_list)
  return request({
    url: '/explorer/delete_file',
    method: 'post',
    data:{
      delete_list:delete_list
    }
  })
}

export function index_data(user_name) {
  return request({
    headers:{'Content-Type':'application/json'},
    url: '/explorer/index',
    method: 'get',
    params:{user_name
    }
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
