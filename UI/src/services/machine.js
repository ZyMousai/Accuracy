import { Machine } from '@/services/api'
import { request, METHOD } from '@/utils/request'

/**
 * 机器管理页面
 * 查询机器
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function MachineDate(query) {
    return request(Machine, METHOD.GET, query)
}

// /**
//  * 机器管理页面
//  * 查询所有机器
//  * @param query  查新请求参数
//  * @returns {Promise<AxiosResponse<T>>}
//  */
// export async function OffersAccountDateAll(query) {
//     return request(OffersAccountAll, METHOD.GET, query)
// }
//
// /**
//  * 机器管理页面
//  * 查询单个机器
//  * @param id  查新请求参数
//  * @returns {Promise<AxiosResponse<T>>}
//  */
// export async function OffersAccountOneDate(id) {
//     return request(OffersAccountOne, METHOD.GET, {
//         user_id: id
//     })
// }

/**
 * 机器管理页面
 * 增加机器
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function MachineAdd(query) {
    return request(Machine, METHOD.POST, query)
}

/**
 * 机器管理页面
 * 修改机器
 * @param form  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function MachineEdit(form) {
    return request(Machine, 'PATCH', form)
}

/**
 * 机器管理页面
 * 删除机器
 * @param ids  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function MachineDelete(ids) {
    return request(Machine, "DELETE", {
        ids: ids,
    })
}
// export async function OffersAccountDelete(ids) {
//     return request(OffersAccount, "DELETE", ids)
// }

