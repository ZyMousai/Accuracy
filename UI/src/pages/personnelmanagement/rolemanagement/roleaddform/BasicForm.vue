<template>
  <a-card :body-style="{padding: '24px 32px'}" :bordered="false">
      <a-form-model
        ref="ruleForm"
        :model="form"
        :rules="rules"
        :label-col="{ span: 7 }"
        :wrapper-col="{ span: 10 }"
      >
    <a-form-model-item ref="name" label="角色名" prop="name">
      <a-input v-model="form.name" />
    </a-form-model-item>
    <a-form-model-item label="一级菜单选择" prop="firstmenu">
      <a-select v-model="form.firstmenu" placeholder="请选择一级菜单">
        <a-select-option v-for="item in firstmenulist" :key="item" :value="item">
          {{item}}
        </a-select-option>
      </a-select>
    </a-form-model-item>
    <a-form-model-item label="二级菜单选择" prop="secondarymenu">
      <a-checkbox-group v-model="form.secondarymenu">
        <a-checkbox value="1" name="type">
          文档
        </a-checkbox>
        <a-checkbox value="2" name="type">
          回收站
        </a-checkbox>
      </a-checkbox-group>
    </a-form-model-item>
    <a-form-model-item label="权限选择" prop="permissionarr">
      <a-checkbox-group v-model="form.permissionarr">
        <a-checkbox value="1" name="type">
          新增
        </a-checkbox>
        <a-checkbox value="2" name="type">
          修改
        </a-checkbox>
        <a-checkbox value="3" name="type">
          删除
        </a-checkbox>
        <a-checkbox value="3" name="type">
          查看
        </a-checkbox>
        <a-checkbox value="3" name="type">
          搜索
        </a-checkbox>
      </a-checkbox-group>
    </a-form-model-item>
    <a-form-model-item style="margin-top: 24px" :wrapperCol="{span: 10, offset: 7}">
      <a-button type="primary" @click="onSubmit">
        提交
      </a-button>
      <a-button style="margin-left: 10px;" @click="resetForm">
        重置
      </a-button>
    </a-form-model-item>
  </a-form-model>
  </a-card>
</template>

<script>
export default {
  name: 'BasicForm',
  data () {
    return {
      value: 1,
      form: {
        name: '',
        firstmenu: undefined,
        delivery: false,
        secondarymenu: [],
        permissionarr: []
      },
      firstmenulist: ['文档管理'],
      rules: {
        name: [
          { required: true, message: '请填写角色名', trigger: 'blur' }
        ],
        firstmenu: [{ required: true, message: '请选择一级菜单', trigger: 'change' }],
        secondarymenu: [
          {
            type: 'array',
            required: true,
            message: '请至少选择一个二级菜单',
            trigger: 'change',
          },
        ],
        permissionarr: [
          {
            type: 'array',
            required: true,
            message: '请至少选择一个权限',
            trigger: 'change',
          },
        ]
      },
    }
  },
  methods: {
    onSubmit() {
      this.$refs.ruleForm.validate(valid => {
        if (valid) {
          alert('submit!');
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    resetForm() {
      this.$refs.ruleForm.resetFields();
    },
  }
}
</script>

<style scoped>

</style>
