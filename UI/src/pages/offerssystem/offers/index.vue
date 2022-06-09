<template>
  <a-card>
    <div :class="advanced ? 'search' : null">
      <a-form layout="horizontal" :model="query">
        <div :class="advanced ? null: 'fold'">
          <a-row>
            <a-col :md="6" :sm="24" >
              <a-form-item
                label="联盟"
                :labelCol="{span: 5}"
                :wrapperCol="{span: 18, offset: 1}"
              >
                <a-select v-model="query.union_id" placeholder="请选择" :allowClear="true" :showSearch="true"
                    :filter-option ="filterOption">
                  <a-select-option v-for="item in offersalliancesystem" :key="item.id" :value="item.id">
                    {{item.union_name}}
                  </a-select-option>
                </a-select>
              </a-form-item>
            </a-col>




<!--            <a-col :md="6" :sm="24" >-->
<!--              <a-form-item-->
<!--                label="账号"-->
<!--                :labelCol="{span: 5}"-->
<!--                :wrapperCol="{span: 18, offset: 1}"-->
<!--              >-->
<!--                <a-select v-model="query.account_id" placeholder="请选择" :allowClear="true" :showSearch="true"-->
<!--                    :filter-option ="filterOption">-->
<!--                  <a-select-option v-for="item in offersaccountsystem" :key="item.id" :value="item.id">-->
<!--                    {{item.offers_account}}-->
<!--                  </a-select-option>-->
<!--                </a-select>-->
<!--              </a-form-item>-->
<!--            </a-col>-->
            <a-col :md="6" :sm="24" >
              <a-form-item
                label="国家"
                :labelCol="{span: 5}"
                :wrapperCol="{span: 18, offset: 1}"
              >
                <a-input v-model="query.country" placeholder="国家" :allowClear="true"/>
              </a-form-item>
            </a-col>
            <a-col :md="6" :sm="24">
              <a-form-item
                label="任务名"
                :labelCol="{span: 5}"
                :wrapperCol="{span: 18, offset: 1}"
              >
                <a-input v-model="query.offers_name" placeholder="任务名" :allowClear="true"/>
              </a-form-item>
            </a-col>
          </a-row>
          <a-row v-if="advanced">

<!--            <a-col :md="6" :sm="24" >-->
<!--              <a-form-item-->
<!--                label="佣金"-->
<!--                :labelCol="{ span: 5 }"-->
<!--                :wrapperCol="{ span: 18, offset: 1 }"-->
<!--              >-->
<!--                <a-select v-model="query.pay_filter" placeholder="" :allowClear="true" :showSearch="true"-->
<!--                    :filter-option ="filterOption" style="width: 66px;">-->
<!--                  <a-select-option-->
<!--                    v-for="item in ['<','<=','==','>=', '>', '!=']"-->
<!--                    :key="item"-->
<!--                    :value="item"-->
<!--                  >-->
<!--                    {{ item }}-->
<!--                  </a-select-option>-->
<!--                </a-select>-->
<!--                <a-input-number-->
<!--                  v-model="query.pay"-->
<!--                  :value="query.pay"-->
<!--                  :allowClear="true"-->
<!--                />-->
<!--              </a-form-item>-->
<!--            </a-col>-->
            <a-col :md="8" :sm="24">
              <a-form-item
                label="入库时间"
                :labelCol="{ span: 5 }"
                :wrapperCol="{ span: 18, offset: 1 }"
              >
                <a-range-picker
                  format="YYYY-MM-DD HH:mm:ss"
                  :placeholder="['开始日期', '结束日期']"
                  allow-clear
                  @change="bptjTimeChange"
                  :ranges="aranges"
                  v-model='create_time'
                />
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
      <standard-table
        :columns="columns"
        :dataSource="dataSource"
        :rowKey='record=>record.id'
        :loading="tableloading"
        :pagination="false"
      >
<!--        <div slot="action" slot-scope="{record}">-->
<!--          <a @click="showModal(record)" style="margin-right: 8px">-->
<!--            <a-icon type="edit"/>修改-->
<!--          </a>-->
<!--          <a @click="deletedialog(record.id)">-->
<!--            <a-icon type="delete" />删除-->
<!--          </a>-->
<!--        </div>-->
        <div slot="offers_desc" slot-scope="{record}">
          <a-button  :disabled="record.offers_desc_disabled" @click="showModal(record.offers_desc)">查看</a-button>
        </div>
        <div slot="offers_url" slot-scope="{record}">
          <a-button :disabled="record.offers_url_disabled"  @click="register(record.offers_url)">打开</a-button>
          <a-button :disabled="record.offers_url_disabled" v-clipboard:copy="record.offers_url" v-clipboard:success="onCopy" v-clipboard:error="onCopyError">复制</a-button>
        </div>
        <div slot="remark" slot-scope="{record}">
          <a-input v-model="record.remark" style="width: 100%" @blur="remarkEdit(record)"/>
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
      <!-- 编辑表单 -->
      <a-modal v-model="visible" width="66%" :title="tablename" on-ok="handleOk" :maskClosable="false" @afterClose="closeform()">
        <template slot="footer">
          <a-button key="back" @click="closeform">
            取消
          </a-button>
        </template>
        <template>
          <div ref="reportHTML" v-html="htmlText" class="web-con"></div>
        </template>
      </a-modal>
    </div>
  </a-card>
</template>

<script>
// import dayjs from 'dayjs';
import StandardTable from '@/components/table/StandardTable'
import Cookie from 'js-cookie'
import {OffersUnionDateAll} from "../../../services/offersunion";
import {OffersAccountDateAll} from "../../../services/offersaccount";
import {OffersDate, OffersEdit} from "../../../services/offers";
import moment from 'moment'

const columns = [
  // {
  //   title: '序号',
  //   dataIndex: 'index',
  //   width: 80
  // },
  {
    title: '任务ID',
    dataIndex: 'offers_id',
  },
  {
    title: '联盟',
    dataIndex: 'union_name'
  },
  {
    title: '国家',
    dataIndex: 'country'
  },
  {
    title: '任务名',
    dataIndex: 'offers_name'
  },
  {
    title: '入库时间',
    dataIndex: 'create_time'
  },
  {
    title: '任务描述',
    key: 'offers_desc',
    scopedSlots: {customRender: 'offers_desc'}
  },
  {
    title: '佣金',
    dataIndex: 'pay_pay_unit'
  },
  {
    title: 'url',
    key: 'offers_url',
    scopedSlots: {customRender: 'offers_url'}
  },
  {
    title: '备注',
    key: 'remark',
    scopedSlots: {customRender: 'remark'}
  },
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
        union_id: null,
        // account_id: null,
        offers_name: null,
        start_create_time: null,
        end_create_time: null,
        country: null,
      },
      total: 0,
      editform: {
        id: '',
        remark: null,
      },
      dateFormat: "YYYY-MM-DD HH:mm:ss",
      create_time: [null, null],
      // create_time: null,
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
      htmlText: "<h1></h1>",
      dialogvisible: false,
      offersalliancesystem: [],
      offersaccountsystem: [],
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
      bodystyle:{
        width:"66%",
      },
      aranges: {
          '今天': [moment().startOf("day"), moment().endOf('day')],
          '昨天': [moment().subtract(1,'day').startOf("day"), moment().subtract(1,'day').endOf('day')],
          '近一周': [moment().subtract('days', 7).startOf("day"), moment()],
          '近两周': [moment().subtract('days', 14).startOf("day"), moment()],
          '近一个月': [moment().subtract('days', 30).startOf("day"), moment()],
          '近三个月': [moment().subtract('days', 90).startOf("day"), moment()],
          '近半年': [moment().subtract('days', 182).startOf("day"), moment()], // 一年的一半
          '近一年': [moment().subtract('days', 365).startOf("day"), moment()],
          '当月': [moment().startOf('month').startOf("day"), moment()],
          '当季': [moment().startOf('quarter').startOf("day"), moment()],
          '当年': [moment().startOf('year').startOf("day"), moment()],
        },
    }
  },
  created () {
    this.getoffersalliancesystem()
    this.gettabledata()

  },
  methods: {
    //获取联盟列表
    getoffersalliancesystem(){
      OffersUnionDateAll().then(res => {
        if (res.status === 200) {
          console.log(this.roles);
          this.offersalliancesystem = res.data.data
        } else {
          this.$message.error('获取联盟列表失败！')
        }
      })
      //获取账号列表
      OffersAccountDateAll().then(res => {
        if (res.status === 200) {
          console.log(this.roles);
          this.offersaccountsystem = res.data.data
        } else {
          this.$message.error('获取账号列表失败！')
        }
      })
    },
    // 获取表格数据
    gettabledata () {
      this.alone = process.env.VUE_APP_API_ALONE_URL
      this.tableloading = true
      OffersDate(this.query).then(res => {
        if (res.status === 200) {
          console.log(res);
          var re_da = res.data.data;
          // 给予序号
          for (var i = 0; i < re_da.length; i++) {
            re_da[i]["pay_pay_unit"] = re_da[i]["pay"].toString()+" "+re_da[i]["pay_unit"]
            re_da[i]["create_time"] = re_da[i]["create_time"].replace("T", " ");
            re_da[i]["offers_url_disabled"] = re_da[i]["offers_url"] ? false : true
            re_da[i]["offers_desc_disabled"] = re_da[i]["offers_desc"] ? false : true
          }
          this.dataSource = re_da
          this.total = res.data.total
          this.tableloading = false
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
      // this.query.start_time = this.start_time ? this.start_time : null
      // this.query.end_time = this.end_time ? this.end_time : null
      console.log(this.create_time)
      this.gettabledata()
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
    showModal(offers_desc) {
      this.tablename = "任务描述";
      this.isdisabled = true;
      this.htmlText = offers_desc
      console.log(this.editform);
      this.visible = true;
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
    canceldelete() {
      this.ids = [];
      this.dialogvisible = false
    },
    async oncancel() {
      this.dialogvisible = false
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
    register(offers_url){
      window.open(offers_url)
    },
    remarkEdit(data){
      OffersEdit({id: data.id, remark: data.remark}).then(res => {
        if (res.status === 200) {
          this.$message.success(`编辑成功！`);
        } else {
          this.$message.error(`编辑失败！`);
        }
        this.loading = false;
        this.visible = false;
        this.gettabledata()
      })
    },
    // 复制成功时的回调函数
    onCopy () {
     this.$message.success("内容已复制到剪切板！")
    },
    // 复制失败时的回调函数
    onCopyError () {
     this.$message.error("抱歉，复制失败！")
    },
    // 搜索框根据显示的内容搜索的组件
    filterOption(input, option){
			return option.componentOptions.children[0].text.toLowerCase().indexOf(input.toLowerCase()) >= 0;
		},
    // 日期选择
    bptjTimeChange(date, dateString){
      console.log(dateString);
      this.query.start_time = dateString[0] ? dateString[0] : null
      this.query.end_time = dateString[1] ? dateString[1] : null
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
