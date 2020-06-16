import request from '@/utils/request'

export function getProjectAreaList(listQuery) {
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
    url: `/api/projectArea/?search=${listQuery.search}&name=${listQuery.name}&project=${listQuery.project}&area=${listQuery.area}&update_time_after=${after_date}&update_time_before=${before_date}&ordering=${listQuery.order}${listQuery.prop}&page=${listQuery.page}&page_size=${listQuery.pageSize}`,
    method: 'get'
  })
}

export function getProjectAreaList2(pageSize) {
  return request({
    url: `/api/projectArea/?page_size=${pageSize}`,
    method: 'get'
  })
}

export function createArea(data, method) {
  return request({
    url: `/api/projectArea/`,
    method,
    data
  })
}

export function updateArea(ID, data, method) {
  return request({
    url: `/api/projectArea/${ID}/`,
    method,
    data
  })
}

export function deleteArea(ID) {
  return request({
    url: `/api/projectArea/${ID}/`,
    method: 'delete'
  })
}
