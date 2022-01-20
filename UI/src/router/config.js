import TabsView from '@/layouts/tabs/TabsView'
import BlankView from '@/layouts/BlankView'
// import PageView from '@/layouts/PageView'

// 路由配置
const options = {
    routes: [{
            path: '/login',
            name: '登录页',
            component: () =>
                import ('@/pages/login')
        },
        {
            path: '/400',
            name: '404',
            component: () =>
                import ('@/pages/exception/404'),
        },
        {
            path: '/403',
            name: '403',
            component: () =>
                import ('@/pages/exception/403'),
        },
        {
            path: '/',
            name: '首页',
            component: TabsView,
            redirect: '/login',
            children: [{
                    path: 'dashboard',
                    name: '首页',
                    meta: {
                        icon: 'home'
                    },
                    component: () =>
                        import ('@/pages/dashboard')
                },
                {
                    path: 'personaldata',
                    name: '个人资料',
                    meta: {
                        invisible: true
                    },
                    component: () =>
                        import ('@/pages/personaldata')
                },
                {
                    path: 'documentmanagement',
                    name: '文档管理',
                    meta: {
                        icon: 'folder-open',
                    },
                    component: BlankView,
                    children: [{
                            path: 'document',
                            name: '文档',
                            component: () =>
                                import ('@/pages/documentmanagement/document'),
                        },
                        {
                            path: 'recyclebin',
                            name: '回收站',
                            component: () =>
                                import ('@/pages/documentmanagement/recyclebin'),
                        }
                    ]
                },
                {
                    path: 'accountmanagement',
                    name: '账号管理',
                    meta: {
                        icon: 'safety',
                    },
                    component: BlankView,
                    children: [{
                        path: 'account',
                        name: '账号',
                        component: () =>
                            import ('@/pages/accountmanagement'),
                    }]
                },
                {
                    path: 'personnelmanagement',
                    name: '人员管理',
                    meta: {
                        icon: 'user',
                    },
                    component: BlankView,
                    children: [{
                            path: 'usermanagement',
                            name: '用户管理',
                            component: () =>
                                import ('@/pages/personnelmanagement/usermanagement'),
                        },
                        {
                            path: 'rolemanagement',
                            name: '角色管理',
                            component: () =>
                                import ('@/pages/personnelmanagement/rolemanagement'),
                        },
                        {
                            path: 'departmentmanagement',
                            name: '部门管理',
                            component: () =>
                                import ('@/pages/personnelmanagement/departmentmanagement'),
                        }
                    ]
                },
                {
                    path: 'assistantfunction',
                    name: '文员功能',
                    meta: {
                        icon: 'appstore',
                    },
                    component: BlankView,
                    children: [{
                        path: 'voluumsiteId',
                        name: 'Voluum-SiteId',
                        component: () =>
                            import ('@/pages/assistantfunction/voluumsiteId'),
                    }]
                },
                {
                    name: '验权页面',
                    path: 'auth/demo',
                    meta: {
                        icon: 'file-ppt',
                        authority: {
                            permission: 'form',
                            role: 'manager'
                        },
                        component: () =>
                            import ('@/pages/demo')
                    }
                }
            ]
        }
    ]
}

export default options