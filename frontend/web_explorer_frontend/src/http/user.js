import {request} from './request'
import Qs from 'qs'


export function user_login(user_name, user_password) {
  return request({
    // headers:{'Content-Type':'application/json'},
    url: '/user/login',
    method: 'post',
    data: {
      user_name:user_name,
      user_password:user_password
    }
  })

}

export function user_register(user_name, user_password, sec_password) {
  return request({
    url: '/user/register',
    method:'post',
    data:{
      user_name,
      user_password,
      sec_password,
    },

  })

}


