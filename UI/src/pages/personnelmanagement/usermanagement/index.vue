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
              <a-input v-model="query.name" placeholder="请输入" />
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="角色"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-select v-model="query.role_id" placeholder="请选择">
                <a-select-option v-for="item in ruleslist" :key="item.role" :value="item.id">
                  {{item.role}}
                </a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="部门"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-select v-model="query.department_id" placeholder="请选择">
                <a-select-option v-for="item in departmentoptions" :key="item.id" :value="item.id">
                  {{item.department}}
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
        :loading="tableloading"
        :pagination="false"
      >
      <span slot="gender"  slot-scope="{record}">
        {{ record.gender ? '男' : '女' }}
      </span>
        <div slot="action" slot-scope="{record}">
          <a @click="modifypermissions(record.id)" style="margin-right: 8px">
            <a-icon type="usergroup-delete" />修改权限
          </a>
          <a @click="showModal(record)" style="margin-right: 8px">
            <a-icon type="edit"/>修改信息
          </a>
          <a-popconfirm
            title="你确定要重置密码吗？"
            ok-text="是"
            cancel-text="否"
            @confirm="resetPassword(record.id)"
            >
            <a style="margin-right: 8px">
              <a-icon type="retweet" />重置密码
            </a>
          </a-popconfirm>
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
          layout="vertical"
        >
        <a-row :gutter="16">
          <a-col :span="10">
            <a-form-model-item ref="account" label="用户名" prop="account">
              <a-input v-model="form.account" :disabled="isdisabled" />
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
            <a-form-model-item label="入职时间" prop="entry_time">
              <a-date-picker v-model="form.entry_time" style="width: 100%" :value-format="dateFormat" placeholder="请选择入职时间" />
            </a-form-model-item>
          </a-col>
        </a-row>
        <a-row :gutter="16" v-if="this.tablename === '新增'">
          <a-col :span="10">
            <a-form-model-item label="角色" prop="role_id">
            <a-select v-model="form.role_id" placeholder="请选择角色">
              <a-select-option v-for="item in ruleslist" :key="item.role" :value="item.id">
                {{item.role}}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          </a-col>
          <a-col :span="10">
            <a-form-model-item label="出生日期" prop="birth">
            <a-date-picker v-model="form.birth" style="width: 100%" :value-format="dateFormat" placeholder="请选择出生日期" />
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
        </a-row>
        <div>小提示：</div>
        <div>1.用户名一旦创建成功，则无法修改用户名。</div>
        <div>2.所有用户的初始密码为123456，创建成功后请尽快修改密码。</div>
        </a-form-model>
      </template>
      </a-modal>
      <!-- 权限修改表单 -->
      <a-modal v-model="permissionsvisible" :title="tablename" on-ok="permissionsOkhandleOk" :maskClosable="false" @afterClose="permissionshandleCancel()" :width='850'>
      <template slot="footer">
        <a-button key="back" @click="permissionshandleCancel">
          取消
        </a-button>
        <a-button key="submit" type="primary" :loading="permissionsloading" @click="permissionsOkhandleOk">
          提交
        </a-button>
      </template>
      <template>
        <a-form-model
          ref="permissionsruleForm"
          :model="permissionsform"
          :rules="permissionsrules"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          layout="vertical"
        >
        <a-row :gutter="16">
          <a-col :span="10">
            <a-form-model-item label="角色" prop="role_id">
            <a-select v-model="permissionsform.role_id" placeholder="请选择角色">
              <a-select-option v-for="item in ruleslist" :key="item.role" :value="item.id">
                {{item.role}}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          </a-col>
        </a-row>
        </a-form-model>
      </template>
      </a-modal>
    </div>
    <!-- 删除确认对话框 -->
    <a-modal
     title="系统消息"
     :visible="dialogvisible"
     ok-text="是"
     cancel-text="否"
     @ok="user_onok"
     @cancel="user_onno">
      <p>是否删除所选用户，删除后将无法恢复！</p>
    </a-modal>
  </a-card>
</template>

<script>
import StandardTable from '@/components/table/StandardTable'
import {UsersDate, DeleteUsers, RolesDate, RolesResetPassword, UsersAdd, GetOneUsersDate, UsersEdit, UsersAddRole, UsersDeleteRole, DepartmentDate} from '@/services/personnelmanagement'
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
    key: 'gender',
    slots: { title: 'genderTitle' },
    scopedSlots: { customRender: 'gender' },
  },
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

export default {
  name: 'QueryList',
  components: {StandardTable},
  data () {
    var checkMobile = (rule, value, cb) => {
      console.log(value);
      const regMobile = /^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/;
      if (regMobile.test(value)) {
          // 合法的手机号码
          return cb() 
      }
      cb(new Error('手机号码格式不正确'))
    }
    return {
      dateFormat: 'YYYY-MM-DD',
      query: {
        page: 1,
        page_size: 10,
        name: null,
        department_id: null,
        role_id: null
      },
      form: {
        account: '',
        role_id: '',
        department_id: '',
        name: '',
        gender: null,
        birth: '',
        phone: '',
        address: ''
      },
      total: 0,
      advanced: true,
      columns: columns,
      dataSource: dataSource,
      selectedRows: [],
      ids: [],
      tableloading: false,
      genderlist: [['男', "true"], ["女", "false"]],
      ruleslist: [],
      departmentoptions: [],
      dialogvisible: false,
      tablename: '',
      visible: false,
      loading: false,
      userid: '',
      permissionsloading: false,
      permissionsvisible: false,
      isdisabled: false,
      permissionsform: {
        role_id: '',
        department_id: ''
      },
      repermissionsform: {
        role_id: '',
        department_id: ''
      },
      permissionsrules: {
        department_id: [{ required: true, message: '请选择部门', trigger: 'change' }],
        role_id: [{ required: true, message: '请选择角色', trigger: 'change' }],
      },
      rules: {
        account: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
        gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
        department_id: [{ required: true, message: '请选择部门', trigger: 'change' }],
        role_id: [{ required: true, message: '请选择角色', trigger: 'change' }],
        entry_time: [{ required: true, message: '请选择入职时间', trigger: 'change' }],
        phone: [{ required: true, message: '请填写手机号', trigger: 'blur' },
                  { validator: checkMobile, rtigger:'blur'  }],
        address: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        birth: [{ required: true, message: '请选择入职时间', trigger: 'change' }],
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
      RolesDate().then(res => {
        if (res.status === 200) {
          this.ruleslist = res.data.data
        } else {
          this.$message.error('获取角色列表失败！')
        }
      })
      DepartmentDate().then(res => {
        if (res.status === 200) {
          this.departmentoptions = res.data.data
        } else {
          this.$message.error('获取部门列表失败！')
        }
      })
    },
    // 获取表格数据
    gettabledata () {
      this.tableloading = true
      UsersDate(this.query).then(res => {
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
    async user_onok() {
      for (let i = 0; i < this.ids.length; i++) {
        await DeleteUsers(this.ids[i]).then(res => {
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
        this.query[key] = null
      }
      this.query.page = 1
      this.query.page_size = 10
      this.gettabledata()
    },
    // 打开编辑表单
    showModal(data) {
      this.form = {}
      if (data.id) {
        this.tablename = '编辑'
        this.isdisabled = true
        GetOneUsersDate(data.id).then(res => {
          this.form = res.data.data
          this.userid = this.form.id
          this.ruleslist.forEach(i => {
            if (i.role === this.form.users_role) {
              this.form.role_id = i.id
              return
            }
          })
          this.form.gender = this.form.gender + ''
          this.visible = true;
        })
      } else {
        this.tablename = '新增'
        this.isdisabled = false
        this.visible = true;
      }
    },
    // 重置密码
    resetPassword(id) {
      RolesResetPassword({"id":id, "password": "123456"}).then(res => {
        if (res.status === 200) {
          this.$message.success(`重置成功！`);
        } else {
          this.$message.error(`重置失败！`);
        }
      })
    },
    // 提交编辑表单
    handleOk() {
      this.$refs.ruleForm.validate(valid => {
        if (valid) {
          this.form.creator = localStorage.getItem('name')
          this.loading = true;
          this.tablename === '新增' ? this.addadta() : this.ediddata()
        }
      })
    },
    addadta() {
      UsersAdd(this.form).then(res => {
        if (res.status === 200) {
          this.userid = res.data.id
          this.adduserrole(this.form)
        } else {
          this.$message.error(`${this.tablename}失败！`);
          this.loading = false;
        }
      })
    },
    ediddata() {
      UsersEdit(this.form).then(res => {
        if (res.status === 200) {
          this.$message.success(`${this.tablename}成功！`);
          this.gettabledata()
          this.loading = false;
          this.visible = false;
        } else {
          this.$message.error(`${this.tablename}失败！`);
          this.loading = false;
        }
      })
    },
    // 修改用户权限
    modifypermissions(data) {
      this.tablename = '修改'
      this.permissionsvisible = true
      this.userid = data
      GetOneUsersDate(data).then(res => {
        this.ruleslist.forEach(i => {
          if (i.role === res.data.data.users_role) {
            this.repermissionsform.role_id = i.id
            this.permissionsform.role_id = i.id
            return
          }
        })
      })
    },
    // 提交权限编辑表单
    permissionsOkhandleOk() {
      this.$refs.permissionsruleForm.validate(valid => {
        if (valid) {
          this.deleteuserrole(this.repermissionsform)
        }
      })
    },
    // 关闭权限编辑表单
    permissionshandleCancel() {
      this.permissionsvisible = false
      this.$refs.permissionsruleForm.resetFields();
    },
    // 添加用户关联角色
    adduserrole(data) {
      const form = {
        role_id: data.role_id,
        ids: []
      }
      form.ids.push(this.userid)
      UsersAddRole(form).then(res => {
        if (res.status === 200) {
          this.$message.success(`角色${this.tablename}成功！`);
          this.loading = true;
          this.visible = false;
          this.permissionsloading = false
          this.permissionsvisible = false
          this.gettabledata()
        } else {
          this.$message.error(`角色${this.tablename}失败！`);
          this.permissionsloading = false
          this.loading = false;
        }
      })
    },
    // 删除用户关联角色
    deleteuserrole(data) {
      const form = {
        role_id: data.role_id,
        ids: []
      }
      this.permissionsloading = true
      form.ids.push(this.userid)
      UsersDeleteRole(form).then(res => {
        if (res.status === 200) {
          this.adduserrole(this.permissionsform)
        } else {
          this.$message.error(`${this.tablename}失败！`);
          this.permissionsloading = false
          this.loading = false;
        }
      })
    },
    // 关闭编辑表单
    handleCancel() {
      this.visible = false;
      this.$refs.ruleForm.resetFields();
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
