import request from '@/utils/request'

export function getProject(listQuery) {
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
    url: `/api/project/?search=${listQuery.search}&name=${listQuery.name}&project=${listQuery.project}&area=${listQuery.area}&update_time_after=${after_date}&update_time_before=${before_date}&ordering=${listQuery.order}${listQuery.prop}&page=${listQuery.page}&page_size=${listQuery.pageSize}`,
    method: 'get'
  })
}

export function getProjectInfo(pageSize) {
  return request({
    url: `/api/project/?page_size=${pageSize}`,
    method: 'get'
  })
}

export function createProject(data, method) {
  return request({
    url: `/api/project/`,
    method,
    data
  })
}

export function updateProject(ID, data, method) {
  return request({
    url: `/api/project/${ID}/`,
    method,
    data
  })
}

export function deleteProject(ID) {
  return request({
    url: `/api/project/${ID}/`,
    method: 'delete'
  })
}
