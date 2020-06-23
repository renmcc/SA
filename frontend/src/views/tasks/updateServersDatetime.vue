<template>
  <div>
    <div
      class="app-container"
    >
      <aside>
        此任务用于修改测试服服务器系统时间，方便运用、测试，进行游戏功能调试。
      </aside>
      <el-tabs v-model="activeTab" @tab-click="handleClick">
        <el-tab-pane label="提交任务" name="taskForms">
          <el-form ref="listQuery" :model="listQuery" :rules="rules" label-width="80px" label-position="right">
            <el-form-item label="项目" prop="project">
              <el-radio v-for="item in ProjectInfo" :key="item.id" v-model="listQuery.project" :label="item.id">{{ item.name }}</el-radio>
            </el-form-item>
            <el-form-item label="地区" prop="region">
              <el-radio v-for="item in ProjectRegionInfo" :key="item.id" v-model="listQuery.region" :label="item.id">{{ item.name }}</el-radio>
            </el-form-item>
            <el-form-item label="大区" prop="area">
              <el-radio v-for="item in projectArea" :key="item.id" v-model="listQuery.area" :disabled="onlineArea.includes(item.name)" :label="item.id">{{ item.remark }}</el-radio>
            </el-form-item>
            <el-form-item label="角色" prop="role">
              <el-checkbox-group v-model="listQuery.role">
                <el-checkbox v-for="item in ProjectRoleInfo" :key="item.id" :label="item.id">{{ item.name }}</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            <el-form-item label="服务器" prop="server">
              <el-table :data="ipList" style="width: 100%" fit highlight-current-row @sort-change="sortChange" @selection-change="handleSelectionChange">
                <el-table-column type="selection" width="55" />
                <el-table-column prop="private_ip" label="IP地址" width="180" sortable="custom" />
                <el-table-column prop="remark" label="备注" min-width="120px" sortable="custom" />
              </el-table>
            </el-form-item>
            <el-form-item label="修改时间" prop="time">
              <el-date-picker
                v-model="modifyDateTime"
                type="datetime"
                placeholder="选择日期时间"
                align="right"
                value-format="yyyy-MM-dd HH:mm:ss"
                :picker-options="pickerOptions"
              />
            </el-form-item>
            <el-form-item>
              <el-button :loading="loading" type="primary" @click="submit">执行</el-button>
            </el-form-item>
          </el-form>
          <el-dialog title="最后确认" :visible.sync="confirmExec" width="50%">
            <el-form label-width="80px" label-position="right">
              <el-form-item label="修改时间">
                {{ modifyDateTime }}
              </el-form-item>
              <el-form-item label="服务器">
                <el-table :data="ipList" style="width: 100%">
                  <el-table-column prop="private_ip" label="IP地址" width="180" />
                  <el-table-column prop="remark" label="备注" min-width="120px" />
                </el-table>
              </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
              <el-button size="mini" @click="resetDjalog">取 消</el-button>
              <el-button type="primary" size="mini" @click="confirmDjalog">确 定</el-button>
            </span>
          </el-dialog>
        </el-tab-pane>
        <el-tab-pane label="日志输出" name="taskLog">
          <pre v-highlightjs="datalist"><code class="bash" /></pre>
        </el-tab-pane>
        <el-tab-pane label="历史记录" name="history">
          <el-table v-loading="listLoading" :data="historyData" fit highlight-current-row style="width: 100%;">
            <el-table-column label="项目" prop="project" align="center" width="80px" class-name="small-padding fixed-width" />
            <el-table-column label="地区" prop="region" align="center" width="80px" class-name="small-padding fixed-width" />
            <el-table-column label="大区" prop="area" align="center" width="80px" class-name="small-padding fixed-width" />
            <el-table-column label="角色" prop="role" align="center" min-width="40px" class-name="small-padding fixed-width" />
            <el-table-column label="服务器" prop="servers" align="center" min-width="80px" class-name="small-padding fixed-width" />
            <el-table-column label="修改的时间" prop="datetime" align="center" min-width="80px" class-name="small-padding fixed-width" />
            <el-table-column label="任务ID" prop="taskId" align="center" min-width="100px" class-name="small-padding fixed-width" />
            <el-table-column label="执行时间" prop="add_time" sortable align="center" min-width="100px" class-name="small-padding fixed-width" />
            <el-table-column label="操作" align="center" width="100" class-name="small-padding fixed-width">
              <template slot-scope="{row}">
                <el-button type="primary" size="mini" @click="handleHistory(row)">执行过程</el-button>
              </template>
            </el-table-column>
          </el-table>
          <pagination v-show="total>10" :total="total" :page.sync="historyQuery.page" :limit.sync="historyQuery.pageSize" @pagination="getHistoryData"/>
        </el-tab-pane>
        <el-dialog title="执行结果" :visible.sync="historyDialog" width="80%">
          <pre v-highlightjs="historyResult"><code class="bash" /></pre>
          <span slot="footer" class="dialog-footer">
            <el-button type="primary" size="mini" @click="historyDialog = false">关闭</el-button>
          </span>
        </el-dialog>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import { getServersList } from '@/api/serversList'
import { getProjectInfo } from '@/api/project'
import { getProjectRegionInfo } from '@/api/projectRegion'
import { getProjectAreaList2 } from '@/api/projectArea'
import { getProjectRoleInfo } from '@/api/projectRole'
import { getUpdateServersDatetime, createUpdateServersDatetime } from '@/api/updateServersDatetime'
import { mapGetters } from 'vuex'
import Pagination from '@/components/Pagination'

export default {
  name: 'UpdateServersDatetime',
  components: { Pagination },
  data() {
    const validRole = (rule, value, callback) => {
      if (this.listQuery.role.length === 0) {
        callback(new Error('项目所属角色不能为空'))
      } else {
        callback()
      }
    }
    const validServer = (rule, value, callback) => {
      if (this.multipleSelection.length === 0) {
        callback(new Error('服务器不能为空'))
      } else {
        callback()
      }
    }
    const validTime = (rule, value, callback) => {
      if (this.modifyDateTime === '') {
        callback(new Error('修改时间不能为空'))
      } else {
        callback()
      }
    }
    return {
      total: 0,
      historyResult: '',
      historyDialog: false,
      confirmExec: false,
      listLoading: false,
      historyData: [],
      listQuery: {
        page: 1,
        pageSize: 1000,
        region: 1,
        project: 1,
        area: 2,
        role: [1],
        name: '',
        search: '',
        datetimeValue: [],
        order: '',
        prop: ''
      },
      historyQuery: {
        page: 1,
        pageSize: 10,
        search: '',
        order: '-id',
        user: ''
      },
      ipList: [],
      ProjectInfo: [],
      ProjectRegionInfo: [],
      projectArea: [],
      onlineArea: ['104', '105', '106'],
      ProjectRoleInfo: [],
      multipleSelection: [],
      modifyDateTime: '',
      pickerOptions: {
        shortcuts: [{
          text: '今天',
          onClick(picker) {
            picker.$emit('pick', new Date())
          }
        }, {
          text: '昨天',
          onClick(picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24)
            picker.$emit('pick', date)
          }
        }, {
          text: '一周前',
          onClick(picker) {
            const date = new Date()
            date.setTime(date.getTime() - 3600 * 1000 * 24 * 7)
            picker.$emit('pick', date)
          }
        }]
      },
      activeTab: 'taskForms',
      loading: false,
      demo2: false,
      websock: null,
      wsuri: 'ws://192.168.10.10:8000/tasks/updateServerDatetime/',
      datalist: '',
      channelName: '',
      rules: {
        project: [{ required: true, message: '请选择项目', trigger: 'blur' }],
        region: [{ required: true, message: '请选择项目所属地区', trigger: 'blur' }],
        area: [{ required: true, message: '请选择项目所属大区', trigger: 'blur' }],
        role: [{ required: true, validator: validRole, trigger: 'blur' }],
        server: [{ required: true, validator: validServer, trigger: 'blur' }],
        time: [{ required: true, validator: validTime, trigger: 'blur' }]
      }
    }
  },
  computed: {
    resultData: function() {
      const data = { role: [] }
      this.ProjectInfo.forEach(v => { if (v.id === this.listQuery.project) { data.project = v.name } })
      this.ProjectRegionInfo.forEach(v => { if (v.id === this.listQuery.region) { data.region = v.name } })
      this.projectArea.forEach(v => { if (v.id === this.listQuery.area) { data.area = v.name } })
      this.ProjectRoleInfo.forEach(v => { this.listQuery.role.forEach(r => { if (r === v.id) { data.role.push(v.name) } }) })
      data.role = data.role.join(',')
      data.servers = this.multipleSelection.join(',')
      data.datetime = this.modifyDateTime
      data.channelName = this.channelName
      return data
    },
    ...mapGetters({ currentUser: 'name' })
  },
  watch: {
    listQuery: {
      handler(newValue, oldValue) {
        this.getList()
      },
      deep: true
    }
  },
  created() {
    this.getProject()
    this.getProjectRegionInfo()
    this.getProjectArea()
    this.getProjectRoleInfo()
    this.getList()
  },
  destroyed() {
    this.ws ? this.ws.close() : '' // 离开路由之后断开websocket连接
  },
  methods: {
    initWebSocket() {
      this.ws = new WebSocket(this.wsuri)
      this.ws.onmessage = this.websocketonmessage
      this.ws.onopen = this.websocketonopen
      this.ws.onerror = this.websocketonerror
      this.ws.onclose = this.websocketclose
    },
    websocketonopen(e) { // 连接建立之后执行send方法发送数据
      console.log('浏览器WebSocket已打开')
    },
    websocketonerror() { // 连接建立失败
      this.$notify({
        title: '错误',
        message: '服务器错误，无法接收实时信息',
        type: 'error',
        duration: 2000
      })
    },
    websocketonmessage(msg) { // 数据接收
      // 转换为json对象
      const data = JSON.parse(msg.data)
      data.hasOwnProperty('channel_name') ? this.channelName = data['channel_name'] : this.datalist += data.message
    },
    websocketsend(Data) { // 数据发送
      this.websock.send(Data['channel_name'])
    },
    websocketclose(e) { // 关闭
      console.log('断开连接')
    },
    getList(obj) {
      getServersList(this.listQuery).then(response => {
        this.ipList = response.results
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
    getProjectArea() {
      const pageSize = 1000
      getProjectAreaList2(pageSize).then(response => {
        this.projectArea = response.results
      })
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
    handleSelectionChange(val) {
      this.multipleSelection = []
      val.forEach(v => {
        this.multipleSelection.push(v.private_ip)
      })
    },
    getProjectRoleInfo() {
      const pageSize = 1000
      getProjectRoleInfo(pageSize).then(response => {
        this.ProjectRoleInfo = response.results
      })
    },
    sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
    },
    submit() {
      this.$refs['listQuery'].validate((valid) => {
        if (valid) {
          this.confirmExec = true
          if (this.ws) {
            if (this.ws.readyState !== 1) {
              this.initWebSocket()
            }
          } else {
            this.initWebSocket()
          }
        } else {
          this.$message({
            title: 'Error',
            message: `表单错误清检查`,
            type: 'warning',
            duration: 2000
          })
        }
      })
    },
    resetDjalog() {
      this.confirmExec = false
    },
    confirmDjalog() {
      this.confirmExec = false
      createUpdateServersDatetime(this.resultData, 'post').then(response => {
        this.datalist = ''
        this.$notify({
          title: '成功',
          message: `任务${response.taskid}创建成功`,
          type: 'success',
          duration: 5000
        })
      })
    },
    getHistoryData(obj) {
      getUpdateServersDatetime(this.historyQuery, this.currentUser).then(response => {
        this.total = response.count
        this.historyData = response.results
      })
    },
    handleClick(tab, event) {
      if (tab.name === 'history') {
        this.getHistoryData()
      }
    },
    handleHistory(row) {
      this.historyResult = row.results
      this.historyDialog = true
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
