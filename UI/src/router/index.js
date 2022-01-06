import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '首页', icon: 'dashboard' }
    }]
  },

  {
    path: '/personaldata',
    component: Layout,
    hidden: true,
    children: [{
      path: '/',
      name: 'Personaldata',
      component: () => import('@/views/personaldata/index'),
      meta: { title: '个人资料', icon: 'dashboard' }
    }]
  },

  {
    path: '/documentmanagement',
    component: Layout,
    redirect: '/documentmanagement/document',
    name: 'Documentmanagement',
    meta: {
      title: '文档管理',
      icon: 'el-icon-document'
    },
    children: [
      {
        path: 'document',
        component: () => import('@/views/documentmanagement/document/index'),
        name: 'Document',
        meta: { title: '文档' },
      },
      {
        path: 'recyclebin',
        component: () => import('@/views/documentmanagement/recyclebin/index'),
        name: 'Recyclebin',
        meta: { title: '回收站' },
      }
    ]
  },

  {
    path: '/accountmanagement',
    component: Layout,
    redirect: '/accountmanagement/account',
    name: 'Accountmanagement',
    alwaysShow: true,
    meta: {
      title: '账号管理',
      icon: 'el-icon-user-solid'
    },
    children: [
      {
        path: 'account',
        component: () => import('@/views/accountmanagement/account/index'),
        name: 'Account',
        meta: { title: '账号' },
      }
    ]
  },
  
  {
    path: '/personnelmanagement',
    component: Layout,
    redirect: '/personnelmanagement/usermanagement',
    name: 'Personnelmanagement',
    meta: {
      title: '人员管理',
      icon: 'el-icon-document'
    },
    children: [
      {
        path: 'usermanagement',
        component: () => import('@/views/personnelmanagement/usermanagement/index'),
        name: 'Usermanagement',
        meta: { title: '用户管理' },
      },
      {
        path: 'rolemanagement',
        component: () => import('@/views/personnelmanagement/rolemanagement/index'),
        name: 'Rolemanagement',
        meta: { title: '角色管理' },
      },
      {
        path: 'departmentmanagement',
        component: () => import('@/views/personnelmanagement/departmentmanagement/index'),
        name: 'Departmentmanagement',
        meta: { title: '部门管理' },
      }
    ]
  },
  
  {
    path: '/assistantfunction',
    component: Layout,
    redirect: '/assistantfunction/voluumsiteId',
    name: 'Assistantfunction',
    alwaysShow: true,
    meta: {
      title: '文员功能',
      icon: 'el-icon-user-solid'
    },
    children: [
      {
        path: 'voluumsiteId',
        component: () => import('@/views/assistantfunction/voluumsiteId/index'),
        name: 'VoluumsiteId',
        meta: { title: 'Voluum-SiteId' },
      }
    ]
  },

  {
    path: '/example',
    component: Layout,
    redirect: '/example/table',
    name: 'Example',
    meta: { title: 'Example', icon: 'el-icon-s-help' },
    children: [
      {
        path: 'table',
        name: 'Table',
        component: () => import('@/views/table/index'),
        meta: { title: 'Table', icon: 'table' }
      },
      {
        path: 'tree',
        name: 'Tree',
        component: () => import('@/views/tree/index'),
        meta: { title: 'Tree', icon: 'tree' }
      }
    ]
  },

  {
    path: '/form',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'Form',
        component: () => import('@/views/form/index'),
        meta: { title: 'Form', icon: 'form' }
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

export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
