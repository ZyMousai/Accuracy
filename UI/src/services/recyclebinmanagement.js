import { RecycleShow, RecycleClear, RecycleRecover } from '@/services/api'
import { request, METHOD } from '@/utils/request'

/**
 * 回收站页面
 * 获取回收站表格数据
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function RecycleDocumentDate(query) {
    return request(RecycleShow, METHOD.GET, query)
}

/**
 * 彻底清除文档
 * @param id  查新请求参数
 * @param is_logic_del  是否是逻辑删除
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function RecycleDeleteDocuments(id, is_logic_del) {
    return request(RecycleClear, "DELETE", {
        ids: id,
        is_logic_del: is_logic_del
    })
}

/**
 * 恢复文档
 * @param id  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function RecycleRecoverManagement(id) {
    return request(RecycleRecover, METHOD.GET, {
        file_id: id,
    })
}