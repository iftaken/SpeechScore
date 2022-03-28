import { createRouter, createWebHashHistory } from 'vue-router'

import Login from './components/Login.vue'
import Home from './components/Home.vue'

import Tasks from './components/menus/Tasks.vue'
import CreateTask from './components/common/CreateTask.vue'
import TaskDetail from './components/common/TaskDetail.vue'
import ScoreTask from './components/common/ScoreTask.vue'


// 创建路由实例对象
const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', redirect: '/login' },
    { path: '/login', component: Login, name: 'login' },
    {
      path: '/home',
      redirect: '/home/tasks',
      component: Home,
      name: 'home',
      children: [
        { path: 'tasks', component: Tasks },
        { path: 'createTask', component: CreateTask },
        { path: 'taskDetail', component: TaskDetail, props: true },
        { path: 'scoreTask', component: ScoreTask, props: true }
      ],
    },
  ],
})

// 全局路由导航守卫
router.beforeEach((to, from, next) => {
  // 判断用户访问的是否为登录页
  if (to.path === '/login') return next()
  // 获取 token 值
  const tokenStr = localStorage.getItem('token')
  if (!tokenStr) {
    next('/login')
  } else {
    next()
  }
})

export default router
