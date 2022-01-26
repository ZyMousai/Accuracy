import { LOGIN, ROUTES } from '@/services/api'
import { request, METHOD, removeAuthorization } from '@/utils/request'

/**
 * 登录服务
 * @param username  账户名
 * @param password 账户密码
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function login(username, password) {
    return request(LOGIN, METHOD.POST, 'grant_type=&username=' + username + '&password=' + password + '&scope=&client_id=&client_secret=', {
        headers: {
            'Content-type': 'application/x-www-form-urlencoded'
        }
    })
}

export async function getRoutesConfig() {
    return request(ROUTES, METHOD.GET)
}

/**
 * 退出登录
 */
export function logout() {
    localStorage.removeItem(process.env.VUE_APP_ROUTES_KEY)
    localStorage.removeItem(process.env.VUE_APP_PERMISSIONS_KEY)
    localStorage.removeItem(process.env.VUE_APP_ROLES_KEY)
    removeAuthorization()
}
export default {
    login,
    logout,
    getRoutesConfig
}