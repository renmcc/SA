<template>
  <div class="upload-container">
    <el-upload
      :action="action"
      :name="name"
      :headers="headers"
      :multiple="false"
      :limit="1"
      :before-upload="beforeUpload"
      :on-success="onSuccess"
      :on-error="onError"
      :on-remove="onRemove"
      :file-list="fileList"
      :on-exceed="onExceed"
      :disabled="disabled"
      drag
      show-file-list
      accept="application/zip"
      class="image-upload"
    >
      <i class="el-icon-upload" />
      <div v-if="fileList.length === 0" class="el-upload__text">
        请将电子书拖入或 <em>点击上传</em>
      </div>
      <div v-else class="el-upload__text">图书已上传</div>
    </el-upload>
  </div>
</template>

<script>
import { getToken } from '@/utils/auth'

export default {
  name: 'EbookUpload',
  props: {
    fileList: {
      type: Array,
      default() {
        return []
      }
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      action: `${process.env.VUE_APP_BASE_API}/api/uploadBook/`,
      name: 'book'
    }
  },
  computed: {
    headers() {
      return {
        Authorization: `Bearer ${getToken()}`
      }
    }
  },
  methods: {
    beforeUpload(file) {
      this.$emit('beforeUpload', file)
    },
    onSuccess(response, file) {
      this.$message({
        message: '上传成功',
        type: 'success'
      })
      this.$emit('onSuccess', file)
    },
    onError(err) {
      this.$message({
        message: '上传失败',
        type: 'error'
      })
      this.$emit('onError', err)
    },
    onRemove() {
      this.$message({
        message: '删除成功',
        type: 'success'
      })
      this.$emit('onRemove')
    },
    onExceed() {
      this.$message({
        message: '每次只能上传一本电子书',
        type: 'warning'
      })
    }
  }
}
</script>

<style scoped>

</style>
