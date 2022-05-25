import { OffersAccount, OffersAccountOne, OffersAccountAll } from '@/services/api'
import { request, METHOD } from '@/utils/request'

/**
 * 账号管理页面
 * 查询账号
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function OffersAccountDate(query) {
    return request(OffersAccount, METHOD.GET, query)
}

/**
 * 账号管理页面
 * 查询所有账号
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function OffersAccountDateAll(query) {
    return request(OffersAccountAll, METHOD.GET, query)
}

/**
 * 账号管理页面
 * 查询单个账号
 * @param id  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function OffersAccountOneDate(id) {
    return request(OffersAccountOne, METHOD.GET, {
        user_id: id
    })
}

/**
 * 账号管理页面
 * 增加账号
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function OffersAccountAdd(query) {
    return request(OffersAccount, METHOD.POST, query)
}

/**
 * 账号管理页面
 * 修改账号
 * @param form  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function OffersAccountEdit(form) {
    return request(OffersAccount, 'PATCH', form)
}

/**
 * 账号管理页面
 * 删除账号
 * @param ids  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function OffersAccountDelete(ids) {
    return request(OffersAccount, "DELETE", {
        offers_account_ids: ids,
    })
}
// export async function OffersAccountDelete(ids) {
//     return request(OffersAccount, "DELETE", ids)
// }

