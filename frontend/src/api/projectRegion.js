import request from '@/utils/request'

export function getProjectRegion(listQuery) {
  let after_date = ''
  let before_date = ''
  if (listQuery.datetimeValue == null) {
    listQuery.datetimeValue = []
  }
  if (listQuery.datetimeValue.length > 0) {
    after_date = listQuery.datetimeValue[0]
    before_date = listQuery.datetimeValue[1]
  }
  return request({
    url: `/api/projectRegion/?search=${listQuery.search}&name=${listQuery.name}&project=${listQuery.project}&area=${listQuery.area}&update_time_after=${after_date}&update_time_before=${before_date}&ordering=${listQuery.order}${listQuery.prop}&page=${listQuery.page}&page_size=${listQuery.pageSize}`,
    method: 'get'
  })
}

export function getProjectRegionInfo(pageSize) {
  return request({
    url: `/api/projectRegion/?page_size=${pageSize}`,
    method: 'get'
  })
}

export function createProjectRegion(data, method) {
  return request({
    url: `/api/projectRegion/`,
    method,
    data
  })
}

export function updateProjectRegion(ID, data, method) {
  return request({
    url: `/api/projectRegion/${ID}/`,
    method,
    data
  })
}

export function deleteProjectRegion(ID) {
  return request({
    url: `/api/projectRegion/${ID}/`,
    method: 'delete'
  })
}
