<template>
  <a-card>
    <div :class="advanced ? 'search' : null">
      <a-form layout="horizontal" :model="query">
        <div :class="advanced ? null: 'fold'">
          <a-row >
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="平台"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-input v-model="query.platform" placeholder="请输入" />
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="账号"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-input v-model="query.account" style="width: 100%" placeholder="请输入" />
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
        :loading="tableloading"
        :pagination="false"
        :rowKey='record=>record.id'
      >
        <div slot="password" slot-scope="{record}">
          {{record.password}}
          <a-button type="link" @click="showPassword(record)" style="padding: 0 5px 0;" :disabled="record.isciphertext ? false : true">
            <a-icon type="sync" /><span style="margin: 0;">解密</span>
          </a-button>
          <a-button type="link" @click="hidePassword(record)" style="padding: 0 5px 0" :disabled="record.isciphertext ? true : false">
            <a-icon type="sync" /><span style="margin: 0;">加密</span>
          </a-button>
        </div>
        <div slot="action" slot-scope="{record}">
          <a @click="showModal(record)" style="margin-right: 8px">
            <a-icon type="edit"/>修改
          </a>
          <a @click="DeleteDate(record.id)">
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
        <a-button key="back" @click="handleCancel()">
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
            <a-form-model-item ref="platform" label="平台" prop="platform">
              <a-input v-model="form.platform" />
            </a-form-model-item>
          </a-col>
          <a-col :span="10">
            <a-form-model-item ref="account" label="账号" prop="account">
              <a-input v-model="form.account" />
            </a-form-model-item>
          </a-col>
        </a-row>
        <a-row :gutter="16">
          <a-col :span="10">
            <a-form-model-item ref="password" label="密码" prop="password">
            <a-input v-model="form.password" />
          </a-form-model-item>
          </a-col>
          <a-col :span="10">
            <a-form-model-item label="权限角色" prop="role_id">
            <a-select v-model="reform.role_id" placeholder="请选择角色">
              <a-select-option v-for="item in departmentoptions" :key="item.id" :value="item.id">
                {{item.role}}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          </a-col>
        </a-row>
        <a-row>
          <a-col>
            <a-form-model-item label="备注" prop="remark" :labelCol="{span: 2}" :wrapperCol="{span: 18}">
            <a-input v-model="form.remark" type="textarea" />
          </a-form-model-item>
          </a-col>
        </a-row>
        </a-form-model>
      </template>
    </a-modal>
    <!-- 删除确认对话框 -->
    <a-modal
     title="系统消息"
     :visible="dialogvisible"
     ok-text="是"
     cancel-text="否"
     @ok="onok"
     @cancel="onno">
      <p>删除后将无法恢复！</p>
    </a-modal>
    </div>
  </a-card>
</template>

<script>
import StandardTable from '@/components/table/StandardTable'
import CryptoJS from 'crypto-js/crypto-js'
import {AccountDate, GetDownmenutDate, AddAccount, GetOngAccountDate, DeleteDate, EditAccount, AddAccountRole, DeleteAccountRole} from '@/services/accountmanagement'
const columns = [
  {
    title: '序号',
    dataIndex: 'index',
    width: 80
  },
  {
    title: '平台',
    dataIndex: 'platform'
  },
  {
    title: '账号',
    dataIndex: 'account'
  },
  {
    title: '密码',
    dataIndex: 'password',
    width: 800,
    scopedSlots: { customRender: 'password' }
  },
  {
    title: '备注',
    dataIndex: 'remark'
  },
  {
    title: '操作',
    scopedSlots: { customRender: 'action' }
  }
]

const dataSource = []

const KEY = CryptoJS.enc.Utf8.parse(" ");
const IV = CryptoJS.enc.Utf8.parse(" ");

export default {
  name: 'QueryList',
  components: {StandardTable},
  data () {
    return {
      query: {
        page: 1,
        page_size: 10,
        account: '',
        platform: ''
      },
      form: {
        account: '',
        platform: '',
        remark: '',
        role_id: [],
        password: ''
      },
      reform: {
        role_id: ""
      },
      KEY: KEY,
      IV: IV,
      total: 0,
      advanced: true,
      columns: columns,
      dataSource: dataSource,
      selectedRows: [],
      departmentoptions: [],
      tablename: '',
      visible: false,
      loading: false,
      tableloading: false,
      dialogvisible: false,
      accountid: '',
      ids: [],
      rules: {
        platform: [{ required: true, message: '请输入平台', trigger: 'blur' }],
        account: [{ required: true, message: '请输入账号', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
        role_id: [{ required: true, message: '请选择角色', trigger: 'change' }],
        remark: [{ required: false, trigger: 'blur' }],
      }
    }
  },
  created () {
    this.gettabledata()
    this.getdowndata()
  },
  methods: {
    // 获取表格数据
    gettabledata () {
      this.tableloading = true
      AccountDate(this.query).then(res => {
        if (res.status === 200) {
          this.dataSource = res.data.data
          this.total = res.data.total
          this.tableloading = false
          for (var i = 0; i < this.dataSource.length; i++) {
            this.dataSource[i]["index"] = i + 1
            this.dataSource[i]["isciphertext"] = true
          }
        } else {
          this.tableloading = false
          this.$message.error(`获取数据失败！`);
        }
      })
    },
    // 获取角色下拉菜单数据
    getdowndata() {
      GetDownmenutDate().then(res => {
        if (res.status === 200) {
          this.departmentoptions = res.data.data
        } else {
          this.$message.error(`获取角色菜单数据失败！`);
        }
      })
    },
    toggleAdvanced () {
      this.advanced = !this.advanced
    },
    // 查询
    queryevents() {
      this.query.page = 1
      this.query.page_size = 10
      this.gettabledata()
    },
    // 删除对话框
    DeleteDate(id) {
      this.ids.push(id);
      console.log(this.ids);
      this.dialogvisible = true;
    },
    async onok() {
      for (let i = 0; i < this.ids.length; i++) {
        await DeleteDate(this.ids[i]).then(res => {
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
    onno() {
      this.ids = [];
      this.dialogvisible = false
    },
    // 批量删除
    Batchdelete() {
      for (let i = 0; i < this.selectedRows.length; i++) {
        this.ids.push(this.selectedRows[i].id)
      }
      this.deleteaccountrole(this.reform)
      this.dialogvisible = true
    },
    // 重置查询表单
    resettingqueryform() {
      for(var key in this.query) {
        this.query[key] = ''
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
        GetOngAccountDate(data.id).then(res => {
          this.form = res.data.data
          this.form.password = this.Decrypt(this.form.password)
          this.accountid = data.id
          this.visible = true;
        })
      } else {
        this.tablename = '新增'
        this.visible = true;
      }
    },
    // 提交表单
    handleOk() {
      this.$refs.ruleForm.validate(valid => {
        if (valid) {
          this.form.password = this.Encrypt(this.encryption(this.form.password))
          this.loading = true;
          this.tablename === '新增' ? this.addadta() : this.ediddata()
        }
      })
    },
    addadta() {
      AddAccount(this.form).then(res => {
        if (res.status === 200) {
          console.log(res.data.id);
          this.accountid = res.data.id
          this.addaccountrole(this.reform)
        } else {
          this.$message.error(`${this.tablename}失败！`);
        }
        this.loading = false;
        this.visible = false;
        this.gettabledata()
      })
    },
    ediddata() {
      EditAccount(this.form).then(res => {
        if (res.status === 200) {
          this.deleteaccountrole(this.reform)
          this.addaccountrole(this.reform)
        } else {
          this.$message.error(`${this.tablename}失败！`);
        }
        this.loading = false;
        this.visible = false;
        this.gettabledata()
      })
    },
    // 添加用户关联角色
    addaccountrole(data) {
      console.log(data);
      const form = {
        role_id: data.role_id,
        ids: []
      }
      form.ids.push(this.accountid)
      AddAccountRole(form).then(res => {
        if (res.status === 200) {
          this.$message.success(`${this.tablename}成功！`);
          this.loading = false;
          this.accountid = ''
          this.gettabledata()
          this.handleCancel()
        } else {
          this.$message.error(`${this.tablename}失败！`);
          this.loading = false;
        }
      })
    },
    // 删除用户关联角色
    deleteaccountrole(data) {
      const form = {
        role_id: data.role_id,
        ids: []
      }
      form.ids.push(this.accountid)
      DeleteAccountRole(form).then(res => {
        if (res.status === 200) {
          this.addaccountrole(this.form)
        } else {
          this.$message.error(`${this.tablename}失败！`);
          this.loading = false;
        }
      })
    },
    encryption(data) {
      var ciphertext = data
      for (let i = 0; i < 10; i++) {
        ciphertext += '/0'
      }
      return ciphertext
    },
    // 关闭编辑表单
    handleCancel() {
      this.visible = false;
      this.$refs.ruleForm.resetFields();
    },
    // 显示密码
    showPassword(data) {
      console.log(data);
      data.isciphertext = false
      data.password = this.Decrypt(data.password)
    },
    hidePassword(data) {
      console.log(data);
      data.isciphertext = true
      data.password = this.Encrypt(this.encryption(data.password))
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
    // AES加密
    Encrypt(str, keyStr, ivStr) {
      let key = this.KEY
      let iv = this.IV
      
      if (keyStr && ivStr) {
        key = CryptoJS.enc.Utf8.parse(keyStr);
        iv = CryptoJS.enc.Utf8.parse(ivStr);
      }
      let srcs = CryptoJS.enc.Utf8.parse(str);
      var encrypt = CryptoJS.AES.encrypt(srcs, key, {
          iv: iv,
          mode: CryptoJS.mode.CBC,            //这里可以选择AES加密的模式
          padding: CryptoJS.pad.Pkcs7
      });
      return CryptoJS.enc.Base64.stringify(encrypt.ciphertext);
    },
    // AES解密
    Decrypt(str, keyStr, ivStr) {
      let key = KEY
      let iv = IV
      if (keyStr && ivStr) {
          key = CryptoJS.enc.Utf8.parse(keyStr);
          iv = CryptoJS.enc.Utf8.parse(ivStr);
      }
      let base64 = CryptoJS.enc.Base64.parse(str);
      let src = CryptoJS.enc.Base64.stringify(base64);
      var decrypt = CryptoJS.AES.decrypt(src, key, {
          iv: iv,
          mode: CryptoJS.mode.CBC,            //这里可以选择AES解密的模式
          padding: CryptoJS.pad.Pkcs7
      });
      var decryptedStr = decrypt.toString(CryptoJS.enc.Utf8).split('/0')[0];
      return decryptedStr.toString();
    },
    // 搜索框根据显示的内容搜索的组件
    filterOption(input, option){
			return option.componentOptions.children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0;
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