<template>
  <div>
    <el-input v-model="input" placeholder="请输入内容" />
  </div>
</template>

<script>
export default {
  name: 'BookList',
  data() {
    return {
      isCollapse: false,
      input: ''
    }
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log('handleSelect', key, keyPath)
    },
    handleOpen(key, keyPath) {
      console.log('handleOpen', key, keyPath)
    },
    handleClose(key, keyPath) {
      console.log('handleClose', key, keyPath)
    }
  }
}
</script>
