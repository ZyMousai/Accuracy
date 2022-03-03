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
    <a-form-model-item label="菜单选择" prop="menu">
      <a-select v-model="form.menu" placeholder="请选择菜单" mode="multiple">
        <a-select-opt-group v-for="item in menuoptions" :label="item.menu_name" :key="item.id">
          <a-select-option v-for="sonitem in item.son_menu" :value="sonitem.id" :key="sonitem.id">
            {{sonitem.menu_name}}
          </a-select-option>
        </a-select-opt-group>
      </a-select>
    </a-form-model-item>
    <a-form-model-item label="权限选择" prop="permissionarr">
      <a-checkbox-group v-model="form.permissionarr">
        <a-checkbox v-for="item in operationoptions" :value="item.id" name="type" :key="item.id">
          {{ item.operate }}
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
import {GetRoleMenu, AddRole, AddRoleMenu, AddRolePermission, GetOneRolesDate} from '@/services/personnelmanagement'
export default {
  name: 'BasicForm',
  data () {
    return {
      value: 1,
      form: {
        name: '',
        menu: [],
        firstmenu: [],
        sontmenu: [],
        permissionarr: []
      },
      roleid: '',
      editroleid: '',
      isdisabled: true,
      menuoptions: [],
      useroptions: [],
      operationoptions: [{id: 1, operate:'新增'}, {id: 2, operate:'修改'},{id: 3, operate:'删除'},{id: 4, operate:'查看'},{id: 5, operate:'搜索'}],
      secondarymenuoptions: [],
      rules: {
        name: [{ required: true, message: '请填写角色名', trigger: 'blur' }],
        menu: [{type: 'array', required: true, message: '请选择菜单', trigger: 'change' }],
        firstmenu: [{type: 'array', required: true, message: '请选择一级菜单', trigger: 'change' }],
        sontmenu: [{type: 'array', required: true, message: '请至少选择一个二级菜单', trigger: 'change',}],
        permissionarr: [{type: 'array', required: true, message: '请至少选择一个权限', trigger: 'change',}]
      },
    }
  },
  created() {
    this.gerallmenu()
    this.geturldata()
  },
  methods: {
    // 获取url的参数
    geturldata() {
      this.form = {}
      this.editroleid = location.href.split("?")[1]
      console.log(this.editroleid);
      if (this.editroleid) {
        GetOneRolesDate(this.editroleid).then(res => {
          console.log(res);
        })
      }
    },
    gerallmenu() {
      GetRoleMenu().then(res => {
        if (res.status === 200) {
          this.menuoptions = res.data.data
        } else {
          this.$message.error(`获取菜单数据失败！`);
        }
      })
    },
    onSubmit() {
      this.$refs.ruleForm.validate(valid => {
        if (valid) {
          this.addrole()
        }
      });
    },
    // 新增角色
    addrole() {
      const data = {
        role: this.form.name,
        creator: localStorage.getItem('name')
      }
      AddRole(data).then(res => {
        if (res.status === 200) {
          this.roleid = res.data.id
          this.addrolemenu()
        } else {
          this.$message.error(`添加角色失败！`);
        }
      })
    },
    // 新增菜单
    addrolemenu() {
      const data = {
        role_id: this.roleid,
        ids: this.form.menu
      }
      AddRoleMenu(data).then(res => {
        if (res.status === 200) {
          this.addoperationauthority()
        } else {
          this.$message.error(`添加角色失败！`);
        }
      })
    },
    // 删除菜单
    // 新增操作权限
    addoperationauthority() {
      const data = {
        role_id: this.roleid,
        ids: this.form.permissionarr
      }
      AddRolePermission(data).then(res => {
        if (res.status === 200) {
          this.$message.success(`添加角色成功！`);
          this.$router.push('/personnelmanagement/rolemanagement')
          this.$refs.ruleForm.resetFields();
        } else {
          this.$message.error(`添加角色失败！`);
        }
      })
    },
    // 删除操作权限
    resetForm() {
      this.$refs.ruleForm.resetFields();
    },
  }
}
</script>

<style scoped>

</style>
