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
                        },
                        {
                            path: 'addrole',
                            name: '角色新增',
                            meta: {
                                invisible: true,
                            },
                            component: () =>
                                import ('@/pages/personnelmanagement/rolemanagement/roleaddform'),
                        },
                        {
                            path: 'editrole',
                            name: '角色权限编辑',
                            meta: {
                                invisible: true,
                            },
                            component: () =>
                                import ('@/pages/personnelmanagement/rolemanagement/roleaddform'),
                        },
                        {
                            path: 'adddepartment',
                            name: '新增部门',
                            meta: {
                                invisible: true,
                            },
                            component: () =>
                                import ('@/pages/personnelmanagement/departmentmanagement/departmentaddform'),
                        },
                        {
                            path: 'editdepartment',
                            name: '部门权限修改',
                            meta: {
                                invisible: true,
                            },
                            component: () =>
                                import ('@/pages/personnelmanagement/departmentmanagement/departmentaddform'),
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
                        },
                        {
                            path: 'statisticscardinformation',
                            name: '统计卡情况',
                            component: () =>
                                import ('@/pages/assistantfunction/statisticscardinformation'),
                        }
                    ]
                },
                {
                    path: 'trackmanagement',
                    name: '跟踪管理',
                    meta: {
                        icon: 'link',
                    },
                    component: BlankView,
                    children: [{
                            path: 'followlink',
                            name: '跟踪链接',
                            component: () =>
                                import ('@/pages/domainnamemanagement/followlink'),
                        },
                        {
                            path: 'affiliatelist',
                            name: '联盟列表',
                            component: () =>
                                import ('@/pages/domainnamemanagement/affiliatelist'),
                        }
                    ]
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