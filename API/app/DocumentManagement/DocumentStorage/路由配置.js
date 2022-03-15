[{
    router: 'rootrout',
    children: [{
        router: 'dashboard',
    }, {
        router: 'personaldata',
    }, {
        router: 'documentmanagement',
        children: ['document', 'recyclebin']
    }, {
        router: 'accountmanagement',
        children: ['account']
    }, {
        router: 'personnelmanagement',
        children: ['usermanagement', 'rolemanagement', 'departmentmanagement', 'addrole', 'editrole', 'adddepartment', 'editdepartment', ]
    }, {
        router: 'assistantfunction',
        children: ['voluumsiteId', 'statisticscardinformation']
    }, {
        router: 'trackmanagement',
        children: ['followlink', 'affiliatelist']
    }]
}]