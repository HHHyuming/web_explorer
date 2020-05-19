import request from './request'

export function user_login(user_name, user_password) {
  return request({
    url: '/user/login',
    data:{
      user_name,
      user_password
    }
  })

}
