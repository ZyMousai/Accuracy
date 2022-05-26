<template>
  <a-card>
    <div :class="advanced ? 'search' : null">
      <a-form layout="horizontal" :model="query">
        <div :class="advanced ? null: 'fold'">
          <a-row >
            <a-col :md="8" :sm="24" >
              <a-form-item
                label="联盟"
                :labelCol="{span: 5}"
                :wrapperCol="{span: 18, offset: 1}"
              >
                <a-select
                    v-model="query.union_id"
                    placeholder="请选择"
                    :allowClear="true"
                    :showSearch="true"
                    :filter-option ="filterOption"
                >
                  <a-select-option v-for="item in unionnamesystem" :key="item.id" :value="item.id">
                    {{item.union_name}}
                  </a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :md="8" :sm="24" >
              <a-form-item
                label="账号"
                :labelCol="{span: 5}"
                :wrapperCol="{span: 18, offset: 1}"
              >
                <a-input v-model="query.offers_account" placeholder="账号"  :allowClear="true"/>
              </a-form-item>
            </a-col>
          </a-row>
          <a-row v-if="advanced">
            <a-col :md="8" :sm="24" >
              <a-form-item
                label="开始日期"
                :labelCol="{span: 5}"
                :wrapperCol="{span: 18, offset: 1}"
              >
                <a-date-picker v-model="start_time" style="width: 100%" placeholder="请输入开始时间" format="YYYY-MM-DD"/>
              </a-form-item>
            </a-col>
            <a-col :md="8" :sm="24" >
              <a-form-item
                label="结束日期"
                :labelCol="{span: 5}"
                :wrapperCol="{span: 18, offset: 1}"
              >
                <a-date-picker v-model="end_time" style="width: 100%" placeholder="请输入结束时间" format="YYYY-MM-DD" />
              </a-form-item>
            </a-col>
            <a-col :md="8" :sm="24">
              <a-form-item
                label="状态"
                :labelCol="{ span: 5 }"
                :wrapperCol="{ span: 18, offset: 1 }"
              >
                <a-select v-model="query.state" placeholder="请选择" :allowClear="true">
                  <a-select-option
                    v-for="item in state_select"
                    :key="item[1]"
                    :value="item[1]"
                  >
                    {{ item[0] }}
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
      <a-button type="primary" @click="showModal">
        <a-icon type="plus-circle" />新增
      </a-button>
      <a-table
        :columns="columns"
        :data-source="dataSource"
        :selectedRows.sync="selectedRows"
        :rowKey='record=>record.id'
        :loading="tableloading"
        :pagination="false"
      >
        <div slot="action" slot-scope="record">
          <a @click="showModal(record)" style="margin-right: 8px">
            <a-icon type="edit"/>修改
          </a>
          <a @click="deletedialog(record.id)">
            <a-icon type="delete" />删除
          </a>
        </div>
        <div slot="status" slot-scope="record">
          <a-switch slot="status" :loading="record.status_loading" default-checked
                    :checked="record.status ? true : false"
                    @change="record.status_loading=true;status_change(record.status, record.id)"/>
        </div>
        <!--                    :checked="record.status ? true : false"-->
      </a-table>
      <a-pagination
        style="margin-top: 15px;"
        v-model="query.page"
        :total="total"
        show-size-changer
        @showSizeChange="onShowSizeChange"
        :show-total="total => `一共 ${total} 条`"
        @change="pageonChange" />
      <!-- 编辑表单 -->
      <a-modal v-model="visible" :title="tablename" on-ok="handleOk" :maskClosable="false" @afterClose="closeform()">
      <template slot="footer">
        <a-button key="back" @click="closeform">
          取消
        </a-button>
        <a-button key="submit" type="primary" :loading="loading" @click="submitform">
          提交
        </a-button>
      </template>
      <template>
        <a-form-model
          ref="ruleForm"
          :model="editform"
          :rules="editrules"
          :label-col="{ span: 4 }"
          :wrapper-col="{ span: 14 }"
        >
<!--          <a-form-model-item ref="union_id" label="联盟名" prop="union_name">-->
<!--            <a-input v-model="editform.union_name" />-->
<!--          </a-form-model-item>-->
          <a-form-model-item label="联盟名" prop="union_id">
            <a-select v-model="editform.union_id" placeholder="请选择" :allowClear="true">
              <a-select-option v-for="item in unionnamesystem" :key="item.id" :value="item.id">
                {{item.union_name}}
              </a-select-option>
            </a-select>
          </a-form-model-item>

          <a-form-model-item ref="offers_account" label="账号" prop="offers_account">
            <a-input v-model="editform.offers_account" />
          </a-form-model-item>

          <a-form-model-item ref="offers_pwd" label="密码" prop="offers_pwd">
            <a-input v-model="editform.offers_pwd" type="password"/>
          </a-form-model-item>

          <a-form-model-item ref="offers_api_key" label="api-key" prop="offers_api_key">
            <a-input v-model="editform.offers_api_key" />
          </a-form-model-item>

          <a-form-model-item ref="ip_info_state" label="ip国家" prop="ip_info_state">
            <a-input v-model="editform.ip_info_state" />
          </a-form-model-item>
          <a-form-model-item ref="ip_info_country" label="ip洲或地区" prop="ip_info_country">
            <a-input v-model="editform.ip_info_country" />
          </a-form-model-item>
          <a-form-model-item label="options">
            <a-space
              v-for="(user, index) in editform.users"
              :key="user.id"
              style="display: flex; margin-bottom: 0px;align-items: center;"
              align="baseline"
            >
              <a-form-item
                :name="['users', index, 'key']"
                :rules="{
                  required: true,
                  message: 'Missing key',
                }"
              >
                <a-input v-model="user.key" placeholder="key" />
              </a-form-item>
              <a-form-item
                :name="['users', index, 'value']"
                :rules="{
                  required: true,
                  message: 'Missing value',
                }"
              >
                <a-input v-model="user.value" placeholder="value" />
              </a-form-item>
                <a-button @click="removeUser(user)" style="margin-bottom: 24px;">删除</a-button>
            </a-space>
          </a-form-model-item>
          <a-form-item>
            <a-button type="dashed" block @click="addUser">
              Add Option
            </a-button>
          </a-form-item>
        </a-form-model>
      </template>
    </a-modal>
    <!-- 删除确认对话框 -->
    <a-modal
     title="系统消息"
     :visible="dialogvisible"
     :closable="false"
     @icon="oncancel"
     :footer="modalfooter"
    >
      <p>是否删除</p>
    </a-modal>
    </div>
  </a-card>
</template>

<script>
import Cookie from 'js-cookie'
import {
  OffersAccountAdd,
  OffersAccountDate,
  OffersAccountDelete,
  OffersAccountEdit
} from "../../../services/offersaccount";
import {OffersUnionDateAll} from "../../../services/offersunion";

const columns = [
  // {
  //   title: '序号',
  //   dataIndex: 'index',
  //   width: 80
  // },
  {
    title: 'id',
    dataIndex: 'index',
  },
  {
    title: '联盟名',
    dataIndex: 'union_name'
  },
  {
    title: '账号',
    dataIndex: 'offers_account'
  },
  {
    title: '密码',
    dataIndex: 'offers_pwd_mi'
  },
  {
    title: 'api-key',
    dataIndex: 'offers_api_key'
  },
  {
    title: '创建时间',
    dataIndex: 'create_time'
  },
  {
    title: '状态',
    key: 'status',
    scopedSlots: {customRender: 'status'}
  },
  {
    title: '操作',
    scopedSlots: { customRender: 'action' }
  }
]

const dataSource = []

export default {
  name: 'QueryList',
  data () {
    return {
      query: {
        page: 1,
        page_size: 10,
        union_id: null,
        status: null,
        offers_account: null,
        start_time: null,
        end_time: null,
      },
      total: 0,
      editform: {
        id: '',
        status: null,
        union_id: null,
        offers_account: null,
        offers_pwd: null,
        offers_api_key: null,
        options: null,
        ip_info: null,
        ip_info_state: "",
        ip_info_country: "",
        users:[],
      },
      state_select: [
        ["开启", 0],
        ["关闭", 1],
      ],
      advanced: true,
      columns: columns,
      dataSource: dataSource,
      updocuurl: '',
      selectedRows: [],
      ids: [],
      visible: false,
      loading: false,
      start_time: '',
      end_time: '',
      role_id: '',
      tablename: "",
      dialogvisible: false,
      unionnamesystem: [],
      unionnamesystem_search: [],
      editrules: {
        union_name: [{ required: true, message: '请输入联盟名', trigger: 'blur' }],
        union_system_id: [{ required: true, message: '请选择追踪系统列表', trigger: 'change' }]
      },
      tableloading: false,
      alone: '',
      headers: {
        accept: 'application/json',
        authorization: 'authorization-text',
        token: Cookie.get('Authorization')
      },
    }
  },
  created () {
    this.getunionnamesystem()
  },
  methods: {
    removeUser(item){
      let index = this.editform.users.indexOf(item);
      if (index !== -1) {
        this.editform.users.splice(index, 1);
      }
    },
    addUser() {
      this.editform.users.push({key: '', value: ''});
    },
    //获取追踪系统列表
    getunionnamesystem(){
      OffersUnionDateAll().then(res => {
        if (res.status === 200) {
          this.unionnamesystem = res.data.data
          this.gettabledata()
        } else {
          this.$message.error('获取联盟列表失败！')
        }
      })
    },
    // 获取表格数据
    gettabledata () {
      this.alone = process.env.VUE_APP_API_ALONE_URL
      this.tableloading = true
      OffersAccountDate(this.query).then(res => {
        if (res.status === 200) {
          console.log(res);
          var reg = /(.*)(.)$/;
          var re_da = res.data.data;
          // 给予序号
          for (var i = 0; i < re_da.length; i++) {
            re_da[i]["index"] = i + 1
            re_da[i]["status_loading"] = false
            re_da[i]["offers_pwd_mi"] = re_da[i]["offers_pwd"].replace(reg,function(a,b){
                return b.replace(/./g,"*") + "*";
            });
          }
          this.dataSource = re_da
          this.total = res.data.total
          this.tableloading = false
          // for (var i = 0; i < this.dataSource.length; i++) {
          //   this.dataSource[i]["index"] = i + 1
          //   this.dataSource[i]["file_url"] = this.alone + '/DocumentManagement/documents/v1/download/' + this.dataSource[i].filename
          // }
          console.log(this.dataSource);
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
      console.log(this.query)
      this.query.page = 1
      this.query.page_size = 10
      this.query.start_time = this.start_time ? this.start_time.format('YYYY-MM-DD') : null
      this.query.end_time = this.end_time ? this.end_time.format('YYYY-MM-DD') : null
      this.gettabledata()
    },
    // 批量删除
    Batchdelete() {
      this.dialogvisible = true
      console.log(this.selectedRows);
      for (let i = 0; i < this.selectedRows.length; i++) {
        this.ids.push(this.selectedRows[i].id)
      }
    },
    // 重置查询表单
    resettingqueryform() {
      for(var key in this.query) {
        this.query[key] = null
      }
      this.query.page = '1'
      this.query.page_size = '10'
      // this.query.union_system_id = localStorage.getItem('union_system_id') - ''
      this.gettabledata()
    },
    // 打开编辑表单
    showModal(data) {
      if (data.id) {
        this.tablename = "编辑";
        this.isdisabled = true;
        console.log(data);
        this.editform.id = data.id
        this.editform.status = data.status
        this.editform.union_id = data.union_id
        this.editform.offers_account = data.offers_account
        this.editform.offers_pwd = data.offers_pwd
        this.editform.offers_api_key = data.offers_api_key

        this.editform.ip_info_state = data.ip_info["state"]
        this.editform.ip_info_country = data.ip_info["nation"]

        this.editform.options = data.options
        this.editform.users = []
        for(var da_k in data.options){
          this.editform.users.push({
            key: da_k,
            value: data.options[da_k],
          });
        }
        this.visible = true;
        console.log(this.editform);
      }else {
        this.tablename = "新增";
        this.isdisabled = false;
      }
      this.visible = true;
    },
    // 提交编辑表单
    submitform() {
      this.$refs.ruleForm.validate(valid => {
        if (valid) {
          this.loading = true;
          var dick_options = {}
          this.editform.users.forEach(e => {
            dick_options[e.key] = e.value
          })
          this.editform.options = dick_options
          this.editform.ip_info = {
            "state": this.editform.ip_info_state,
            "nation": this.editform.ip_info_country
          }
          if (this.tablename === "新增"){
            this.editform.status = 1
            OffersAccountAdd(this.editform).then(res => {
              if (res.status === 200) {
                this.$message.success(`新增成功！`);
              } else {
                this.$message.error(`新增失败！`);
              }
              this.loading = false;
              this.visible = false;
              this.gettabledata()
            })
          }else {
            OffersAccountEdit(this.editform).then(res => {
              if (res.status === 200) {
                this.$message.success(`编辑成功！`);
              } else {
                this.$message.error(`编辑失败！`);
              }
              this.loading = false;
              this.visible = false;
              this.gettabledata()
            })
          }
        }
      })
    },
    // 关闭编辑表单
    closeform() {
      this.visible = false;
      this.$refs.ruleForm.resetFields();
    },
    deletedialog(id) {
      this.ids.push(id)
      this.dialogvisible = true
    },
    async onok() {
      for (let i = 0; i < this.ids.length; i++) {
        await OffersAccountDelete(this.ids[i]).then(res => {
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
      this.gettabledata();
      this.ids = [];
      this.dialogvisible = false
    },
    canceldelete() {
      this.ids = [];
      this.dialogvisible = false
    },
    async oncancel() {
      this.dialogvisible = false
    },
    // 自定义删除对话框底部按钮
    modalfooter() {
      return (
        <div>
          <a-button onClick={this.onok}  type="primary">是</a-button>
          <a-button onClick={this.canceldelete}>取消</a-button>
        </div>
      )
    },
    // <a-button onClick={this.onno}  type="danger">直接删除</a-button>

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
    status_change(status, id) {
      console.log("id");
      console.log(id);
      console.log("id");
      // id.loadingchanr = true
      OffersAccountEdit({status: status ? 0 : 1, id: id}).then(res => {
        console.log("成功")
        console.log(res)
        this.gettabledata()
      })
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
