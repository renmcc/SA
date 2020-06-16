<template>
  <div>
    <el-form ref="postForm" :model="postForm">
      <sticky :class-name="'sub-navbar'">
        <el-button v-if="!isEdit" @click="showGuide">显示帮助</el-button>
        <el-button
          v-loading="loading"
          type="success"
          style="margin-left: 10px"
          @click="submit"
        >
          {{ isEdit ? '编辑电子书' : '新增电子书' }}
        </el-button>
      </sticky>
      <div class="detail-container">
        <waring />
        <el-row>
          <el-col :span="24">
            <ebook-upload
              :file-list="fileList"
              :disabled="isEdit"
              @onSuccess="onUploadSuccess"
              @onRemove="onUploadRemove"
            />
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item prop="title">
              <md-input v-model="postForm.title" :maxlength="100" name="name" required type="email">
                书名
              </md-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="作者:" :label-width="labelWidth" label-position="left">
              <el-input v-model="postForm.author" placeholder="作者" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="出版社:" :label-width="labelWidth" label-position="left">
              <el-input v-model="postForm.publisher" placeholder="出版社" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="语言:" :label-width="labelWidth" label-position="left">
              <el-input v-model="postForm.language" placeholder="语言" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="根文件:" :label-width="labelWidth" label-position="left">
              <el-input v-model="postForm.rootFile" placeholder="根文件" disabled />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="文件路径:" :label-width="labelWidth" label-position="left">
              <el-input v-model="postForm.filePath" placeholder="文件路径" disabled />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="解压路径:" :label-width="labelWidth" label-position="left">
              <el-input v-model="postForm.unzipPath" placeholder="解压路径" disabled />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="封面路径:" :label-width="labelWidth" label-position="left">
              <el-input v-model="postForm.filePath" placeholder="封面路径" disabled />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="文件名称:" :label-width="labelWidth" label-position="left">
              <el-input v-model="postForm.unzipPath" placeholder="文件名称" disabled />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item label="封面：" :label-width="labelWidth">
              <a v-if="postForm.cover" :href="postForm.cover" target="_blank">
                <img :src="postForm.cover" class="preview-img" alt="">
              </a>
              <span v-else>无</span>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item :label-width="labelWidth" label="目录：">
              <div v-if="postForm.contents" class="contents-wrapper">
                <el-tree />
              </div>
              <span v-else>无</span>
            </el-form-item>
          </el-col>
        </el-row>
      </div>
    </el-form>
  </div>
</template>

<script>
import Sticky from '@/components/Sticky'
import Waring from './Warning'
import EbookUpload from '@/components/EbookUpload'
import MdInput from '@/components/MDinput'

export default {
  name: 'Detail',
  components: { Sticky, Waring, EbookUpload, MdInput },
  props: {
    isEdit: Boolean
  },
  data() {
    return {
      loading: false,
      postForm: {
        status: 'draft',
        title: '',
        author: '',
        publisher: '',
        language: '',
        rootFile: '',
        filePath: ''
      },
      fileList: [],
      labelWidth: '120px'
    }
  },
  methods: {
    showGuide() {
      console.log('aaa')
    },
    submit() {
      this.loading = true
      setTimeout(() => {
        this.loading = false
      }, 1000)
    },
    onUploadSuccess() {},
    onUploadRemove() {}
  }
}
</script>

<style scoped>
  .detail-container {
    padding: 40px 50px 20px;
  }
  .preview-img {
    height: 230px;
    width: 200px;
  }
</style>
