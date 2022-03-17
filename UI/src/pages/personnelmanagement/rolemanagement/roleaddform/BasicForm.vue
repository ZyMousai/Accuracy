<template>
  <a-card :body-style="{padding: '24px 32px'}" :bordered="false">
      <a-form-model
        ref="ruleForm"
        :model="form"
        :rules="rules"
        :label-col="{ span: 7 }"
        :wrapper-col="{ span: 10 }"
      >
    <a-form-model-item ref="role" label="角色名" prop="role">
      <a-input v-model="form.role" @change="inputchange" />
    </a-form-model-item>
    <!-- <a-form-model-item label="菜单选择" prop="menu">
      <a-select v-model="form.menu" placeholder="请选择菜单" mode="multiple">
        <a-select-opt-group v-for="item in menuoptions" :label="item.name" :key="item.id">
          <a-select-option v-for="sonitem in item.children" :value="sonitem.id" :key="sonitem.id">
            {{sonitem.name}}
          </a-select-option>
        </a-select-opt-group>
      </a-select>
    </a-form-model-item> -->
    <a-form-model-item label="菜单选择" prop="menu">
      <a-tree-select
        v-model="preselectionmenu"
        :treeCheckable="true"
        style="width: 100%"
        placeholder="选择菜单"
        allow-clear
        showCheckedStrategy="SHOW_ALL"
        @change="onchange"
      >
        <a-tree-select-node v-for="item in menuoptions" :key="item.name" :title="item.name" :value="item.name">
          <a-tree-select-node v-for="sonitem in item.children" :key="sonitem.name" :title="sonitem.name" :value="sonitem.name">
            <a-tree-select-node v-for="operateitem in sonitem.permission" :value="operateitem.id" :key="operateitem.id" :title="operateitem.operate + '(' + operateitem.remark + ')'">
            </a-tree-select-node>
          </a-tree-select-node>
        </a-tree-select-node>
      </a-tree-select>
    </a-form-model-item>
    <!-- <a-form-model-item label="权限选择" prop="permissionarr">
      <a-checkbox-group v-model="form.permissionarr">
        <a-checkbox v-for="item in operationoptions" :value="item.id" name="type" :key="item.id">
          {{ item.operate }}
        </a-checkbox>
      </a-checkbox-group>
    </a-form-model-item> -->
    <a-form-model-item style="margin-top: 24px" :wrapperCol="{span: 10, offset: 7}">
      <a-button type="primary" @click="onSubmit" :disabled="isdisabled">
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
import {GetRoleMenu, AddRole, EditRole, AddRoleMenu, AddRolePermission, GetOneRolesDate, DeleteRoleMenu, DeleteRolePermission} from '@/services/personnelmanagement'
export default {
  name: 'BasicForm',
  data () {
    return {
      value: 1,
      form: {
        role: '',
        menu: [],
        permissionarr: []
      },
      reform: {
        menu: [],
        permissionarr: []
      },
      roleid: '',
      isdisabled: true,
      menuoptions: [],
      useroptions: [],
      checkList: [],
      menudata: [],
      preselectionmenu: [],
      operationoptions: [{id: 1, operate:'新增'}, {id: 2, operate:'修改'},{id: 3, operate:'查看'},{id: 4, operate:'删除'}],
      secondarymenuoptions: [],
      rules: {
        role: [{ required: true, message: '请填写角色名', trigger: 'blur' }],
        // menu: [{type: 'array', required: true, message: '请选择菜单', trigger: 'change' }],
        // permissionarr: [{type: 'array', required: true, message: '请至少选择一个权限', trigger: 'change',}]
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
      this.roleid = location.href.split("?")[1]
      if (this.roleid) {
        GetOneRolesDate(this.roleid).then(res => {
          this.form.role = res.data.data.role
          this.preselectionmenu.push(...res.data.permission_id_list)
          this.form.permissionarr.push(...res.data.permission_id_list)
          this.reform.permissionarr.push(...res.data.permission_id_list)
          this.form.menu.push(...res.data.menu_id_list)
          this.reform.menu.push(...res.data.menu_id_list)
          console.log();
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
          this.isdisabled = true
          console.log(this.form);
          if (this.roleid) {
            this.editrole()
          } else {
            this.addrole()
          }
        }
      });
    },
    // 新增角色
    addrole() {
      const data = {
        role: this.form.role,
        creator: localStorage.getItem('name')
      }
      AddRole(data).then(res => {
        if (res.status === 200) {
          this.roleid = res.data.id
          this.addrolemenu(this.form)
          this.addoperationauthority(this.form)
        } else {
          this.$message.error(`添加角色失败！`);
        }
      })
    },
    // 编辑角色名
    editrole() {
      const data = {
        id: this.roleid,
        role: this.form.role
      }
      EditRole(data).then(res => {
        if (res.status === 200) {
          this.daleterolemenu(this.reform)
          this.daleteoperationauthority(this.reform)
        } else {
          this.$message.error(`编辑角色失败！`);
        }
      })
    },
    // 新增菜单
    addrolemenu(from) {
      const data = {
        role_id: this.roleid,
        ids: from.menu
      }
      AddRoleMenu(data).then(res => {
        if (res.status !== 200) {
          this.$message.error(`添加角色失败！`);
        }
      })
    },
    // 删除菜单
    daleterolemenu(from) {
      const data = {
        role_id: this.roleid,
        ids: from.menu
      }
      DeleteRoleMenu(data).then(res => {
        if (res.status === 200) {
          this.addrolemenu(this.form)
        } else {
          this.$message.error(`修改角色失败！`);
        }
      })
    },
    // 新增操作权限
    addoperationauthority(from) {
      const data = {
        role_id: this.roleid,
        ids: from.permissionarr
      }
      AddRolePermission(data).then(res => {
        if (res.status === 200) {
          this.$message.success(`操作成功！`);
          this.$router.push('/personnelmanagement/rolemanagement')
          this.roleid = ''
          this.reform = {
            menu: [],
            permissionarr: []
          }
          this.isdisabled = false
          this.$refs.ruleForm.resetFields();
        } else {
          this.$message.error(`添加角色失败！`);
        }
      })
    },
    // 删除操作权限
    daleteoperationauthority(from) {
      const data = {
        role_id: this.roleid,
        ids: from.permissionarr
      }
      DeleteRolePermission(data).then(res => {
        if (res.status === 200) {
          this.addoperationauthority(this.form)
        } else {
          this.$message.error(`修改角色失败！`);
        }
      })
    },
    resetForm() {
      this.isdisabled = false
      this.$refs.ruleForm.resetFields();
      this.preselectionmenu = []
    },
    onchange(value, node, extra) {
      this.isdisabled = false
      this.form.menu = []
      const halfCheckedKeys = extra.triggerNode.vcTree._data._halfCheckedKeys
      this.form.permissionarr = value.toString().match(/\d+/g)
      this.menuoptions.forEach(e => {
        e.children.forEach(i => {
          value.forEach(y => {
            if (i.name === y) {
              this.form.menu.push(i.id)
            }
          })
        })
      })
      this.menuoptions.forEach(e => {
        e.children.forEach(i => {
          halfCheckedKeys.forEach(y => {
            if (i.name === y) {
              this.form.menu.push(i.id)
            }
          })
        })
      })
    },
    inputchange() {
      this.isdisabled = false
    }
  }
}
</script>

<style scoped>

</style>
