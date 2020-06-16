import { login, getInfo, updateInfo } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import router, { resetRouter } from '@/router'

const state = {
  token: getToken(),
  name: '',
  avatar: '',
  introduction: '',
  roles: [],
  date_joined: '',
  username: '',
  is_active: false,
  mobile: '',
  email: '',
  position: ''
}

const mutations = {
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_INTRODUCTION: (state, introduction) => {
    state.introduction = introduction
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_ROLES: (state, roles) => {
    state.roles = roles
  },
  SET_DATEJOINED: (state, date_joined) => {
    state.date_joined = date_joined
  },
  SET_USERNAME: (state, username) => {
    state.username = username
  },
  SET_ISACTIVE: (state, is_active) => {
    state.is_active = is_active
  },
  SET_MOBILE: (state, mobile) => {
    state.mobile = mobile
  },
  SET_EMAIL: (state, email) => {
    state.email = email
  },
  SET_POSITION: (state, position) => {
    state.position = position
  }
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password }).then(response => {
        const { token } = response.results
        commit('SET_TOKEN', token)
        commit('SET_NAME', username)
        setToken(token)
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // get user info
  getUserInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo(state.name).then(response => {
        if (!response) {
          reject('获取用户信息失败.')
        }

        const { roles, name, avatar, introduction, date_joined, username, email, is_active, mobile, position } = response

        // roles must be a non-empty array
        if (!roles || roles.length <= 0) {
          reject('账号无权限登录')
        }

        commit('SET_ROLES', roles)
        commit('SET_NAME', name)
        commit('SET_AVATAR', avatar)
        commit('SET_INTRODUCTION', introduction)
        commit('SET_DATEJOINED', date_joined)
        commit('SET_USERNAME', username)
        commit('SET_ISACTIVE', is_active)
        commit('SET_MOBILE', mobile)
        commit('SET_EMAIL', email)
        commit('SET_POSITION', position)
        resolve(response)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // 更新个人信息
  updateInfo({ commit, state }, userInfoForm) {
    return new Promise((resolve, reject) => {
      updateInfo(state.username, userInfoForm).then(response => {
        if (!response) {
          reject('更新用户信息失败.')
        }
        commit('SET_NAME', response.name)
        commit('SET_MOBILE', response.mobile)
        commit('SET_EMAIL', response.email)
        resolve(response)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  logout({ commit, state, dispatch }) {
    return new Promise((resolve, reject) => {
      try {
        commit('SET_TOKEN', '')
        commit('SET_ROLES', [])
        removeToken()
        resetRouter()
        // reset visited views and cached views
        // to fixed https://github.com/PanJiaChen/vue-element-admin/issues/2485
        dispatch('tagsView/delAllViews', null, { root: true })
        resolve()
      } catch (e) {
        reject(e)
      }
    })
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      commit('SET_TOKEN', '')
      commit('SET_ROLES', [])
      removeToken()
      resolve()
    })
  },

  // dynamically modify permissions
  changeRoles({ commit, dispatch }, role) {
    return new Promise(async resolve => {
      const token = role + '-token'

      commit('SET_TOKEN', token)
      setToken(token)

      const { roles } = await dispatch('getInfo')

      resetRouter()

      // generate accessible routes map based on roles
      const accessRoutes = await dispatch('permission/generateRoutes', roles, { root: true })

      // dynamically add accessible routes
      router.addRoutes(accessRoutes)

      // reset visited views and cached views
      dispatch('tagsView/delAllViews', null, { root: true })

      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
