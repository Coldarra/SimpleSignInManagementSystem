import Vue from 'vue'
import Router from 'vue-router'
// import Home from './views/Home.vue'

Vue.use(Router)

export default new Router({
  // mode: 'history',
  routes: [
    {
      path: '/',
      name: 'index',
      component: () => import('@/components/index.vue'),
      meta: {
        requireLogin: false,
        requreAdmin: false,
        title: "首页"
      }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/components/login.vue'),
      meta: {
        requireLogin: false,
        requreAdmin: false,
        title:"登录"
      }
    },
    {
      path: '/manage',
      name: 'manage',
      component: () => import('@/components/manage.vue'),
      meta: {
        requireLogin: true,
        requreAdmin: false,
        title:"人员管理"
      }
    },
    {
      path: '/meeting',
      name: 'meeting',
      component: () => import('@/components/meetings.vue'),
      meta: {
        requireLogin: true,
        requreAdmin: false,
        title:"会议"
      }
    },
    {
      path: '/meeting/:meeting_id',
      name: 'name_detail',
      component: () => import('@/components/meeting_detail.vue'),
      meta: {
        requireLogin: true,
        requreAdmin: false,
        title:"会议详情"
      }
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
    }
  ]
})
