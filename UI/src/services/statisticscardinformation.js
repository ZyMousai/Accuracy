import { GetCreditCardListData, GetTaskListData, CardAccount, CommissionConsume, CardsExcel, addcards, GetAccountTaskName, CardsExcelExport } from '@/services/api'
import { request, METHOD } from '@/utils/request'

/**
 * 统计卡页面
 * 获取统计卡 父表格数据
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function CreditCardListData(query) {
    return request(GetCreditCardListData, METHOD.GET, query)
}

/**
 * 统计卡页面
 * 修改统计卡 父表格数据
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function PatchCardListData(query) {
    return request(GetCreditCardListData, "PATCH", query)
}

/**
 * 统计卡页面
 * 获取统计卡 子表格数据
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function CreditTaskListData(query) {
    return request(GetTaskListData, METHOD.GET, query)
}

/**
 * 统计卡页面
 * 获取uuid对应的任务名
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function GetAccountTaskNameData(query) {
    return request(GetAccountTaskName, METHOD.GET, query)
}

/**
 * 统计卡页面
 * 新增统计卡 子表格数据
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function AddCreditTask(query) {
    return request(GetTaskListData, METHOD.POST, query)
}
/**
 * 统计卡页面
 * 新增卡号
 * @param form  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function AddOneCard(form) {
    return request(addcards, METHOD.POST, form)
}

/**
 * 统计卡页面
 * 修改统计卡 子表格数据
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function PatchTaskListData(query) {
    return request(GetTaskListData, "PATCH", query)
}

/**
 * 统计卡页面
 * 删除卡号数据
 * @param id  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function table_delete(id) {
    return request(GetCreditCardListData, "DELETE", {
        ids: id
    })
}

/**
 * 统计卡页面
 * 删除任务数据
 * @param id  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function innerdelete(id) {
    return request(GetTaskListData, "DELETE", {
        ids: id
    })
}

/**
 * 统计卡页面
 * 获取账号列表
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function CardAccountListData(query) {
    return request(CardAccount, METHOD.GET, query)
}


/**
 * 统计卡页面
 * 添加账号列表
 * @param form  添加请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function AddCardAccount(form) {
    return request(CardAccount, METHOD.POST, form)
}

/**
 * 统计卡页面
 * 删除账号列表
 * @param id  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function CardAccountdelete(id) {
    return request(CardAccount, "DELETE", {
        ids: id
    })
}


/**
 * 统计卡页面
 * 根据uid来计算收益和消耗
 * @param query  查询请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function CommissionConsumetion(query) {
    return request(CommissionConsume, METHOD.GET, query)
}

/**
 * 统计卡页面
 * 上传文件
 * @param query  查询请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function AddCardsExcel(query) {
    return request(CardsExcel, METHOD.POST, query)
}

/**
 * 统计卡页面
 * 导出数据成excel
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function ExcelExport(query) {
    return request(CardsExcelExport, METHOD.POST, query, {responseType: 'arraybuffer'})
}
