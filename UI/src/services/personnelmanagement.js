import { USERS, DEPARTMENTS } from '@/services/api'
import { request, METHOD } from '@/utils/request'

/**
 * 用户页面
 * 获取用户列表
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function UsersDate(query) {
    return request(USERS, METHOD.GET, query)
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
