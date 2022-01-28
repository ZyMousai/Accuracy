import { TrackAlliance } from '@/services/api'
import { request, METHOD } from '@/utils/request'

/**
 * 联盟列表页面
 * 获取联盟列表
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function TrackAllianceDate(query) {
    return request(TrackAlliance, METHOD.GET, query)
}
