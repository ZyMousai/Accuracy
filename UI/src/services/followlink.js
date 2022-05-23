import { GetFollowLinkDate } from '@/services/api'
import { request, METHOD } from '@/utils/request'

/**
 * 跟踪链接页面
 * 获取跟踪链接表格数据
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function FollowLinkDate(query) {
    return request(GetFollowLinkDate, METHOD.GET, query)
}