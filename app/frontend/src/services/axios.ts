import axios, { AxiosHeaders } from 'axios'

export const getCookie = (cookie_name: string) => {
  let name = cookie_name + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

const refreshAccessToken = () => {
  return refreshAxiosInstance.post(`/api/auth/refresh`)
}


const axiosInstance = axios.create({
  baseURL: '/',
  headers: {
      "Content-Type": "application/json",
    },
  withCredentials: true
});

export const refreshAxiosInstance = axios.create({
  baseURL: '/',
  headers: {
      "Content-Type": "application/json",
    },
  withCredentials: true
});

axiosInstance.interceptors.request.use(
  async config => {
    (config.headers as AxiosHeaders).set("x-csrf-token", getCookie('csrf_access_token'));
    return config;
  },
  error => {
    Promise.reject(error)
  });


axiosInstance.interceptors.response.use((response) => {
  return response
}, async function (error) {
  const originalRequest = error.config;
  if (error.response.status === 401 && !originalRequest._retry) {
    originalRequest._retry = true;
    await refreshAccessToken();            
    return axiosInstance(originalRequest);
  }
  return Promise.reject(error);
});



refreshAxiosInstance.interceptors.request.use(
  async config => {
    (config.headers as AxiosHeaders).set("x-csrf-token", getCookie('csrf_refresh_token'));
    return config;
  },
  error => {
    Promise.reject(error)
})



export default axiosInstance;
