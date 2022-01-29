import { AffiliatelistDate, TaskUrl } from '@/services/api'
import { request, METHOD } from '@/utils/request'

/**
 * 联盟列表页面
 * 获取联盟列表表格数据
 * @param query  查询请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function GetAffiliatelistDate(query) {
    return request(AffiliatelistDate, METHOD.GET, query)
}

/**
 * 联盟列表页面
 * 添加数据
 * @param form  添加请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function AddDate(form) {
    return request(AffiliatelistDate, METHOD.POST, form)
}

/**
 * 联盟列表页面
 * 编辑数据
 * @param form  编辑请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function EditDate(form) {
    return request(AffiliatelistDate, "PATCH", form)
}

/**
 * 联盟列表页面
 * 删除父表数据
 * @param ids  添加请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function DeleteDate(ids) {
    return request(AffiliatelistDate, "DELETE1", ids)
}

/**
 * 联盟列表页面
 * 添加跟踪域链接
 * @param form  添加请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function AddTaskUrlDate(form) {
    return request(TaskUrl, METHOD.POST, form)
}