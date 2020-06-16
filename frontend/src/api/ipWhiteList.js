import request from '@/utils/request'

export function getIpWhiteList(listQuery) {
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
    url: `/api/IpWhiteList/?search=${listQuery.search}&name=${listQuery.name}&add_time_after=${after_date}&add_time_before=${before_date}&ordering=${listQuery.order}${listQuery.prop}&page=${listQuery.page}&page_size=${listQuery.pageSize}`,
    method: 'get'
  })
}

export function createIpWhite(data, method) {
  return request({
    url: `/api/IpWhiteList/`,
    method,
    data
  })
}

export function updateIpWhite(ID, data, method) {
  return request({
    url: `/api/IpWhiteList/${ID}/`,
    method,
    data
  })
}

export function deleteIpWhite(ID) {
  return request({
    url: `/api/IpWhiteList/${ID}/`,
    method: 'delete'
  })
}
