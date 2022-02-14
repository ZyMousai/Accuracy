<template>
  <a-card>
    <div :class="advanced ? 'search' : null">
      <a-form layout="horizontal" :model="query">
        <div :class="advanced ? null: 'fold'">
          <a-row >
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="姓名"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-input v-model="query.platform" placeholder="请输入" />
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="部门"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-select v-model="query.department" placeholder="请选择">
                <a-select-option v-for="item in departmentoptions" :key="item['department']" :value="item['id']">
                  {{item['department']}}
                </a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="角色"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-select v-model="query.department" placeholder="请选择">
                <a-select-option v-for="item in roleoptions" :key="item" :value="item">
                  {{item}}
                </a-select-option>
              </a-select>
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
        <a-button type="primary" @click="showModal"><a-icon type="plus-circle" />新增</a-button>
        <a-button type="primary" @click="Batchdelete()"><a-icon type="delete" />批量删除</a-button>
      </a-space>
      <standard-table
        :columns="columns"
        :dataSource="dataSource"
        :selectedRows.sync="selectedRows"
        :rowKey='record=>record.id'
        @clear="onClear"
        @change="onChange"
      >
        <div slot="description" slot-scope="{text}">
          {{text}}
        </div>
        <div slot="action" slot-scope="{record}">
          <a @click="showModal(record.id)" style="margin-right: 8px">
            <a-icon type="edit"/>修改
          </a>
          <a @click="resetPassword(record.id)" style="margin-right: 8px">
            <a-icon type="retweet" />重置密码
          </a>
          <a @click="showdeleConfirm(record.id)">
            <a-icon type="delete" />删除
          </a>
        </div>
        <template slot="statusTitle">
          <a-icon @click.native="onStatusTitleClick" type="info-circle" />
        </template>
      </standard-table>
      <!-- 表单 -->
      <a-modal v-model="visible" :title="tablename" on-ok="handleOk" :maskClosable="false" @afterClose="handleCancel()" :width='850'>
      <template slot="footer">
        <a-button key="back" @click="handleCancel">
          取消
        </a-button>
        <a-button key="submit" type="primary" :loading="loading" @click="handleOk">
          提交
        </a-button>
      </template>
      <template>
        <a-form-model
          ref="ruleForm"
          :model="form"
          :rules="rules"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          :layout="form.layout"
        >
        <a-row :gutter="16">
          <a-col :span="10">
            <a-form-model-item ref="account" label="用户名" prop="account">
              <a-input v-model="form.account" />
            </a-form-model-item>
          </a-col>
          <a-col :span="10">
            <a-form-model-item ref="name" label="姓名" prop="name">
              <a-input v-model="form.name" />
            </a-form-model-item>
          </a-col>
        </a-row>
        <a-row :gutter="16">
          <a-col :span="10">
            <a-form-model-item label="性别" prop="gender">
            <a-select v-model="form.gender" placeholder="请选择性别">
              <a-select-option v-for="item in genderlist" :key="item[0]" :value="item[1]">
                {{item[0]}}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          </a-col>
          <a-col :span="10">
            <a-form-model-item label="部门" prop="department">
            <a-select v-model="form.department" placeholder="请选择部门">
              <a-select-option v-for="item in departmentoptions" :key="item['department']" :value="item['id']">
                {{item['department']}}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          </a-col>
        </a-row>
        <a-row :gutter="16">
          <a-col :span="10">
            <a-form-model-item label="角色" prop="role">
            <a-select v-model="form.role" placeholder="请选择角色">
              <a-select-option v-for="item in ruleslist" :key="item.role" :value="item.id">
                {{item.role}}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          </a-col>
          <a-col :span="10">
            <a-form-model-item label="入职时间" prop="entry_time">
            <a-date-picker v-model="form.entry_time" style="width: 100%" :value-format="dateFormat" placeholder="请选择入职时间" />
          </a-form-model-item>
          </a-col>
        </a-row>
        <a-row :gutter="16">
          <a-col :span="10">
            <a-form-model-item ref="phone" label="联系电话" prop="phone">
              <a-input v-model="form.phone" />
            </a-form-model-item>
          </a-col>
          <a-col :span="10">
            <a-form-model-item ref="address" label="联系地址" prop="address">
              <a-input v-model="form.address" />
            </a-form-model-item>
          </a-col>
        </a-row>
        <a-row :gutter="16">
          <a-col :span="10">
            <a-form-model-item label="出生日期" prop="birth">
            <a-date-picker v-model="form.birth" style="width: 100%" :value-format="dateFormat" placeholder="请选择出生日期" />
          </a-form-model-item>
          </a-col>
          <a-col :span="10">
            <a-form-model-item ref="account" label="创建人" prop="creator">
              <a-input v-model="form.creator" />
            </a-form-model-item>
          </a-col>
        </a-row>
        <div>小提示：</div>
        <div>1.用户名一旦创建成功，则无法修改用户名。</div>
        <div>2.所有用户的初始密码为123456，创建成功后请尽快修改密码。</div>
        </a-form-model>
      </template>
    </a-modal>
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
import {UsersDate} from '@/services/personnelmanagement'
import {
  DeleteUsers,
  DepartmentDate,
  RolesDate,
  RolesResetPassword,
  UsersAdd
} from "../../../services/personnelmanagement";
const columns = [
  {
    title: '序号',
    dataIndex: 'index'
  },
  {
    title: '用户名',
    dataIndex: 'account'
  },
  {
    title: '姓名',
    dataIndex: 'name',
  },
  {
    title: '性别',
    dataIndex: 'gender',
  },
  // {
  //   title: '部门',
  //   dataIndex: '',
  // },

  {
    title: '入职时间',
    dataIndex: 'entry_time'
  },
  {
    title: '电话',
    dataIndex: 'phone'
  },
  {
    title: '创建人',
    dataIndex: 'creator'
  },
  {
    title: '操作',
    scopedSlots: { customRender: 'action' }
  }
]

const dataSource = []

for (let i = 0; i < 100; i++) {
  dataSource.push({
    key: i,
    ne: 'NO ' + i,
    description: '这是一段描述',
    callNo: Math.floor(Math.random() * 1000),
    status: Math.floor(Math.random() * 10) % 4,
    updatedAt: '2018-07-26'
  })
}

export default {
  name: 'QueryList',
  components: {StandardTable},
  data () {
    return {
      dateFormat: 'YYYY-MM-DD',
      query: {
        platform: '',
        department: ''
      },
      form: {
        layout: 'vertical',
        account: '',
        name: '',
        department: '',
        gender: '',
        entry_time: '',
        phone: '',
        address: '',
        birth: '',
        creator: '',
        role: ''
      },
      advanced: true,
      columns: columns,
      dataSource: dataSource,
      selectedRows: [],
      ids: [],
      departmentoptions: [{id:"0",department:'商务部'}, {id:"1",department:"技术部"}],
      roleoptions: ['商务', "技术"],
      genderlist: [['男', "true"], ["女", "false"]],
      ruleslist: [{id: "0", role: '商务专员'}, {id: "1", role: "技术专员"}],
      dialogvisible: false,
      tablename: '',
      visible: false,
      loading: false,
      rules: {
        filename: [{ required: true, message: '请输入文件名', trigger: 'blur' }],
        department: [{ required: true, message: '请选择部门', trigger: 'change' }],
        desc: [{ required: false, message: 'Please input activity form', trigger: 'blur' }],
      }
    }
  },
  created () {
    this.gettabledata()
    this.getdepartmentoptions()
  },
  methods: {
    //获取部门列表和角色列表
    getdepartmentoptions(){
      DepartmentDate().then(res => {
        this.departmentoptions = res.data.data
      })
      RolesDate().then(res => {
        this.ruleslist = res.data.data
      })
    },
    // 获取表格数据
    gettabledata () {
      UsersDate(this.query).then(res => {
        var re_da = res.data.data;
        // 给予序号
        for (var i = 0; i < re_da.length; i++) {
          // re_da[i]["time"] = re_da[i]["time"].split(" ")[0];
          re_da[i]["index"] = i + 1
        }
        this.dataSource = re_da
      })
    },
    async user_onok() {
      // let is_logic_del = '0'
      // console.log(this.ids)
      for (let i = 0; i < this.ids.length; i++) {
        await DeleteUsers(this.ids[i]).then(res => {
          console.log(res);
          })
      }
      this.gettabledata()
      this.ids = []
      this.dialogvisible = false
    },
    async user_onno() {
      this.ids = []
      this.dialogvisible = false
    },
    toggleAdvanced () {
      this.advanced = !this.advanced
    },
    remove () {
      this.dataSource = this.dataSource.filter(item => this.selectedRows.findIndex(row => row.key === item.key) === -1);
      this.selectedRows = []
    },
    onClear() {
      this.$message.info('您清空了勾选的所有行')
    },
    onStatusTitleClick() {
      this.$message.info('你点击了状态栏表头')
    },
    onChange() {
      this.$message.info('表格状态改变了')
    },
    handleMenuClick (e) {
      if (e.key === 'delete') {
        this.remove()
      }
    },
    // 查询
    queryevents() {
      console.log(this.query);
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
    // 打开编辑表单
    showModal(id) {
      typeof id === 'number' ? this.tablename = '编辑' : this.tablename = '新增'
      console.log(id);
      this.visible = true;
    },
    // 重置密码
    resetPassword(id) {
      RolesResetPassword({"id":id, "password": "123456"}).then(res => {
        console.log("重置密码成功")
        console.log(res)
        // 提示框





      })
    },
    // 提交编辑表单
    handleOk() {
      this.$refs.ruleForm.validate(valid => {
        if (valid) {
          console.log(valid)
          this.loading = true;
          console.log('ok');
          UsersAdd(this.form).then(res => {
            console.log(res)
          })
          this.gettabledata()
          this.visible = false;
        }
      })
    },
    // 关闭编辑表单
    handleCancel() {
      this.visible = false;
      this.$refs.ruleForm.resetFields();
      console.log('ok');
    },
    // 删除对话框
    showdeleConfirm(id) {
      this.ids.push(id)
      this.dialogvisible = true
    }
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
