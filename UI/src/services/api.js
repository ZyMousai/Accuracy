//跨域代理前缀
const API_PROXY_PREFIX = 'http://192.168.50.115:8000/api'
// const API_PROXY_PREFIX = 'http://127.0.0.1:8000/api'
const BASE_URL = process.env.NODE_ENV === 'production' ? process.env.VUE_APP_API_BASE_URL : API_PROXY_PREFIX
    // const BASE_URL = process.env.VUE_APP_API_BASE_URL
module.exports = {
    LOGIN: `${BASE_URL}/PersonnelManagement/users/v1/login`,
    GetDocumentManagementtTableData: `${BASE_URL}/DocumentManagement/documents/v1`,
    DeleteDocument: `${BASE_URL}/DocumentManagement/documents/v1`,
    GetCreditCardListData: `${BASE_URL}/Clerk/card/v1/card`,
    ROUTES: `${BASE_URL}/routes`,
    USERS: `${BASE_URL}/PersonnelManagement/users/v1/`,

}