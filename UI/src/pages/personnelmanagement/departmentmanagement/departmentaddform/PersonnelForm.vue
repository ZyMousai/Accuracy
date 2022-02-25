<template>
  <form :autoFormCreate="(form) => this.form = form">
    <a-table
      :columns="columns"
      :dataSource="dataSource"
      :pagination="false"
      :rowKey='record=>record.id'
      :loading="tableloading"
    >
      <template  v-for="(col, i) in ['name']" :slot="col" slot-scope="text, record">
          <a-select
            :key="col"
            v-if="record.editable"
            v-model="userid"
            :placeholder="columns[i].title"
            style="margin: -5px 0"
            @change="e => handleChange(e, record.key, col)">
            <a-select-option v-for="item in useroptions" :key="item.id" :value="item.id">
              {{item.name}}
            </a-select-option>
          </a-select>
          <template v-else>{{text}}</template>
      </template>
      <template slot="operation" slot-scope="text, record">
        <template v-if="record.editable">
          <span v-if="record.isNew">
            <a @click="saveRow(record.key)">添加</a>
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
          <a-popconfirm title="是否要删除此行？" @confirm="userremove(record.id)">
            <a>删除</a>
          </a-popconfirm>
        </span>
      </template>
    </a-table>
    <a-button v-if="isshowbutton" style="width: 100%; margin-top: 16px; margin-bottom: 8px" type="dashed" icon="plus" @click="newMember">新增成员</a-button>
  </form>
</template>

<script>
import {UsersDate, GetDepartmentUser, AddDepartmentUser, DeleteDepartmentUser} from '@/services/personnelmanagement'
const columns = [
  {
    title: '姓名',
    dataIndex: 'name',
    key: 'name',
    width: '25%',
    scopedSlots: { customRender: 'name' }
  },
  {
    title: '添加时间',
    dataIndex: 'entry_time',
    key: 'entry_time',
    width: '20%',
    scopedSlots: { customRender: 'entry_time' }
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
      isshowbutton: false,
      tableloading: false,
      userid: '',
      useroptions: []
    }
  },
  created () {
    this.geturldata()
    this.getuserall()
    this.getpersonnoldata()
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
    // 获取全部用户数据
    getuserall() {
      UsersDate().then(res => {
        console.log(res);
        if (res.status === 200) {
          this.useroptions = res.data.data
        } else {
          this.$message.error('获取用户列表失败！')
        }
      })
    },
    getpersonnoldata() {
      const query = {
        department_id: this.id
      }
      GetDepartmentUser(query).then(res => {
        this.tableloading = true
        if (res.status === 200) {
          this.tableloading = false
          this.dataSource = res.data.data
        } else {
          this.tableloading = false
          this.$message.error('获取用户列表失败！')
        }
      })
    },
    newMember () {
      this.dataSource.push({
        key: this.dataSource.length + 1,
        name: '',
        editable: true,
        isNew: true
      })
    },
    remove (key) {
      const newData = this.dataSource.filter(item => item.key !== key)
      this.dataSource = newData
    },
    saveRow (key) {
      console.log(this.userid);
      if (this.userid) {
        let target = this.dataSource.filter(item => item.key === key)[0]
        target.editable = false
        target.isNew = false
        const form = {
          department_id: '',
          ids: []
        }
        form.department_id = this.id
        form.ids.push(this.userid)
        AddDepartmentUser(form).then(res => {
          console.log(res);
          if (res.status === 200) {
            this.$message.success(`添加成功！`);
            this.getpersonnoldata()
          }
        })
      } else {
        this.$message.error('请选择用户！')
      }
    },
    // 删除用户
    userremove(id) {
      const data = {
        department_id: this.id,
        ids: []
      }
      data.ids.push(id)
      DeleteDepartmentUser(data).then(res => {
        if (res.status === 200) {
          this.$message.success(`删除成功！`);
          this.getpersonnoldata()
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
      const user = this.useroptions.filter(i => value === i.id)[0]
      if (target) {
        target[column] = user.name
        this.dataSource = newData
      }
    }
  }
}
</script>

<style scoped>

</style>
