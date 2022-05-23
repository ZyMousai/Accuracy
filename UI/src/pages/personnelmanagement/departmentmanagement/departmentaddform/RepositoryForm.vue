<template>
  <a-form @submit="handleSubmit" :form="form" class="form">
    <a-row class="form-row">
      <a-col :lg="6" :md="12" :sm="24">
        <a-form-item label="部门名称">
          <a-input
            placeholder="请输入部门名称"
            v-decorator="['department', {rules: [{ required: true, message: '请输入部门名称', whitespace: true}]}]"
          />
        </a-form-item>
      </a-col>
    </a-row>
    <a-form-item v-if="showSubmit">
      <a-button htmlType="submit" >Submit</a-button>
    </a-form-item>
  </a-form>
</template>

<script>
import {GetOneDepartmentDate} from '@/services/personnelmanagement'
export default {
  name: 'RepositoryForm',
  props: ['showSubmit', 'inputvale'],
  data() {
    return {
      form: this.$form.createForm(this)
    }
  },
  created() {
    this.geturldata()
  },
  methods: {
    handleSubmit (e) {
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log('Received values of form: ', values)
        }
      })
    },
    // 获取部门信息
    geturldata() {
      const id = location.href.split("?")[1]
      if (id) {
        GetOneDepartmentDate(id).then(res => {
          if (res.status === 200) {
            this.form.setFieldsValue({
              department: res.data.data.department
            })
            this.$message.success(`获取${res.data.data.department}信息成功！`);
          } else {
            this.$message.error(`获取${res.data.data.department}信息失败！`);
          }
        })
      }
    },
  }
}
</script>

<style lang="less" scoped>
  .form{
    .form-row{
      margin: 0 -8px
    }
    .ant-col-md-12,
    .ant-col-sm-24,
    .ant-col-lg-6,
    .ant-col-lg-8,
    .ant-col-lg-10,
    .ant-col-xl-8,
    .ant-col-xl-6{
      padding: 0 8px
    }
  }
</style>
