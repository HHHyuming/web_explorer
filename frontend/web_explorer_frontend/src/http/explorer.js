import {request} from './request'

export function add_file(file_path, file_name, desc) {
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
