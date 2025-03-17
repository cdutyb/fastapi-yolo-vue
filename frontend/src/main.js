import 'bootstrap/dist/css/bootstrap.css';
import { createApp } from 'vue'
import axios from 'axios';
import App from './App.vue'
import router from './router';
import store from './store';

// 引入Element Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'

const app = createApp(App);

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:5000/';  // the FastAPI backend

axios.interceptors.response.use(undefined, function (error) {
  if (error) {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      store.dispatch('logOut');
      return router.push('/login')
    }
  }
});

// 使用Element Plus，并设置为中文
app.use(ElementPlus, {
  locale: zhCn,
})

app.use(router);
app.use(store);
app.mount("#app");