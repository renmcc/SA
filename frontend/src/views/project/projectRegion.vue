<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.search" placeholder="地区名称" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
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
      <el-table-column label="ID" prop="id" sortable="custom" align="center" width="70" class-name="small-padding fixed-width" />
      <el-table-column label="地区名称" prop="name" sortable="custom" align="center" min-width="120px" class-name="small-padding fixed-width" />
      <el-table-column label="描述" prop="remark" sortable="custom" align="center" min-width="80px" class-name="small-padding fixed-width" />
      <el-table-column label="添加时间" prop="created" sortable="custom" align="center" min-width="150px" class-name="small-padding fixed-width" />
      <el-table-column label="更新时间" prop="update_time" sortable="custom" align="center" min-width="150" class-name="small-padding fixed-width" />
      <el-table-column label="操作" align="center" width="200" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">编辑</el-button>
          <el-button size="mini" type="danger" @click="handleDelete(row,$index)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination
      v-show="total>10"
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.pageSize"
      @pagination="getList"
    />
    <el-dialog
      title="警告"
      :visible.sync="confirmDelete"
      width="30%"
    >
      <span>确定要删除地区<b>{{ deleteRowData.name }}</b>吗？</span>
      <span slot="footer" class="dialog-footer">
        <el-button size="mini" @click="resetDjalog">取 消</el-button>
        <el-button type="primary" size="mini" @click="confirmDjalog">确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog :title="dialogStatus" :visible.sync="dialogFormVisible" width="40%">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="right" label-width="90px" class="transfer-class">
        <el-form-item label="地区名称" prop="name">
          <el-input v-model.trim="temp.name" style="width: 70%" placeholder="地区名称" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model.trim="temp.remark" type="textarea" :rows="4" style="width: 70%" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="restData">取消</el-button>
        <el-button type="primary" @click="dialogStatus==='添加项目'?createData():updateData()">确认</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getProjectRegion, createProjectRegion, updateProjectRegion, deleteProjectRegion } from '@/api/projectRegion'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination'

export default {
  name: 'ProjectRegion',
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      list: [],
      total: 0,
      regionFilterList: [],
      projectFilterList: [],
      areaFilterList: [],
      listLoading: true,
      listQuery: {
        page: 1,
        pageSize: 10,
        region: '',
        project: '',
        area: '',
        name: '',
        search: '',
        datetimeValue: [],
        order: '',
        prop: ''
      },
      groupsPermissions: [],
      temp: {
        name: '',
        remark: null
      },
      dialogFormVisible: false,
      dialogStatus: '',
      dialogPvVisible: false,
      pvData: [],
      rules: {
        name: [{ required: true, message: '地区名称不能为空', trigger: 'blur' }]
      },
      downloadLoading: false,
      confirmDelete: false,
      deleteRowData: {},
      projectArea: [],
      ProjectInfo: [],
      ProjectRegionInfo: [],
      ProjectRoleInfo: []
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList(obj) {
      this.listLoading = true
      getProjectRegion(this.listQuery).then(response => {
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
        name: '',
        remark: null
      }
    },
    restData() {
      this.dialogFormVisible = false
    },
    handleCreate() {
      this.dialogStatus = '添加项目'
      this.restTemp()
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.listLoading = false
      this.dialogStatus = '编辑项目'
      this.dialogFormVisible = true
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          createProjectRegion(this.temp, 'post').then(response => {
            this.restTemp()
            this.restData()
            this.getList()
            this.$message({
              title: 'Success',
              message: `地区 ${this.temp.name} 添加成功`,
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
          updateProjectRegion(ID, tempData, 'patch').then(() => {
            this.restData()
            this.getList()
            this.$message({
              title: 'Success',
              message: `地区 ${tempData.name} 更新成功`,
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
      deleteProjectRegion(ID).then(() => {
        this.confirmDelete = false
        this.getList()
        this.$message({
          title: 'Success',
          message: `地区 ${this.deleteRowData.name} 删除成功`,
          type: 'success',
          duration: 2000
        })
      })
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['id', '项目', '地区', '大区', '角色', '主机名', '公网ip', '内网ip', '操作系统', 'CPU', '内存', '硬盘', '状态', '描述', '添加时间', '更新时间']
        const filterVal = ['id', 'projectInfo', 'regionInfo', 'areaInfo', 'roleInfo', 'hostname', 'public_ip', 'private_ip', 'os', 'cpu', 'memory', 'disk', 'status', 'remark', 'add_time', 'update_time']
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
        } else if (j === 'projectInfo') {
          return v.projectInfo.name
        } else if (j === 'regionInfo') {
          return v.regionInfo.name
        } else if (j === 'areaInfo') {
          return v.areaInfo.name
        } else if (j === 'roleInfo') {
          return v.roleInfo.join(',')
        } else {
          return v[j]
        }
      }))
    },
    permissionFilterMethod(query, item) {
      return item.label.indexOf(query) > -1
    },
    accountFormatter(row, column) {
      return row.status ? '启用' : '禁用'
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
