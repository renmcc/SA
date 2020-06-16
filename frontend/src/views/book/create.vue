<template>
  <div class="book-container">
    <detail :is-edit="false" />
  </div>
</template>

<script>
import Detail from './components/Detail'

export default {
  components: {
    Detail
  },
  data() {
    return {
    }
  }
}
</script>

<style scoped>
  .book-container {

  }
</style>
