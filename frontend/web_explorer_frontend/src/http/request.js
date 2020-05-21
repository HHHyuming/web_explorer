import axios from 'axios'


const req_obj = axios.create({
  baseURL: 'http://127.0.0.1:5000',
  // timeout: 5000
})

export function request(config) {

  return req_obj(config)
}


