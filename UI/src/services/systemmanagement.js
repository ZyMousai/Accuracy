import{HeartbeatGetServiceName, HeartbeatGetServiceNameOne} from '@/services/api'
import { request, METHOD } from '@/utils/request'
/**
 * 心跳功能
 * 查询服务
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
 export async function GetServiceNameDate(query) {
    return request(HeartbeatGetServiceName, METHOD.GET, query)
}

/**
 * 心跳功能
 * 查询单个服务
 * @param id  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
 export async function GetServiceNameDateOne(id) {
        return request(HeartbeatGetServiceNameOne, METHOD.GET, {
        id: id
    })
}

/**
 * 心跳功能
 * 修改心跳功能注册列表
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function PatchHeartbeatDisplay(query) {
    return request(HeartbeatGetServiceName, "PATCH", query)
}

/**
 * 心跳功能
 * 新增心跳功能注册列表
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function AddHeartbeatDisplay(query) {
    return request(HeartbeatGetServiceName, METHOD.POST, query)
}

/**
 * 心跳功能
 * 删除心跳功能注册列表
 * @param id  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function DeleteHeartbeatDisplay(id) {
    return request(HeartbeatGetServiceName, "DELETE", {
        ids: id
    })
}