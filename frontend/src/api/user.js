import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/api/userAuth/',
    method: 'post',
    data
  })
}

export function getInfo(name) {
  return request({
    url: `/api/userInfo/${name}/`,
    method: 'get'
  })
}

export function getUsers(listQuery) {
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
    url: `/api/userInfo/?search=${listQuery.search}&name=${listQuery.name}&date_joined_after=${after_date}&date_joined_before=${before_date}&ordering=${listQuery.order}${listQuery.prop}&page=${listQuery.page}&page_size=${listQuery.pageSize}`,
    method: 'get'
  })
}

export function updateInfo(name, data) {
  return request({
    url: `/api/userInfo/${name}/`,
    method: 'patch',
    data
  })
}

export function changePassword(data) {
  return request({
    url: `/api/changePassword/`,
    method: 'post',
    data
  })
}

export function getGroupsInfo(name, data) {
  return request({
    url: `/api/groupsInfo/`,
    method: 'get'
  })
}

export function Groups(data, method) {
  return request({
    url: `/api/groupsInfo/`,
    method,
    data
  })
}
export function Group(name, data, method) {
  return request({
    url: `/api/groupsInfo/${name}/`,
    method,
    data
  })
}

export function deleteGroup(name) {
  return request({
    url: `/api/groupsInfo/${name}/`,
    method: 'delete'
  })
}

export function postUserInfo(data) {
  return request({
    url: `/api/userInfo/`,
    method: 'post',
    data
  })
}

export function patchUserInfo(account, data) {
  return request({
    url: `/api/userInfo/${account}/`,
    method: 'patch',
    data
  })
}

export function deleteUserInfo(account) {
  return request({
    url: `/api/userInfo/${account}/`,
    method: 'delete'
  })
}

export function getGroups2(listQuery) {
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
    url: `/api/groupsInfo/?search=${listQuery.search}&name=${listQuery.name}&add_time_after=${after_date}&add_time_before=${before_date}&ordering=${listQuery.order}${listQuery.prop}&page=${listQuery.page}&page_size=${listQuery.pageSize}`,
    method: 'get'
  })
}

export function getPermissionsInfo() {
  return request({
    url: `/api/permissionsInfo/?ordering=id`,
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/vue-element-admin/user/logout',
    method: 'post'
  })
}
