import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Public from './public'


import ElementUI from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
import "font-awesome/css/font-awesome.min.css";

import axios from "axios";
import qs from "qs";
axios.defaults.headers.post["Content-Type"] =
  "application/x-www-form-urlencoded";

Vue.use(ElementUI);
Vue.use(router);

Vue.config.productionTip = false
if (process.env.NODE_ENV === "production")
  axios.defaults.baseURL = "http://cs161.cn:18000/";
  // axios.defaults.baseURL = "http://0.0.0.0:8000/";

Vue.prototype.$ajax = axios;
Vue.prototype.Public = Public;


axios.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded"

axios.interceptors.request.use(
  function (config) {
    // console.log(config.data);
    var token = localStorage.getItem("token");
    // console.log("token:",token);

    if (token) {
      config.headers.common["Authorization"] = token;
    }
    config.data = qs.stringify(config.data);
    // console.log(config.data);
    return config;
  },
  function (error) {
    return Promise.reject(error);
  }
);
axios.interceptors.response.use(
  function (res) {
    console.log(res);
    if (res.data.ret != "0") {
      switch (res.data.ret) {
        case "10":
          // store.commit("clearUserInfo");
          router.push({
            path: "/login",
            querry: { redirect: router.currentRoute.fullPath } //从哪个页面跳转
          });
          break;
        default:
          break;
      }
      Vue.prototype.$message({
        message: res.data.msg,
        type: "warning"
        // duration: 0,
      });
    }
    return res;
  },
  function () {
    Vue.prototype.$message({
      message: "服务器请求失败",
      type: "error"
      // duration: 0,
    });
  }
);

router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title
  }
  if (to.meta.requireAdmin) {
    if (localStorage.getItem("level") == "admin") next();
    else {
      next({
        path: "/"
      });
      Vue.prototype.$message({
        message: "无此权限",
        type: "error"
      });
    }
  } else if (to.meta.requireLogin) {
    // console.log("localStorage:", localStorage.getItem("username"));
    if (localStorage.getItem("username")) {
      next();
    } else {
      next({
        path: "/login",
        query: { redirect: to.fullPath }
      });
      Vue.prototype.$message({
        message: "请先登录",
        type: "warning"
        // duration: 0,
      });
    }
  } else {
    next();
  }
});



new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
