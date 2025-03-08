// 导入 axios 库，用于发送 HTTP 请求
import axios from 'axios';

// 定义状态
const state = {
  // 存储当前用户的对象
  user: null,
};

// 定义获取器
const getters = {
  // 判断用户是否已登录
  isAuthenticated: state =>!!state.user,
  // 获取当前用户
  stateUser: state => state.user,
};

// 定义动作
const actions = {
  // 注册新用户
  async register({dispatch}, form) {
    // 发送 POST 请求到 register 接口
    await axios.post('register', form);
    // 创建一个 FormData 对象，用于登录
    let UserForm = new FormData();
    // 将用户名和密码添加到 FormData 对象中
    UserForm.append('username', form.username);
    UserForm.append('password', form.password);
    // 调用 logIn 动作进行登录
    await dispatch('logIn', UserForm);
  },
  // 用户登录
  async logIn({dispatch}, user) {
    // 发送 POST 请求到 login 接口
    await axios.post('login', user);
    // 调用 viewMe 动作获取当前用户信息
    await dispatch('viewMe');
  },
  // 获取当前用户信息
  async viewMe({commit}) {
    // 发送 GET 请求到 users/whoami 接口
    let {data} = await axios.get('users/whoami');
    // 将获取到的用户数据提交到 mutations 中更新状态
    await commit('setUser', data);
  },
  // 删除用户（仅供参考，可能需要根据实际需求进行调整）
  // eslint-disable-next-line no-empty-pattern
  async deleteUser({}, id) {
    // 发送 DELETE 请求到 user/id 接口
    await axios.delete(`user/${id}`);
  },
  // 用户登出
  async logOut({commit}) {
    // 将用户设置为 null，表示用户已登出
    let user = null;
    // 提交 logout 突变来更新状态
    commit('logout', user);
  }
};

// 定义突变
const mutations = {
  // 设置当前用户
  setUser(state, username) {
    state.user = username;
  },
  // 用户登出时调用，将用户设置为 null
  logout(state, user){
    state.user = user;
  },
};

// 导出 Vuex 模块
export default {
  state,
  getters,
  actions,
  mutations
};