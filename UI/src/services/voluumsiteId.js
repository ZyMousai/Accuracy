import { VoluumsiteIdData } from '@/services/api'
import { request, METHOD } from '@/utils/request'

/**
 * voluumsiteId页面
 * 获取voluumsiteId页面表格数据
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function GetVoluumsiteIdData(query) {
    return request(VoluumsiteIdData, METHOD.GET, query)
}

/**
 * voluumsiteId页面
 * 添加voluumsiteId表格数据
 * @param form  添加请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function AddDate(form) {
    return request(VoluumsiteIdData, METHOD.POST, form)
}

/**
 * voluumsiteId页面
 * 添加voluumsiteId表格数据
 * @param id  删除请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function DeleteDate(id) {
    return request(VoluumsiteIdData, "DELETE", {
        ids: id
    })
}