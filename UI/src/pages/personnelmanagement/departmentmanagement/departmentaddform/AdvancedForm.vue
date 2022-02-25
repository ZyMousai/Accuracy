<template>
  <div>
    <a-card class="card" :title="tablename" :bordered="false">
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
import {AddDepartment, EditDepartment} from '@/services/personnelmanagement'
import RepositoryForm from './RepositoryForm'
import RoleForm from './RoleForm'
import PersonnelForm from './PersonnelForm'
import FooterToolBar from '@/components/tool/FooterToolBar'

export default {
  name: 'AdvancedForm',
  components: {FooterToolBar, RoleForm, RepositoryForm, PersonnelForm},
  data () {
    return {
      loading: false,
      tablename: '新增部门',
      id: '',
      inputdata: ''
    }
  },
  computed: {
    desc() {
      return this.$t('desc')
    }
  },
  created () {
    this.geturldata()
  },
  methods: {
    // 获取url的参数
    geturldata() {
      this.id = location.href.split("?")[1]
      if (this.id) {
        this.tablename = '部门修改'
      }
    },
    validate () {
      this.$refs.repository.form.validateFields((err, values) => {
        if (!err) {
          this.loading = true
          this.tablename === '新增部门' ? this.addadta(values) : this.ediddata(values)
        }
      });
    },
    addadta(values) {
      this.loading = true
      const form = {}
      form.department = values.department
      form.creator = localStorage.getItem('name')
      AddDepartment(form).then(res => {
        if (res.status === 200) {
          this.$message.success(`${this.tablename}成功！`);
          this.$router.push('/personnelmanagement/departmentmanagement')
          this.$refs.repository.form.resetFields()
          this.loading = false
        } else {
          this.$message.error(`${this.tablename}失败！`);
          this.loading = false
        }
      })
    },
    ediddata(values) {
      this.loading = true
      const form = {}
      form.department = values.department
      form.id = this.id
      EditDepartment(form).then(res => {
        if (res.status === 200) {
          this.$message.success(`${this.tablename}成功！`);
          this.$router.push('/personnelmanagement/departmentmanagement')
          this.$refs.repository.form.resetFields()
          this.loading = false
        } else {
          this.$message.success(`${this.tablename}失败！`);
          this.loading = false
        }
      })}
  }
}
</script>

<style lang="less" scoped>
  .card{
    margin-bottom: 24px;
  }
</style>
