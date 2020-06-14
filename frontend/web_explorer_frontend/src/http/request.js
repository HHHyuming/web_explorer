import axios from 'axios'


const req_obj = axios.create({
  baseURL: 'http://127.0.0.1:5000',
  // timeout: 5000
})

req_obj.interceptors.request.use(config =>{

  let token = window.sessionStorage.getItem('token')
  console.log('request url', config.url, config.method, token)
  if (token){
    config.headers.Authorization = token
    return config
  }
  return config
}, error => {
  return Promise.reject(error)
})



export function request(config) {

  return req_obj(config)
}


