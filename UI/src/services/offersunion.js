import { OffersUnion, OffersUnionOne, OffersUnionSystem, OffersUnionAll } from '@/services/api'
import { request, METHOD } from '@/utils/request'

/**
 * 联盟管理页面
 * 查询联盟
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function OffersUnionDate(query) {
    return request(OffersUnion, METHOD.GET, query)
}

/**
 * 联盟管理页面
 * 查询联盟所有数据
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function OffersUnionDateAll(query) {
    return request(OffersUnionAll, METHOD.GET, query)
}

/**
 * 联盟管理页面
 * 查询单个联盟
 * @param id  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function OffersUnionOneDate(id) {
    return request(OffersUnionOne, METHOD.GET, {
        user_id: id
    })
}

/**
 * 联盟管理页面
 * 增加联盟
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function OffersUnionAdd(query) {
    return request(OffersUnion, METHOD.POST, query)
}

/**
 * 联盟管理页面
 * 修改联盟
 * @param form  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function OffersUnionEdit(form) {
    return request(OffersUnion, 'PATCH', form)
}

/**
 * 联盟管理页面
 * 删除联盟
 * @param ids  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function OffersUnionDelete(ids) {
    return request(OffersUnion, "DELETE", {
        offers_union_ids: ids,
    })
}
// export async function OffersUnionDelete(ids) {
//     return request(OffersUnion, "DELETE", ids)
// }


/**
 * 联盟管理页面
 * 查询追踪系统
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function OffersUnionSystemDate(query) {
    return request(OffersUnionSystem, METHOD.GET, query)
}