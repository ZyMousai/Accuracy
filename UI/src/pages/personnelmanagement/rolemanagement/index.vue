<template>
  <a-card>
    <div :class="advanced ? 'search' : null">
      <a-form layout="horizontal" :model="query">
        <div :class="advanced ? null: 'fold'">
          <a-row >
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="角色名称"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-input v-model="query.role" placeholder="请输入" />
            </a-form-item>
          </a-col>
        </a-row>
        </div>
        <span style="float: right; margin-top: 3px;">
          <a-button type="primary" @click="queryevents">查询</a-button>
          <a-button style="margin-left: 8px" @click="resettingqueryform">重置</a-button>
          <a @click="toggleAdvanced" style="margin-left: 8px">
            {{advanced ? '收起' : '展开'}}
            <a-icon :type="advanced ? 'up' : 'down'" />
          </a>
        </span>
      </a-form>
    </div>
    <div>
      <a-space class="operator">
        <a-button type="primary" @click="addrole"><a-icon type="plus-circle" />新增</a-button>
        <a-button type="primary" @click="Batchdelete()"><a-icon type="delete" />批量删除</a-button>
      </a-space>
      <standard-table
        :columns="columns"
        :dataSource="dataSource"
        :selectedRows.sync="selectedRows"
        :loading="tableloading"
        :pagination="false"
        :rowKey='record=>record.id'
      >
        <div slot="action" slot-scope="{record}">
          <a @click="editrole(record.id)" style="margin-right: 8px">
            <a-icon type="edit"/>修改
          </a>
          <a @click="showdeleConfirm(record.id)">
            <a-icon type="delete" />删除
          </a>
        </div>
      </standard-table>
      <a-pagination
        style="margin-top: 15px;"
        v-model="query.page"
        :total="total"
        show-size-changer
        @showSizeChange="onShowSizeChange"
        :show-total="total => `一共 ${total} 条`"
        @change="pageonChange" />
    </div>
    <!-- 删除确认对话框 -->
    <a-modal
     title="是否删除此用户"
     :visible="dialogvisible"
     ok-text="是"
     cancel-text="否"
     @ok="user_onok"
     @cancel="user_onno">
    </a-modal>
  </a-card>
</template>

<script>
import StandardTable from '@/components/table/StandardTable'
import {RolesDate} from '@/services/personnelmanagement'
import {DeleteRoles} from "../../../services/personnelmanagement";
const columns = [
  {
    title: '角色',
    dataIndex: 'role'
  },
  {
    title: '创建人',
    dataIndex: 'creator'
  },
  {
    title: '创建时间',
    dataIndex: 'create_time'
  },
  {
    title: '更新时间',
    dataIndex: 'update_time'
  },
  {
    title: '操作',
    scopedSlots: { customRender: 'action' }
  }
]

const dataSource = []

export default {
  name: 'QueryList',
  components: {StandardTable},
  data () {
    return {
      query: {
        page: 1,
        page_size: 10,
        role: ''
      },
      total: 0,
      tableloading: false,
      advanced: true,
      ids: [],
      dialogvisible: false,
      columns: columns,
      dataSource: dataSource,
      selectedRows: [],
      roleoptions: ['商务', "技术"]
    }
  },
  created () {
    this.gettabledata()
  },
  methods: {
    // 获取表格数据
    gettabledata () {
      this.tableloading = true
      RolesDate(this.query).then(res => {
        if (res.status === 200) {
          this.dataSource = res.data.data
          this.total = res.data.total
          this.tableloading = false
          for (var i = 0; i < this.dataSource.length; i++) {
            this.dataSource[i]["index"] = i + 1
          }
        } else {
          this.tableloading = false
          this.$message.error(`获取数据失败！`);
        }
      })
    },
    toggleAdvanced () {
      this.advanced = !this.advanced
    },
    // 查询
    queryevents() {
      this.gettabledata()
    },
    // 批量删除
    Batchdelete() {
      this.ids = []
      for (let i = 0; i < this.selectedRows.length; i++) {
        this.ids.push(this.selectedRows[i].id)
      }
      this.dialogvisible = true
    },
    // 重置查询表单
    resettingqueryform() {
      for(var key in this.query) {
        this.query[key] = ''
      }
    },
    // 新增角色
    addrole() {
      this.$router.push('/personnelmanagement/addrole')
    },
    // 编辑角色
    editrole(id) {
      this.$router.push('/personnelmanagement/editrole/?' + id)
    },
    async user_onok() {
      for (let i = 0; i < this.ids.length; i++) {
        await DeleteRoles(this.ids[i]).then(res => {
          if (res.status === 200) {
            this.$message.success(`删除成功！`);
          } else {
            this.$message.error(`删除失败！`);
          }  
        })
      }
      const totalPage = Math.ceil((this.total - 1) / this.query.page_size)
      this.query.page = this.query.page > totalPage ? totalPage : this.query.page
      this.query.page = this.query.page < 1 ? 1 : this.query.page
      this.gettabledata()
      this.ids = []
      this.dialogvisible = false
    },
    async user_onno() {
      this.ids = []
      this.dialogvisible = false
    },
    // 删除对话框
    showdeleConfirm(id) {
      this.ids.push(id)
      this.dialogvisible = true
    },
    // 分页配置
    onShowSizeChange(current, pageSize) {
      this.query.page = 1
      this.query.page_size = pageSize
      this.gettabledata()
    },
    pageonChange(pageNumber) {
      this.query.page = pageNumber
      this.gettabledata()
    },
  }
}
</script>

<style lang="less" scoped>
  .search{
    margin-bottom: 54px;
  }
  .fold{
    width: calc(100% - 216px);
    display: inline-block
  }
  .operator{
    margin-bottom: 18px;
  }
  @media screen and (max-width: 900px) {
    .fold {
      width: 100%;
    }
  }
</style>
