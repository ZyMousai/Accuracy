// 视图组件
const view = {
    tabs: () =>
        import ('@/layouts/tabs'),
    TabsView: () =>
        import ('@/layouts/tabs/TabsView'),
    BlankView: () =>
        import ('@/layouts/BlankView'),
    page: () =>
        import ('@/layouts/PageView')
}

// 路由组件注册
const routerMap = {
    login: {
        authority: '*',
        path: '/login',
        component: () =>
            import ('@/pages/login')
    },
    rootrout: {
        path: '/',
        name: '首页',
        component: view.TabsView,
        redirect: '/login',
    },
    dashboard: {
        path: 'dashboard',
        name: '首页',
        icon: 'home',
        component: () =>
            import ('@/pages/dashboard')
    },
    personaldata: {
        path: 'personaldata',
        name: '个人资料',
        invisible: true,
        component: () =>
            import ('@/pages/personaldata')
    },
    documentmanagement: {
        path: 'documentmanagement',
        name: '文档管理',
        icon: 'folder-open',
        component: view.BlankView,
    },
    document: {
        path: 'document',
        name: '文档',
        component: () =>
            import ('@/pages/documentmanagement/document')
    },
    recyclebin: {
        path: 'recyclebin',
        name: '回收站',
        component: () =>
            import ('@/pages/documentmanagement/recyclebin')
    },
    accountmanagement: {
        path: 'accountmanagement',
        name: '账号管理',
        icon: 'safety',
        component: view.BlankView,
    },
    account: {
        path: 'account',
        name: '账号',
        component: () =>
            import ('@/pages/accountmanagement')
    },
    personnelmanagement: {
        path: 'personnelmanagement',
        name: '人员管理',
        icon: 'user',
        component: view.BlankView,
    },
    usermanagement: {
        path: 'usermanagement',
        name: '用户管理',
        component: () =>
            import ('@/pages/personnelmanagement/usermanagement')
    },
    rolemanagement: {
        path: 'rolemanagement',
        name: '角色管理',
        component: () =>
            import ('@/pages/personnelmanagement/rolemanagement')
    },
    departmentmanagement: {
        path: 'departmentmanagement',
        name: '部门管理',
        component: () =>
            import ('@/pages/personnelmanagement/departmentmanagement')
    },
    addrole: {
        path: 'addrole',
        name: '角色新增',
        invisible: true,
        component: () =>
            import ('@/pages/personnelmanagement/rolemanagement/roleaddform')
    },
    editrole: {
        path: 'editrole',
        name: '角色权限编辑',
        invisible: true,
        component: () =>
            import ('@/pages/personnelmanagement/rolemanagement/roleaddform')
    },
    adddepartment: {
        path: 'adddepartment',
        name: '新增部门',
        invisible: true,
        component: () =>
            import ('@/pages/personnelmanagement/departmentmanagement/departmentaddform')
    },
    editdepartment: {
        path: 'editdepartment',
        name: '部门权限修改',
        invisible: true,
        component: () =>
            import ('@/pages/personnelmanagement/departmentmanagement/departmentaddform')
    },
    assistantfunction: {
        path: 'assistantfunction',
        name: '文员功能',
        icon: 'appstore',
        component: view.BlankView,
    },
    voluumsiteId: {
        path: 'voluumsiteId',
        name: 'Voluum-SiteId',
        component: () =>
            import ('@/pages/assistantfunction/voluumsiteId')
    },
    statisticscardinformation: {
        path: 'statisticscardinformation',
        name: '统计卡情况',
        component: () =>
            import ('@/pages/assistantfunction/statisticscardinformation')
    },
    trackmanagement: {
        path: 'trackmanagement',
        name: '跟踪管理',
        icon: 'link',
        component: view.BlankView,
    },
    followlink: {
        path: 'followlink',
        name: '跟踪链接',
        component: () =>
            import ('@/pages/domainnamemanagement/followlink')
    },
    affiliatelist: {
        path: 'affiliatelist',
        name: '联盟列表',
        component: () =>
            import ('@/pages/domainnamemanagement/affiliatelist')
    },
    systemmanagement:{
        path:'systemmanagement',
        name:'系统管理',
        icon: 'setting',
        component: view.BlankView,
    },
    heartbeatfunction: {
        path: 'heartbeatfunction',
        name: '心跳功能',
        component: () =>
            import ('@/pages/systemmanagement/heartbeatfunction')
    },
    machine:{
        path:"machine",
        name:"机器",
        component:()=>
            import ('@/pages/systemmanagement/machine')
    },
    offerssystem:{
        path:'offerssystem',
        name:'offers系统',
        icon: 'setting',
        component: view.BlankView,
    },
    offersalliance: {
        path: 'offersalliance',
        name: '联盟管理',
        component: () =>
            import ('@/pages/offerssystem/offersalliance')
    },
    offersaccount: {
        path: 'offersaccount',
        name: '账号管理',
        component: () =>
            import ('@/pages/offerssystem/offersaccount')
    },
    offers: {
        path: 'offers',
        name: 'offers',
        component: () =>
            import ('@/pages/offerssystem/offers')
    },
    exp403: {
        authority: '*',
        name: 'exp403',
        path: '403',
        component: () =>
            import ('@/pages/exception/403')
    },
    exp404: {
        name: 'exp404',
        path: '404',
        component: () =>
            import ('@/pages/exception/404')
    },
    exp500: {
        name: 'exp500',
        path: '500',
        component: () =>
            import ('@/pages/exception/500')
    },
    exception: {
        name: '异常页',
        icon: 'warning',
        component: view.BlankView
    }
}
export default routerMap