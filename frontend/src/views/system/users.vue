<template>
  <div class="app-container">
    <div class="filter-container">
      <el-select v-model="listQuery.name" placeholder="用户名" clearable style="width: 100px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in list" :key="item.id" :label="item.name" :value="item.name" />
      </el-select>
      <el-date-picker
        v-model="listQuery.datetimeValue"
        type="datetimerange"
        value-format="yyyy-MM-dd HH:mm:ss"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        class="datetime"
        @change="handleFilter"
      />
      <el-input v-model="listQuery.search" placeholder="登录账号/用户名/手机" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">搜索</el-button>
    </div>
    <div class="add-container">
      <el-button class="filter-item" type="primary" icon="el-icon-edit" @click="handleCreate">添加</el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">导出</el-button>
    </div>
    <el-table
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="sortChange"
    >
      <el-table-column label="ID" prop="id" sortable="custom" align="center" width="70" />
      <el-table-column label="登录账号" prop="username" sortable="custom" min-width="90px" align="center" />
      <el-table-column label="用户名" prop="name" sortable="custom" min-width="80px" align="center" />
      <el-table-column label="邮箱" prop="email" sortable="custom" min-width="180px" align="center" />
      <el-table-column label="手机号" prop="mobile" sortable="custom" min-width="110px" align="center" />
      <el-table-column label="职位" prop="position" sortable="custom" min-width="80px" align="center" />
      <el-table-column label="角色" prop="roles2" align="center" min-width="95" />
      <el-table-column label="账号状态" prop="is_active" sortable="custom" class-name="status-col" min-width="100" align="center" :formatter="accountFormatter" />
      <el-table-column label="创建时间" prop="date_joined" sortable="custom" align="center" min-width="150" class-name="small-padding fixed-width" />
      <el-table-column label="操作" align="center" width="200" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">编辑</el-button>
          <el-button size="mini" type="danger" @click="handleDelete(row,$index)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog
      title="警告"
      :visible.sync="confirmDelete"
      width="30%"
    >
      <span>确定要删除账号<b>{{ deleteRowData.username }}</b>吗？</span>
      <span slot="footer" class="dialog-footer">
        <el-button size="mini" @click="resetDjalog">取 消</el-button>
        <el-button type="primary" size="mini" @click="confirmDjalog">确 定</el-button>
      </span>
    </el-dialog>
    <pagination
      v-show="total>10"
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.pageSize"
      @pagination="getList"
    />

    <el-dialog :title="dialogStatus" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="right" label-width="80px" style="width: 500px; margin-left:50px;">
        <el-form-item label="登录账号" prop="username">
          <el-input v-model.trim="temp.username" placeholder="登录账号" />
        </el-form-item>
        <el-form-item label="用户名" prop="name">
          <el-input v-model.trim="temp.name" placeholder="用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model.trim="temp.password" placeholder="密码" show-password />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model.trim="temp.email" placeholder="邮箱" />
        </el-form-item>
        <el-form-item label="手机号" prop="mobile">
          <el-input v-model.trim="temp.mobile" placeholder="手机号" />
        </el-form-item>
        <el-form-item label="职位" prop="position">
          <el-input v-model.trim="temp.position" placeholder="职位" />
        </el-form-item>
        <el-form-item label="用户组">
          <el-select v-model="temp.groups" class="filter-item" placeholder="用户组" multiple>
            <el-option v-for="item in groupsInfo" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="账号状态" prop="is_active">
          <el-switch v-model="temp.is_active" active-text="启用" inactive-text="禁用" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="restData()">取消</el-button>
        <el-button type="primary" @click="dialogStatus==='创建用户'?createData():updateData()">确认</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getUsers, getGroupsInfo, postUserInfo, patchUserInfo, deleteUserInfo } from '@/api/user'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination'

export default {
  name: 'Users',
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      list: [],
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        pageSize: 10,
        name: '',
        search: '',
        datetimeValue: [],
        order: '',
        prop: ''
      },
      groupsInfo: [],
      temp: {
        username: '',
        name: '',
        password: '',
        email: '',
        mobile: '',
        position: '',
        groups: [],
        is_active: true
      },
      dialogFormVisible: false,
      dialogStatus: '',
      dialogPvVisible: false,
      pvData: [],
      rules: {
        username: [{ required: true, message: '登录账号不能为空', trigger: 'blur' }, { min: 2, max: 20, message: '长度在 2 到 20个字符', trigger: 'blur' }],
        name: [{ required: true, message: '用户名不能为空', trigger: 'blur' }, { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }],
        password: [{ required: true, message: '密码不能为空', trigger: 'blur' }],
        email: [{ required: true, message: '邮箱不能为空', trigger: 'blur' }, { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }],
        mobile: [{ required: true, trigger: 'blur' }, { min: 11, max: 11, message: '长度为11个字符', trigger: 'blur' }, { pattern: /^1[3|4|5|6|7|8][0-9]{9}$/, message: '输入正确的手机号', trigger: 'blur' }],
        position: [{ required: true, message: '职位不能为空', trigger: 'blur' }, { trigger: 'blur' }]
      },
      downloadLoading: false,
      confirmDelete: false,
      deleteRowData: {}
    }
  },
  watch: {
    list() {
      this.list.forEach(user => {
        user.roles2 = user ? user.roles.join(', ') : ''
      })
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList(obj) {
      this.listLoading = true
      getUsers(this.listQuery).then(response => {
        this.list = response.results
        this.total = response.count
        this.listLoading = false
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    accountFormatter(row, column) {
      return row.is_active ? '正常' : '禁用'
    },
    sortChange(column) {
      this.listQuery.prop = column.prop
      if (column.order === 'descending') {
        this.listQuery.order = '-'
      } else {
        this.listQuery.order = ''
      }
      this.getList()
    },
    getGroups() {
      getGroupsInfo().then(response => {
        this.groupsInfo = response.results
      })
    },
    restTemp() {
      this.temp = {
        username: '',
        name: '',
        password: '',
        email: '',
        mobile: '',
        position: '',
        groups: [],
        is_active: true
      }
    },
    handleCreate() {
      this.dialogStatus = '创建用户'
      this.restTemp()
      this.getGroups()
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    handleUpdate(row) {
      // this.temp = row
      this.temp = Object.assign({}, row)
      this.listLoading = false
      this.dialogStatus = '编辑账号'
      this.getGroups()
      this.dialogFormVisible = true
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          postUserInfo(this.temp).then(response => {
            this.dialogFormVisible = false
            this.restTemp()
            this.getList()
            this.$message({
              title: 'Success',
              message: '创建成功',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    restData() {
      this.dialogFormVisible = false
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          const account = tempData.username
          patchUserInfo(account, tempData).then(() => {
            this.dialogFormVisible = false
            this.getList()
            this.$message({
              title: 'Success',
              message: `${account} 更新成功`,
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleDelete(row, index) {
      this.confirmDelete = true
      this.deleteRowData = row
    },
    resetDjalog() {
      this.confirmDelete = false
      this.$message({
        title: 'Success',
        message: '已取消',
        type: 'success',
        duration: 2000
      })
    },
    confirmDjalog() {
      const account = this.deleteRowData.username
      deleteUserInfo(account).then(() => {
        this.confirmDelete = false
        this.getList()
        this.$message({
          title: 'Success',
          message: `账号 ${account} 删除成功`,
          type: 'success',
          duration: 2000
        })
      })
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['id', '账号', '用户名', '邮箱', '手机号', '职位', '创建时间']
        const filterVal = ['id', 'username', 'name', 'email', 'mobile', 'position', 'date_joined']
        const data = this.formatJson(filterVal)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'table-list'
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal) {
      return this.list.map(v => filterVal.map(j => {
        if (j === 'date_joined') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    }
  }
}
</script>

<style lang="scss" scoped>
  .datetime {
    position: relative;
    bottom: 4px;
  }
</style>
