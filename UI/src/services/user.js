import { LOGIN, ROUTES, USERS, UpdatePassword } from '@/services/api'
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
 * 获取用户信息
 * @param id  账户ID
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function UserData(id) {
    return request(USERS, METHOD.GET, {
        user_id: id
    })
}

/**
 * 更新用户信息
 * @param userform  用户信息
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function UpUserData(userform) {
    return request(USERS, 'PATCH', userform)
}

/**
 * 更新用户密码
 * @param form  请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function UpPassword(form) {
    return request(UpdatePassword, 'PATCH', form)
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