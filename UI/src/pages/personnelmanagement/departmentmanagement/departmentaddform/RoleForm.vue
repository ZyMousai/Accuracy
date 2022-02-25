<template>
  <form :autoFormCreate="(form) => this.form = form">
    <a-table
      :columns="columns"
      :dataSource="dataSource"
      :pagination="false"
      :rowKey='record=>record.id'
      :loading="tableloading"
    >
      <template  v-for="(col, i) in ['role']" :slot="col" slot-scope="text, record">
          <a-select
            :key="col"
            v-if="record.editable"
            v-model="roleid"
            :placeholder="columns[i].title"
            style="margin: -5px 0"
            @change="e => handleChange(e, record.key, col)">
            <a-select-option v-for="item in roleoptions" :key="item.id" :value="item.id">
              {{item.role}}
            </a-select-option>
          </a-select>
          <template v-else>{{text}}</template>
      </template>
      <template slot="operation" slot-scope="text, record">
        <template v-if="record.editable">
          <span v-if="record.isNew">
            <a @click="saveRow(record, record.key)">添加</a>
            <a-divider type="vertical" />
            <a-popconfirm title="是否要删除此行？" @confirm="remove(record.key)">
              <a>刪除</a>
            </a-popconfirm>
          </span>
            <!-- <span v-else>
            <a @click="saveRow(record.key)">保存</a>
            <a-divider type="vertical" />
            <a @click="cancle(record.key)">取消</a>
          </span> -->
        </template>
        <span v-else>
          <!-- <a @click="toggle(record.key)">编辑</a>
          <a-divider type="vertical" /> -->
          <a-popconfirm title="是否要删除此行？" @confirm="roleremove(record.id)">
            <a>删除</a>
          </a-popconfirm>
        </span>
      </template>
    </a-table>
    <a-button v-if="isshowbutton" style="width: 100%; margin-top: 16px; margin-bottom: 8px" type="dashed" icon="plus" @click="newMember">新增成员</a-button>
  </form>
</template>

<script>
import {GetDepartmentRole, RolesDate, AddDepartmentRole, DeleteDepartmentRole} from '@/services/personnelmanagement'
const columns = [
  {
    title: '角色',
    dataIndex: 'role',
    key: 'role',
    width: '25%',
    scopedSlots: { customRender: 'role' }
  },
  {
    title: '添加时间',
    dataIndex: 'create_time',
    key: 'create_time',
    width: '20%',
    scopedSlots: { customRender: 'create_time' }
  },
  {
    title: '操作',
    key: 'operation',
    scopedSlots: { customRender: 'operation' }
  }
]

const dataSource = []

export default {
  name: 'UserForm',
  data () {
    return {
      columns,
      dataSource,
      id: '',
      isshowbutton: false,
      roleid: '',
      roleoptions: [],
      tableloading: false
    }
  },
  created () {
    this.geturldata()
    this.getroledata()
    this.getroleall()
  },
  methods: {
    // 获取url的参数
    geturldata() {
      this.dataSource = []
      this.id = location.href.split("?")[1]
      if (this.id) {
        this.isshowbutton = true
      }
    },
    // 获取全部角色数据
    getroleall() {
      RolesDate().then(res => {
        console.log(res);
        if (res.status === 200) {
          this.roleoptions = res.data.data
        } else {
          this.$message.error('获取角色列表失败！')
        }
      })
    },
    getroledata() {
      const query = {
        department_id: this.id
      }
      GetDepartmentRole(query).then(res => {
        this.tableloading = true
        if (res.status === 200) {
          this.tableloading = false
          this.dataSource = res.data.data
        } else {
          this.tableloading = false
          this.$message.error('获取角色列表失败！')
        }
      })
    },
    newMember () {
      this.dataSource.push({
        key: this.dataSource.length + 1,
        role: '',
        create_time: '',
        editable: true,
        isNew: true
      })
    },
    remove (key) {
      const newData = this.dataSource.filter(item => item.key !== key)
      this.dataSource = newData
    },
    saveRow (record, key) {
      console.log(this.roleid);
      if (this.roleid) {
        let target = this.dataSource.filter(item => item.key === key)[0]
        target.editable = false
        target.isNew = false
        const form = {
          department_id: '',
          ids: []
        }
        form.department_id = this.id
        form.ids.push(this.roleid)
        AddDepartmentRole(form).then(res => {
          console.log(res);
          if (res.status === 200) {
            this.$message.success(`添加成功！`);
            this.getroledata()
          }
        })
      } else {
        this.$message.error('请选择角色！')
      }
    },
    // 删除角色
    roleremove(id) {
      const data = {
        department_id: this.id,
        ids: []
      }
      data.ids.push(id)
      DeleteDepartmentRole(data).then(res => {
        if (res.status === 200) {
          this.$message.success(`删除成功！`);
          this.getroledata()
        } else {
          this.$message.error('删除失败！')
        }
      })
    },
    toggle (key) {
      let target = this.dataSource.filter(item => item.key === key)[0]
      target.editable = !target.editable
    },
    getRowByKey (key, newData) {
      const data = this.dataSource
      return (newData || data).filter(item => item.key === key)[0]
    },
    cancle (key) {
      let target = this.dataSource.filter(item => item.key === key)[0]
      target.editable = false
    },
    handleChange (value, key, column) {
      const newData = [...this.dataSource]
      const target = newData.filter(item => key === item.key)[0]
      const role = this.roleoptions.filter(i => value === i.id)[0]
      if (target) {
        target[column] = role.role
        this.dataSource = newData
      }
    }
  }
}
</script>

<style scoped>

</style>
