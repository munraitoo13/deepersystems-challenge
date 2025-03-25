import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://localhost:7800/api', // Flask backend URL
  timeout: 5000,
})

export default instance
