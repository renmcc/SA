<template>
  <div class="app-container">
    <div class="filter-container">
      <el-select v-model="listQuery.name" placeholder="组名" clearable style="width: 100px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in list" :key="item.id" :label="item.name" :value="item.name" />
      </el-select>
      <el-date-picker
        v-model="listQuery.datetimeValue"
        type="datetimerange"
        value-format="yyyy-MM-dd HH:mm:ss"
        range-separator="-"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        class="datetime"
        @change="handleFilter"
      />
      <el-input v-model="listQuery.search" placeholder="用户组名称" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
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
      <el-table-column label="用户组" prop="name" sortable="custom" min-width="90px" align="center" />
      <el-table-column label="创建时间" prop="add_time" sortable="custom" align="center" min-width="150" class-name="small-padding fixed-width" />
      <el-table-column label="更新时间" prop="update_time" sortable="custom" align="center" min-width="150" class-name="small-padding fixed-width" />
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
      <span>确定要删除用户组<b>{{ deleteRowData.name }}</b>吗？</span>
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

    <el-dialog :title="dialogStatus" :visible.sync="dialogFormVisible" width="70%">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="right" label-width="70px" class="transfer-class">
        <el-form-item label="用户组" prop="name">
          <el-input v-model.trim="temp.name" style="width: 600px" placeholder="用户组" />
        </el-form-item>
        <el-form-item label="权限">
          <el-transfer
            v-model="temp.permissions"
            filterable
            :filter-method="permissionFilterMethod"
            filter-placeholder="输入权限"
            :titles="['可用 权限', '选中的 权限 ']"
            :props="{
              key: 'id',
              label: 'label'
            }"
            :data="groupsPermissions"
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="restData">取消</el-button>
        <el-button type="primary" @click="dialogStatus==='创建用户组'?createData():updateData()">确认</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getGroups2, getPermissionsInfo, Groups, Group, deleteGroup } from '@/api/user'
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
      groupsPermissions: [],
      temp: {
        name: '',
        permissions: []
      },
      dialogFormVisible: false,
      dialogStatus: '',
      dialogPvVisible: false,
      pvData: [],
      rules: {
        name: [{ required: true, message: '用户组不能为空', trigger: 'blur' }, { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }]
      },
      downloadLoading: false,
      confirmDelete: false,
      deleteRowData: {}
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList(obj) {
      this.listLoading = true
      getGroups2(this.listQuery).then(response => {
        this.list = response.results
        this.total = response.count
        this.listLoading = false
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
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
    permissionsInfo() {
      getPermissionsInfo().then(response => {
        this.groupsPermissions = response
      })
    },
    restTemp() {
      this.temp = {
        name: '',
        permissions: []
      }
    },
    restData() {
      this.dialogFormVisible = false
    },
    handleCreate() {
      this.dialogStatus = '创建用户组'
      this.restTemp()
      this.permissionsInfo()
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.listLoading = false
      this.dialogStatus = '编辑用户组'
      this.permissionsInfo()
      this.dialogFormVisible = true
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          Groups(this.temp, 'post').then(response => {
            this.restTemp()
            this.restData()
            this.getList()
            this.$message({
              title: 'Success',
              message: `用户组 ${this.temp.name} 创建成功`,
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          const account = tempData.name
          Group(account, tempData, 'patch').then(() => {
            this.restData()
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
      const account = this.deleteRowData.name
      deleteGroup(account).then(() => {
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
        const tHeader = ['id', '用户组', '创建时间', '更新时间']
        const filterVal = ['id', 'name', 'add_time', 'update_time']
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
        if (j === 'add_time') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    },
    permissionFilterMethod(query, item) {
      return item.label.indexOf(query) > -1
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
