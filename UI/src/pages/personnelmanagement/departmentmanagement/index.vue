<template>
  <div class="new-page" :style="`min-height: ${pageMinHeight}px`">
    <h1>部门管理</h1>
  </div>
</template>

<script>
  import {mapState} from 'vuex'
  export default {
    name: 'departmentmanagement',
    data() {
      return {
      }
    },
    computed: {
      ...mapState('setting', ['pageMinHeight']),
      desc() {
        return this.$t('description')
      }
    }
  }
</script>

<style scoped lang="less">
@import "index";
</style>