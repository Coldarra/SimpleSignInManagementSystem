import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    userInfo: {},
    isLogin: false,
    logining: false,
  },
  getters: {
    isLogin: state => state.isLogin,
    logining: state => state.logining,
  },
  mutations: {
    updateUserInfo(state, data) {
      localStorage.setItem('token', data.token);
      localStorage.setItem('username', data.user.username);
      localStorage.setItem('level', data.user.level);
      state.userInfo = data.user
      state.isLogin = true
    },
    clearUserInfo(state) {
      localStorage.removeItem("token");
      localStorage.removeItem("username");
      localStorage.removeItem("level");
      state.userInfo = {}
      state.isLogin = false
    }
  },
  actions: {

  }
})
