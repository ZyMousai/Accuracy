//跨域代理前缀
// const API_PROXY_PREFIX = 'http://45.76.15.187:8000/api'
//     const API_PROXY_PREFIX = 'http://127.0.0.1:8000/api'
const API_PROXY_PREFIX = 'http://accuracy.vqmjc.cc/api'
// const API_PROXY_PREFIX = 'http://127.0.0.1:8000/api'
    // const API_PROXY_PREFIX = 'http://192.168.50.23:8000/api'
const BASE_URL = process.env.NODE_ENV === 'production' ? process.env.VUE_APP_API_BASE_URL : API_PROXY_PREFIX
    // const BASE_URL = process.env.VUE_APP_API_BASE_URL
module.exports = {
    LOGIN: `${BASE_URL}/PersonnelManagement/users/v1/login`,
    Document: `${BASE_URL}/DocumentManagement/documents/v1/`,
    DeleteDocument: `${BASE_URL}/DocumentManagement/documents/v1/`,
    GetCreditCardListData: `${BASE_URL}/Clerk/card/v1/card`,
    CardAccount: `${BASE_URL}/Clerk/card/v1/account`,
    GetTaskListData: `${BASE_URL}/Clerk/card/v1/task`,
    GetAccountTaskName: `${BASE_URL}/Clerk/card/v1/account_task_name`,
    addcards: `${BASE_URL}/Clerk/card/v1/card`,
    ROUTES: `${BASE_URL}/routes`,
    USERS: `${BASE_URL}/PersonnelManagement/users/v1/`,
    GetOneUSERS: `${BASE_URL}/PersonnelManagement/users/v1/detail`,
    TrackAlliance: `${BASE_URL}/Clerk/track/v1/alliance`,
    ROLES: `${BASE_URL}/PersonnelManagement/roles/v1/`,
    GetOneROLES: `${BASE_URL}/PersonnelManagement/roles/v1/detail`,
    ACCOUNT: `${BASE_URL}/PersonnelManagement/roles/v1/`,
    DEPARTMENTS: `${BASE_URL}/PersonnelManagement/departments/v1/Department`,
    GetOneDEPARTMENTS: `${BASE_URL}/PersonnelManagement/departments/v1/Department/detail`,
    UpdatePassword: `${BASE_URL}/PersonnelManagement/users/v1/password`,
    GetFollowLinkDate: `${BASE_URL}/Clerk/track/v1/execute`,
    AffiliatelistDate: `${BASE_URL}/Clerk/track/v1/alliance`,
    TaskUrl: `${BASE_URL}/Clerk/track/v1/TrackUrl`,
    VoluumsiteIdData: `${BASE_URL}/Clerk/voluum/v1/campaign_mapping`,
    getVoluumsiteIdUrl: `${BASE_URL}/Clerk/voluum/v1/campaign_site_url`,
    CardsExcel: `${BASE_URL}/Clerk/card/v1/cards/excel`,
    RecycleShow: `${BASE_URL}/DocumentManagement/recycle/v1/`,
    RecycleClear: `${BASE_URL}/DocumentManagement/recycle/v1/`,
    RecycleRecover: `${BASE_URL}/DocumentManagement/recycle/v1/recover`,
    Accountmanagement: `${BASE_URL}/AccountManagement/account/v1/`,
    GetOneAccountmanagement: `${BASE_URL}/AccountManagement/account/v1/detail`,
    DepartmentRoleMapping: `${BASE_URL}/PersonnelManagement/departments/v1/DepartmentRoleMapping`,
    DepartmentUserMapping: `${BASE_URL}/PersonnelManagement/departments/v1/DepartmentUserMapping`,
    RoleMenu: `${BASE_URL}/PersonnelManagement/roles/v1/RoleMenu`,
    RolePermission: `${BASE_URL}/PersonnelManagement/roles/v1/RolePermission`,
    RoleUser: `${BASE_URL}/PersonnelManagement/roles/v1/RoleUser`,
    CommissionConsume: `${BASE_URL}/Clerk/card/v1/statistics`,
    RoleAccount: `${BASE_URL}/PersonnelManagement/roles/v1/RoleAccount`,
    DocumentDownloadURL: `${BASE_URL}/DocumentManagement/documents/v1/download`,
    HeartbeatGetServiceName: `${BASE_URL}/Clerk/heartbeat/v1/display`,
    HeartbeatGetServiceNameOne: `${BASE_URL}/Clerk/heartbeat/v1/display/detail`,
}