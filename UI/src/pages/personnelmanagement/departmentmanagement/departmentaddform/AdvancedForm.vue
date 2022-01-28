<template>
  <div>
    <a-card class="card" title="新增部门" :bordered="false">
      <repository-form ref="repository" :showSubmit="false" />
    </a-card>
    <a-card title="部门关联角色选择" :bordered="false">
      <role-form />
    </a-card>
    <a-card title="部门人员管理" :bordered="false">
      <personnel-form />
    </a-card>
    <footer-tool-bar>
      <a-button type="primary" @click="validate" :loading="loading">提交</a-button>
    </footer-tool-bar>
  </div>
</template>

<script>
import RepositoryForm from './RepositoryForm'
import RoleForm from './RoleForm'
import PersonnelForm from './PersonnelForm'
import FooterToolBar from '@/components/tool/FooterToolBar'

export default {
  name: 'AdvancedForm',
  components: {FooterToolBar, RoleForm, RepositoryForm, PersonnelForm},
  data () {
    return {
      loading: false
    }
  },
  computed: {
    desc() {
      return this.$t('desc')
    }
  },
  methods: {
    validate () {
      this.$refs.repository.form.validateFields((err, values) => {
        if (!err) {
          console.log('Received values of form: ', values)
        }
      });
      this.$refs.task.form.validateFields((err, values) => {
        if (!err) {
          console.log('Received values of form: ', values)
        }
      })
    }
  }
}
</script>

<style lang="less" scoped>
  .card{
    margin-bottom: 24px;
  }
</style>
