import { GetCreditCardListData } from '@/services/api'
import { request, METHOD } from '@/utils/request'

/**
 * 统计卡页面
 * 获取统计卡父表格数据
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function CreditCardListData(query) {
    return request(GetCreditCardListData, METHOD.GET, query)
}

/**
 * 统计卡页面
 * 修改统计卡父表格数据
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function PatchCardListData(query) {
    return request(GetCreditCardListData, "PATCH", query)
}