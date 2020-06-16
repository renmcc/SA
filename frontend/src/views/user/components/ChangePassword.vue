<template>
  <el-form ref="changePasswordForm" :model="changePasswordForm" :rules="rules">
    <el-form-item label="旧密码" :label-width="labelWidth" label-position="left" prop="old_password">
      <el-input v-model.trim="changePasswordForm.old_password" placeholder="旧密码" show-password />
    </el-form-item>
    <el-form-item label="新密码" :label-width="labelWidth" label-position="left" prop="new_password1">
      <el-input v-model.trim="changePasswordForm.new_password1" placeholder="新密码" show-password />
    </el-form-item>
    <el-form-item label="确认密码" :label-width="labelWidth" label-position="left" prop="new_password2">
      <el-input v-model.trim="changePasswordForm.new_password2" placeholder="确认密码" show-password />
    </el-form-item>
    <el-form-item :label-width="labelWidth" label-position="left">
      <el-button @click="resetForm('changePasswordForm')">重置</el-button>
      <el-button :loading="loading" type="primary" @click="submit">更新</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import { changePassword } from '@/api/user'

export default {
  name: 'ChangePassword',
  data() {
    const confirmPass = (rule, value, callback) => {
      if (this.changePasswordForm.new_password1 !== value) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }
    return {
      changePasswordForm: {},
      labelWidth: '100px',
      loading: false,
      rules: {
        old_password: [
          { required: true, message: '密码不能为空', trigger: 'blur' }
        ],
        new_password1: [
          { required: true, message: '密码不能为空', trigger: 'blur' },
          { min: 1, max: 20, message: '1-20个字符', trigger: 'blur' }
        ],
        new_password2: [
          { required: true, validator: confirmPass, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submit() {
      this.$refs.changePasswordForm.validate(valid => {
        if (valid) {
          this.loading = true
          changePassword(this.changePasswordForm).then(response => {
            this.loading = false
            this.$message({
              message: '更新成功',
              type: 'success',
              duration: 5 * 1000
            })
          }).catch(() => {
            this.loading = false
            this.$message({
              message: '更新失败',
              type: 'error',
              duration: 5 * 1000
            })
          })
        } else {
          return false
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    }
  }
}
</script>
