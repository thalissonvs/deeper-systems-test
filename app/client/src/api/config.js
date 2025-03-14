import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api', // This will be proxied by Nginx to the backend service
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  timeout: 10000
});

export default apiClient; 