import { Offers } from '@/services/api'
import { request, METHOD } from '@/utils/request'

/**
 * 账号管理页面
 * 查询Offers
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function OffersDate(query) {
    return request(Offers, METHOD.GET, query)
}

/**
 * 账号管理页面
 * 修改Offers
 * @param form  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function OffersEdit(form) {
    return request(Offers, 'PATCH', form)
}