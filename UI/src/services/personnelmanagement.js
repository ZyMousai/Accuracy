import { USERS } from '@/services/api'
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
