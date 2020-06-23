import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

export const constantRoutes = [
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path(.*)',
        component: () => import('@/views/redirect/index')
      }
    ]
  },
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/auth-redirect',
    component: () => import('@/views/login/auth-redirect'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/error-page/404'),
    hidden: true
  },
  {
    path: '/401',
    component: () => import('@/views/error-page/401'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        component: () => import('@/views/dashboard/index'),
        name: 'Dashboard',
        meta: { title: 'Dashboard', icon: 'dashboard', affix: true }
      }
    ]
  },
  {
    path: '/user',
    component: Layout,
    hidden: true,
    redirect: 'noredirect',
    children: [
      {
        path: '/user/center',
        component: () => import('@/views/user/index'),
        name: '个人中心',
        meta: { title: '个人中心', icon: 'user' }
      }
    ]
  }
]

export const asyncRoutes = [
  // {
  //   path: '/book',
  //   name: 'book',
  //   component: Layout,
  //   redirect: 'noRedirect',
  //   alwaysShow: true,
  //   meta: { title: '图书管理', icon: 'documentation', roles: ['ceshi'] },
  //   children: [
  //     {
  //       path: '/book/create',
  //       name: 'BookCreate',
  //       component: () => import('@/views/book/create'),
  //       meta: { title: '上传图书', icon: 'edit', roles: ['ceshi'], keepAlive: true }
  //     },
  //     {
  //       path: '/book/edit',
  //       name: 'bookEdit',
  //       component: () => import('@/views/book/edit'),
  //       hidden: true,
  //       meta: { title: '编辑图书', icon: 'edit', roles: ['ceshi'], activeMenu: '/book/list' }
  //     },
  //     {
  //       path: '/book/list',
  //       name: 'BookList',
  //       component: () => import('@/views/book/list'),
  //       meta: { title: '图书列表', icon: 'list', roles: ['ceshi'] }
  //     }
  //   ]
  // },
  {
    path: '/project',
    name: 'project',
    component: Layout,
    redirect: 'noRedirect',
    alwaysShow: true,
    meta: { title: '项目管理', icon: 'documentation', roles: ['运维组'] },
    children: [
      {
        path: '/project/project',
        name: 'Project',
        component: () => import('@/views/project/project'),
        meta: { title: '项目列表', icon: 'user', roles: ['运维组'], noCache: true }
      },
      {
        path: '/project/region',
        name: 'ProjectRegion',
        component: () => import('@/views/project/projectRegion'),
        meta: { title: '地区列表', icon: 'user', roles: ['运维组'], noCache: true }
      },
      {
        path: '/project/area',
        name: 'ProjectArea',
        component: () => import('@/views/project/projectArea'),
        meta: { title: '大区列表', icon: 'user', roles: ['运维组'], noCache: true }
      },
      {
        path: '/project/role',
        name: 'ProjectRole',
        component: () => import('@/views/project/projectRole'),
        meta: { title: '角色列表', icon: 'user', roles: ['运维组'], noCache: true }
      }
    ]
  },
  {
    path: '/cmdb',
    name: 'cmdb',
    component: Layout,
    redirect: 'noRedirect',
    alwaysShow: true,
    meta: { title: '服务器管理', icon: 'documentation', roles: ['运维组'] },
    children: [
      {
        path: '/cmdb/servers',
        name: 'ServersList',
        component: () => import('@/views/cmdb/serverslist'),
        meta: { title: '服务器列表', icon: 'user', roles: ['运维组'], noCache: false }
      }
    ]
  },
  {
    path: '/tasks',
    name: 'tasks',
    component: Layout,
    redirect: 'noRedirect',
    alwaysShow: true,
    meta: { title: '任务管理', icon: 'documentation', roles: ['运维组'] },
    children: [
      {
        path: '/tasks/updateServersDatetime',
        name: 'UpdateServersDatetime',
        component: () => import('@/views/tasks/updateServersDatetime'),
        meta: { title: '更新服务器时间', icon: 'user', roles: ['运维组'], noCache: true }
      }
    ]
  },
  {
    path: '/system',
    name: 'system',
    component: Layout,
    redirect: 'noRedirect',
    alwaysShow: true,
    meta: { title: '系统管理', icon: 'documentation', roles: ['运维组', '运营组'] },
    children: [
      {
        path: '/system/users',
        name: 'Users',
        component: () => import('@/views/system/users'),
        meta: { title: '用户管理', icon: 'user', roles: ['运维组'], noCache: true }
      },
      {
        path: '/system/groups',
        name: 'Groups',
        component: () => import('@/views/system/groups'),
        meta: { title: '角色管理', icon: 'peoples', roles: ['运维组'], noCache: true }
      },
      {
        path: '/system/ipWhiteList.vue',
        name: 'ipWhiteList.vue',
        component: () => import('@/views/system/ipWhiteList.vue'),
        meta: { title: 'IP白名单', icon: 'peoples', roles: ['运维组', '运营组'], noCache: true }
      }
    ]
  },
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
