<template>
  <div class="app-container">
    <div class="filter-container">
      <el-select v-model="listQuery.project" placeholder="项目" clearable style="width: 100px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in projectFilterList" :key="item.id" :label="item.name" :value="item.id" />
      </el-select>
      <el-select v-model="listQuery.region" placeholder="地区" clearable style="width: 100px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in regionFilterList" :key="item.id" :label="item.name" :value="item.id" />
      </el-select>
      <el-select v-model="listQuery.area" placeholder="大区" clearable style="width: 100px" class="filter-item" @change="handleFilter">
        <el-option v-for="item in areaFilterList" :key="item.id" :label="item.name" :value="item.id" />
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
      <el-input v-model="listQuery.search" placeholder="公网ip/内网ip" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
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
      <el-table-column label="项目" prop="projectInfo.name" sortable align="center" min-width="80px" class-name="small-padding fixed-width" />
      <el-table-column label="地区" prop="regionInfo.name" sortable min-width="100px" align="center" class-name="small-padding fixed-width" />
      <el-table-column label="大区" prop="areaInfo.name" sortable align="center" min-width="80px" class-name="small-padding fixed-width" />
      <el-table-column label="角色" prop="roles" sortable align="center" min-width="270px" class-name="small-padding fixed-width" />
      <el-table-column label="主机名" prop="hostname" sortable="custom" align="center" min-width="100px" class-name="small-padding fixed-width" />
      <el-table-column label="公网IP" prop="public_ip" sortable="custom" align="center" min-width="120px" class-name="small-padding fixed-width" />
      <el-table-column label="内网IP" prop="private_ip" sortable="custom" align="center" min-width="120px" class-name="small-padding fixed-width" />
      <el-table-column label="操作系统" prop="os" sortable="custom" align="center" min-width="100px" class-name="small-padding fixed-width" />
      <el-table-column label="CPU" prop="cpu" sortable="custom" align="center" min-width="300px" class-name="small-padding fixed-width" />
      <el-table-column label="内存" prop="memory" sortable="custom" align="center" min-width="80px" class-name="small-padding fixed-width" />
      <el-table-column label="硬盘" prop="disk" sortable="custom" align="center" min-width="80px" class-name="small-padding fixed-width" />
      <el-table-column label="状态" prop="status" sortable="custom" align="center" min-width="80px" class-name="small-padding fixed-width" :formatter="accountFormatter" />
      <el-table-column label="描述" prop="remark" sortable="custom" align="center" min-width="80px" class-name="small-padding fixed-width" />
      <el-table-column label="添加时间" prop="add_time" sortable="custom" align="center" min-width="150px" class-name="small-padding fixed-width" />
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
      <span>确定要删除服务器<b>{{ deleteRowData.private_ip }}</b>吗？</span>
      <span slot="footer" class="dialog-footer">
        <el-button size="mini" @click="resetDjalog">取 消</el-button>
        <el-button type="primary" size="mini" @click="confirmDjalog">确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog :title="dialogStatus" :visible.sync="dialogFormVisible" width="40%">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="right" label-width="70px" class="transfer-class">
        <el-form-item label="项目">
          <el-select v-model="temp.project" class="filter-item" placeholder="项目">
            <el-option v-for="item in ProjectInfo" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="地区">
          <el-select v-model="temp.region" class="filter-item" placeholder="项目所属地区">
            <el-option v-for="item in ProjectRegionInfo" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="大区">
          <el-select v-model="temp.area" class="filter-item" placeholder="项目所属大区">
            <el-option v-for="item in projectArea" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="temp.role" class="filter-item" placeholder="服务器所属角色" multiple style="width: 70%">
            <el-option v-for="item in ProjectRoleInfo" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="公网ip">
          <el-input v-model.trim="temp.public_ip" style="width: 70%" placeholder="公网ip" />
        </el-form-item>
        <el-form-item label="内网ip" prop="private_ip">
          <el-input v-model.trim="temp.private_ip" style="width: 70%" placeholder="内网ip" />
        </el-form-item>
        <el-form-item label="账号状态">
          <el-switch v-model="temp.status" active-text="启用" inactive-text="禁用" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model.trim="temp.remark" type="textarea" :rows="4" style="width: 70%" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="restData">取消</el-button>
        <el-button type="primary" @click="dialogStatus==='添加服务器'?createData():updateData()">确认</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getServersList, createServers, updateServer, deleteServer } from '@/api/serversList'
import { getProjectAreaList2 } from '@/api/projectArea'
import { getProjectInfo } from '@/api/project'
import { getProjectRegionInfo } from '@/api/projectRegion'
import { getProjectRoleInfo } from '@/api/projectRole'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination'

export default {
  name: 'ServersList',
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
        status: true,
        project: '',
        area: '',
        region: '',
        public_ip: null,
        private_ip: null,
        os: '',
        cpu: '',
        memory: '',
        disk: '',
        remark: '',
        projectInfo: {}
      },
      dialogFormVisible: false,
      dialogStatus: '',
      dialogPvVisible: false,
      pvData: [],
      rules: {
        private_ip: [{ required: true, message: '请输入IP', trigger: 'blur' }]
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
  watch: {
    list() {
      this.list.forEach(server => {
        server.roles = server ? server.roleInfo.join(', ') : ''
      })
      const regionMap = new Map()
      const projectMap = new Map()
      const areaMap = new Map()
      for (const item of this.list) {
        if (!regionMap.has(item.regionInfo.id)) {
          regionMap.set(item.regionInfo.id, item.regionInfo)
        }
        if (!projectMap.has(item.projectInfo.id)) {
          projectMap.set(item.projectInfo.id, item.projectInfo)
        }
        if (!areaMap.has(item.areaInfo.id)) {
          areaMap.set(item.areaInfo.id, item.areaInfo)
        }
      }
      this.regionFilterList = [...regionMap.values()]
      this.projectFilterList = [...projectMap.values()]
      this.areaFilterList = [...areaMap.values()]
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList(obj) {
      this.listLoading = true
      getServersList(this.listQuery).then(response => {
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
        status: true,
        project: '',
        area: '',
        region: '',
        public_ip: null,
        private_ip: null,
        os: '',
        cpu: '',
        memory: '',
        disk: '',
        remark: ''
      }
    },
    restData() {
      this.dialogFormVisible = false
    },
    getProjectArea() {
      const pageSize = 1000
      getProjectAreaList2(pageSize).then(response => {
        this.projectArea = response.results
      })
    },
    getProject() {
      const pageSize = 1000
      getProjectInfo(pageSize).then(response => {
        this.ProjectInfo = response.results
      })
    },
    getProjectRegionInfo() {
      const pageSize = 1000
      getProjectRegionInfo(pageSize).then(response => {
        this.ProjectRegionInfo = response.results
      })
    },
    getProjectRoleInfo() {
      const pageSize = 1000
      getProjectRoleInfo(pageSize).then(response => {
        this.ProjectRoleInfo = response.results
      })
    },
    handleCreate() {
      this.dialogStatus = '添加服务器'
      this.restTemp()
      this.getProjectArea()
      this.getProject()
      this.getProjectRegionInfo()
      this.getProjectRoleInfo()
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row)
      this.getProjectArea()
      this.getProject()
      this.getProjectRegionInfo()
      this.getProjectRoleInfo()
      this.listLoading = false
      this.dialogStatus = '编辑服务器'
      this.dialogFormVisible = true
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          createServers(this.temp, 'post').then(response => {
            this.restTemp()
            this.restData()
            this.getList()
            this.$message({
              title: 'Success',
              message: `服务器 ${this.temp.private_ip} 添加成功`,
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
          updateServer(ID, tempData, 'patch').then(() => {
            this.restData()
            this.getList()
            this.$message({
              title: 'Success',
              message: `服务器 ${tempData.private_ip} 更新成功`,
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
      deleteServer(ID).then(() => {
        this.confirmDelete = false
        this.getList()
        this.$message({
          title: 'Success',
          message: `账号 ${this.deleteRowData.private_ip} 删除成功`,
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
