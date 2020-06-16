<template>
  <div class="app-container">
    <el-row :gutter="20" type="flex">
      <el-col :span="6" :xs="24">
        <user-card />
      </el-col>
      <el-col :span="18" :xs="24">
        <el-card>
          <div slot="header" class="clearfix">
            <span>基本资料</span>
          </div>
          <el-tabs v-model="activeTab">
            <el-tab-pane label="基本资料" name="account">
              <account :user="user" />
            </el-tab-pane>
            <el-tab-pane label="修改密码" name="changepassword">
              <change-password />
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>

import UserCard from './components/UserCard'
import Account from './components/Account'
import ChangePassword from './components/ChangePassword'
import { getToken } from '@/utils/auth'
import { mapGetters } from 'vuex'

export default {
  name: 'Center',
  components: { UserCard, Account, ChangePassword },
  data() {
    return {
      headers: {
        'Authorization': 'Bearer ' + getToken()
      },
      user: {},
      activeTab: 'account'
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'avatar',
      'roles',
      'username',
      'mobile',
      'position',
      'date_joined',
      'is_active',
      'email'
    ])
  },
  created() {
    this.getUser()
  },
  methods: {
    getUser() {
      this.user = {
        name: this.name,
        role: this.roles.join(' | '),
        email: this.email,
        avatar: this.avatar,
        username: this.username,
        mobile: this.mobile,
        position: this.position,
        date_joined: this.date_joined,
        is_active: this.is_active
      }
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
</style>

