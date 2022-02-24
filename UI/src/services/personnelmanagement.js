import { USERS, ROLES, DEPARTMENTS, UpdatePassword } from '@/services/api'
import { request, METHOD } from '@/utils/request'

/**
 * 用户页面
 * 查询用户
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function UsersDate(query) {
    return request(USERS, METHOD.GET, query)
}

/**
 * 用户页面
 * 查询单个用户
 * @param id  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function GetOneUsersDate(id) {
    return request(USERS + id, METHOD.GET, '')
}

/**
 * 用户页面
 * 增加用户
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function UsersAdd(query) {
    return request(USERS, METHOD.POST, query)
}

/**
 * 用户页面
 * 增加用户
 * @param form  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function UsersEdit(form) {
    return request(USERS, 'PATCH', form)
}
/**
 * 删除用户
 * @param id  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function DeleteUsers(id) {
    return request(USERS, "DELETE", {
        ids: id,
    })
}

/**
 * 角色管理页面
 * 获取角色列表
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function RolesDate(query) {
    return request(ROLES, METHOD.GET, query)
}

/**
 * 删除角色
 * @param id  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function DeleteRoles(id) {
    return request(ROLES, "DELETE", {
        ids: id,
    })
}

/**
 * 角色管理页面
 * 重置密码
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function RolesResetPassword(query) {
    return request(UpdatePassword, "PATCH", query)
}



/**
 * 部门页面
 * 获取部门列表
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function DepartmentDate(query) {
    return request(DEPARTMENTS, METHOD.GET, query)
}


/**
 * 删除部门
 * @param id  查新请求参数
 * @param is_logic_del  是否是逻辑删除
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function DeleteDepartment(id, is_logic_del) {
    return request(DEPARTMENTS, METHOD.DELETE, {
        ids: id,
        is_logic_del: is_logic_del
    })
}