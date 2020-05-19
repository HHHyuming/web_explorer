import axios from 'axios'


export function request(config) {
  const req_obj = axios.create({
    baseURL: 'http://127.0.0.1:5000',
    timeout: 5000
  })
  return req_obj
}


