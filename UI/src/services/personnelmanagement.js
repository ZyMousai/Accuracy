import { USERS, ROLES, DEPARTMENTS, UpdatePassword, DepartmentRoleMapping, DepartmentUserMapping, RoleMenu, RolePermission, RoleUser } from '@/services/api'
import { request, METHOD } from '@/utils/request'

/**
 * 用户页面
 * 查询用户
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function UsersDate(query) {
    return request(USERS, METHOD.GET, query)
}

/**
 * 用户页面
 * 查询单个用户
 * @param id  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function GetOneUsersDate(id) {
    return request(USERS + id, METHOD.GET, '')
}

/**
 * 用户页面
 * 增加用户
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function UsersAdd(query) {
    return request(USERS, METHOD.POST, query)
}

/**
 * 用户页面
 * 增加用户角色
 * @param form  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function UsersAddRole(form) {
    return request(RoleUser, METHOD.POST, form)
}

/**
 * 用户页面
 * 增加用户部门
 * @param form  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function UsersAddDepartment(form) {
    return request(DepartmentRoleMapping, METHOD.POST, form)
}

/**
 * 用户页面
 * 修改用户
 * @param form  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function UsersEdit(form) {
    return request(USERS, 'PATCH', form)
}

/**
 * 删除用户
 * @param id  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function DeleteUsers(id) {
    return request(USERS, "DELETE", {
        ids: id,
    })
}

/**
 * 角色管理页面
 * 获取角色列表
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function RolesDate(query) {
    return request(ROLES, METHOD.GET, query)
}

/**
 * 角色页面
 * 增加角色
 * @param from  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function AddRole(from) {
    return request(ROLES, METHOD.POST, from)
}

/**
 * 角色页面
 * 添加角色菜单
 * @param from  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function AddRoleMenu(from) {
    return request(RoleMenu, METHOD.POST, from)
}

/**
 * 角色页面
 * 添加角色权限
 * @param from  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function AddRolePermission(from) {
    return request(RolePermission, METHOD.POST, from)
}

/**
 * 角色添加修改页面
 * 获取角色对应的菜单
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function GetRoleMenu() {
    return request(RoleMenu, METHOD.GET, '')
}

/**
 * 删除角色
 * @param id  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function DeleteRoles(id) {
    return request(ROLES, "DELETE", {
        ids: id,
    })
}

/**
 * 角色管理页面
 * 重置密码
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function RolesResetPassword(query) {
    return request(UpdatePassword, "PATCH", query)
}

/**
 * 部门页面
 * 获取部门列表
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function DepartmentDate(query) {
    return request(DEPARTMENTS, METHOD.GET, query)
}

/**
 * 部门页面
 * 获取某个部门
 * @param id  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function GetOneDepartmentDate(id) {
    return request(DEPARTMENTS + '/' + id, METHOD.GET, '')
}

/**
 * 部门页面
 * 添加部门
 * @param form  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function AddDepartment(form) {
    return request(DEPARTMENTS, METHOD.POST, form)
}

/**
 * 部门页面
 * 修改部门
 * @param form  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function EditDepartment(form) {
    return request(DEPARTMENTS, "PATCH", form)
}
/**
 * 部门页面
 * 删除部门
 * @param id  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function DeleteDepartment(id) {
    return request(DEPARTMENTS, METHOD.DELETE, {
        ids: id
    })
}

/**
 * 部门编辑页面
 * 获取角色列表
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function GetDepartmentRole(query) {
    return request(DepartmentRoleMapping, METHOD.GET, query)
}

/**
 * 部门编辑页面
 * 添加部门角色
 * @param form  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function AddDepartmentRole(form) {
    return request(DepartmentRoleMapping, METHOD.POST, form)
}

/**
 * 部门编辑页面
 * 删除部门角色
 * @param data  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function DeleteDepartmentRole(data) {
    return request(DepartmentRoleMapping, "DELETE1", data)
}

/**
 * 部门编辑页面
 * 获取用户列表
 * @param query  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function GetDepartmentUser(query) {
    return request(DepartmentUserMapping, METHOD.GET, query)
}

/**
 * 部门编辑页面
 * 添加部门用户
 * @param form  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function AddDepartmentUser(form) {
    return request(DepartmentUserMapping, METHOD.POST, form)
}

/**
 * 部门编辑页面
 * 删除部门用户
 * @param data  查新请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
export async function DeleteDepartmentUser(data) {
    return request(DepartmentUserMapping, "DELETE1", data)
}