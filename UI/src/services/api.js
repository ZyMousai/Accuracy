//跨域代理前缀
const API_PROXY_PREFIX = 'http://192.168.50.49:8000/api'
    // const API_PROXY_PREFIX = 'http://127.0.0.1:8000/api'
const BASE_URL = process.env.NODE_ENV === 'production' ? process.env.VUE_APP_API_BASE_URL : API_PROXY_PREFIX
    // const BASE_URL = process.env.VUE_APP_API_BASE_URL
module.exports = {
    LOGIN: `${BASE_URL}/PersonnelManagement/users/v1/login`,
    Document: `${BASE_URL}/DocumentManagement/documents/v1`,
    DeleteDocument: `${BASE_URL}/DocumentManagement/documents/v1`,
    GetCreditCardListData: `${BASE_URL}/Clerk/card/v1/card`,
    ROUTES: `${BASE_URL}/routes`,
    USERS: `${BASE_URL}/PersonnelManagement/users/v1/`,
    TrackAlliance: `${BASE_URL}/Clerk/track/v1/alliance`,
    ROLES: `${BASE_URL}/PersonnelManagement/roles/v1/`,
    ACCOUNT: `${BASE_URL}/PersonnelManagement/roles/v1/`,
    DEPARTMENTS: `${BASE_URL}/PersonnelManagement/departments/v1/Department`,
    UpdatePassword: `${BASE_URL}/PersonnelManagement/users/v1/password`,
    GetFollowLinkDate: `${BASE_URL}/Clerk/track/v1/execute`,
    AffiliatelistDate: `${BASE_URL}/Clerk/track/v1/alliance`,
    TaskUrl: `${BASE_URL}/Clerk/track/v1/TrackUrl`,
    VoluumsiteIdData: `${BASE_URL}/Clerk/voluum/v1/campaign_mapping`,
    getVoluumsiteIdUrl: `${BASE_URL}/Clerk/voluum/v1/campaign_site_url/`,
    RecycleShow: `${BASE_URL}/DocumentManagement/recycle/v1/`,
    RecycleClear: `${BASE_URL}/DocumentManagement/recycle/v1/`,
    RecycleRecover: `${BASE_URL}/DocumentManagement/recycle/v1/recover`,
}