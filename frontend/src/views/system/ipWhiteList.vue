<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.search" placeholder="IP地址" style="width: 300px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">搜索</el-button>
    </div>
    <div class="add-container">
      <el-button class="filter-item" type="primary" icon="el-icon-edit" @click="handleCreate">添加</el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">导出</el-button>
    </div>
    <el-dialog :title="dialogStatus" :visible.sync="dialogFormVisible" width="40%">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="right" label-width="70px" class="transfer-class">
        <el-form-item label="IP地址" prop="ip_addr">
          <el-input v-model.trim="temp.ip_addr" style="width: 300px" placeholder="IP地址" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="restData">取消</el-button>
        <el-button type="primary" @click="dialogStatus==='添加白名单'?createData():updateData()">确认</el-button>
      </div>
    </el-dialog>
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
      <el-table-column label="IP地址" prop="ip_addr" sortable="custom" min-width="90px" align="center" />
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
      <span>确定要删除IP地址<b>{{ deleteRowData.ip_addr }}</b>吗？</span>
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
  </div>
</template>

<script>
import { getIpWhiteList, createIpWhite, updateIpWhite, deleteIpWhite } from '@/api/ipWhiteList'
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
        ip_addr: '',
        search: '',
        datetimeValue: [],
        order: '',
        prop: ''
      },
      groupsPermissions: [],
      temp: {
        ip_addr: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      dialogPvVisible: false,
      pvData: [],
      rules: {
        ip_addr: [{ required: true, message: '请输入IP地址', trigger: 'blur' }]
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
      getIpWhiteList(this.listQuery).then(response => {
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
    restTemp() {
      this.temp = {
        ip_addr: ''
      }
    },
    restData() {
      this.dialogFormVisible = false
    },
    handleCreate() {
      this.dialogStatus = '添加白名单'
      this.restTemp()
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.listLoading = false
      this.dialogStatus = '编辑白名单'
      this.dialogFormVisible = true
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          createIpWhite(this.temp, 'post').then(response => {
            this.restTemp()
            this.restData()
            this.getList()
            this.$message({
              title: 'Success',
              message: `白名单IP ${this.temp.ip_addr} 添加成功`,
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
          const ID = tempData.id
          updateIpWhite(ID, tempData, 'patch').then(() => {
            this.restData()
            this.getList()
            this.$message({
              title: 'Success',
              message: `${ID} 更新成功`,
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
      const ID = this.deleteRowData.id
      deleteIpWhite(ID).then(() => {
        this.confirmDelete = false
        this.getList()
        this.$message({
          title: 'Success',
          message: `账号 ${this.deleteRowData.ip_addr} 删除成功`,
          type: 'success',
          duration: 2000
        })
      })
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['id', 'IP地址', '创建时间', '更新时间']
        const filterVal = ['id', 'ip_addr', 'add_time', 'update_time']
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
