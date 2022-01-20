<template>
  <div class="new-page" :style="`min-height: ${pageMinHeight}px`">
    <h1>用户管理</h1>
  </div>
</template>

<script>
  import {mapState} from 'vuex'
  export default {
    name: 'usermanagement',
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