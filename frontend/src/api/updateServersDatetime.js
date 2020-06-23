import request from '@/utils/request'

export function getUpdateServersDatetime(listQuery, currentUser) {
  return request({
    url: `/api/updateSystemDate/?search=${listQuery.search}&user=${currentUser}&ordering=${listQuery.order}&page=${listQuery.page}&page_size=${listQuery.pageSize}`,
    method: 'get'
  })
}

export function getProjectRoleInfo(pageSize) {
  return request({
    url: `/api/updateSystemDate/?page_size=${pageSize}`,
    method: 'get'
  })
}

export function createUpdateServersDatetime(data, method) {
  return request({
    url: `/api/updateSystemDate/`,
    method,
    data
  })
}
