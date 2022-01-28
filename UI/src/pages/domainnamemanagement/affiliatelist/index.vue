<template>
  <a-card>
    <div :class="advanced ? 'search' : null">
      <a-form layout="horizontal" :model="query">
        <div :class="advanced ? null: 'fold'">
          <a-row >
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="联盟名称或链接"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-input v-model="query.platform" placeholder="请输入" />
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="跟踪域链接"
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
      </a-space>
      <a-table :columns="columns" :data-source="dataSource" class="components-table-demo-nested" >
        <a slot="operation" >编辑</a>
        <a slot="operation" style="margin-left: 5px;">添加跟踪域</a>
        <a slot="operation" style="margin-left: 5px;">删除</a>
        <a-table
          slot="expandedRowRender"
          slot-scope="record"
          :columns="innerColumns"
          :data-source="record.task_ruls"
          :pagination="false"
          :showHeader="false"
        >
          <span slot="operation" class="table-operation">
            <a style="margin-left: 5px;">删除</a>
          </span>
        </a-table>
      </a-table>
      <!-- 父表表单 -->
      <a-modal v-model="subvisible" :title="tablename" on-ok="subhandleOk" :maskClosable="false" @afterClose="handleCancel()" :width='850'>
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
          :label-col="{ span: 3 }"
          :wrapper-col="{ span: 18 }"
          :layout="layout"
          childrenColumnName="track_url"
        >
        <a-row>
          <a-col>
            <a-form-model-item ref="name" label="联盟名称" prop="name">
              <a-input v-model="form.name" />
            </a-form-model-item>
          </a-col>
        </a-row>
        <a-row>
          <a-col>
            <a-form-model-item label="联盟链接" prop="url" :labelCol="{span: 3}" :wrapperCol="{span: 18}">
            <a-input v-model="form.url" type="textarea" />
          </a-form-model-item>
          </a-col>
        </a-row>
        </a-form-model>
      </template>
    </a-modal>
    <!-- 子表表单 -->
    <a-modal v-model="visible" title="添加跟踪域" on-ok="handleOk" :maskClosable="false" @afterClose="handleCancel()" :width='850'>
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
          :label-col="{ span: 3 }"
          :wrapper-col="{ span: 18 }"
          :layout="layout"
          childrenColumnName="track_url"
        >
        <a-row>
          <a-col>
            <a-form-model-item ref="name" label="联盟名称" prop="name">
              <a-input v-model="form.name" />
            </a-form-model-item>
          </a-col>
        </a-row>
        <a-row>
          <a-col>
            <a-form-model-item label="联盟链接" prop="url" :labelCol="{span: 3}" :wrapperCol="{span: 18}">
            <a-input v-model="form.url" type="textarea" />
          </a-form-model-item>
          </a-col>
        </a-row>
        </a-form-model>
      </template>
    </a-modal>
    </div>
  </a-card>
</template>

<script>
import {GetAffiliatelistDate, AddDate} from '@/services/affiliatelist'
const columns = [
  {
    title: '序号',
    dataIndex: 'index',
    key: 'index',
    width: 80
  },
  {
    title: '联盟名称',
    key: 'name',
    dataIndex: 'name'
  },
  {
    title: '链接',
    key: 'url',
    dataIndex: 'url'
  },
  {
    title: '创建时间',
    dataIndex: ''
  },
  { title: '操作',
    key: 'operation',
    scopedSlots: { customRender: 'operation' } 
  },
]

const innerColumns = [{
  title: '链接',
  dataIndex: 'urls',
  key: 'urls',
  width: 1025
  },
  { title: '操作',
    key: 'operation',
    scopedSlots: { customRender: 'operation' } 
  },]

const dataSource = []

export default {
  name: 'QueryList',
  data () {
    return {
      query: {
        page: '1',
        page_size: '10',
        name: '',
        url: '',
      },
      form: {
        name: '',
        url: ''
      },
      subforms: {

      },
      layout: 'vertical',
      advanced: true,
      columns: columns,
      dataSource: dataSource,
      innerColumns,
      selectedRows: [],
      departmentoptions: ['商务部', "技术部"],
      tablename: '',
      visible: false,
      subvisible: false,
      loading: false,
      rules: {
        name: [{ required: true, message: '请输入文件名', trigger: 'blur' }],
        url: [{ required: false, message: 'Please input activity form', trigger: 'blur' }],
      }
    }
  },
  created () {
    this.gettabledata()
  },
  methods: {
    gettabledata () {
      GetAffiliatelistDate(this.query).then(res => {
        console.log(res);
        res.data.data.forEach((i, y) => {
          i['index'] = y + 1
          i.task_ruls = []
          i.track_url.forEach((a, b) => {
            let obj = {}
            obj.id = b
            obj.urls = a
            i.task_ruls.push(obj)
          })
        });
        console.log(res.data.data);
        this.dataSource = res.data.data
      })
    },
    toggleAdvanced () {
      this.advanced = !this.advanced
    },
    remove () {
      this.dataSource = this.dataSource.filter(item => this.selectedRows.findIndex(row => row.key === item.key) === -1)
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
      this.showdeleConfirm(this.selectedRows)
    },
    // 重置查询表单
    resettingqueryform() {
      for(var key in this.query) {
        this.query[key] = ''
      }
    },
    // 打开父表表单
    showModal(id) {
      typeof id === 'number' ? this.tablename = '编辑' : this.tablename = '新增'
      this.visible = true;
    },
    // 提交父表表单
    handleOk() {
      this.$refs.ruleForm.validate(valid => {
        if (valid) {
          this.loading = true;
          AddDate(this.form).then(res => {
            console.log(res);
            this.$message.success('添加成功！')
            this.loading = false;
            this.visible = false;
            this.gettabledata();
          })
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
      this.$confirm({
        title: '是否删除所选项?',
        content: '删除之后无法恢复！',
        onOk() {
          return new Promise((resolve, reject) => {
            console.log(id);
            setTimeout(Math.random() > 0.5 ? resolve : reject, 1000);
          }).catch(() => console.log('Oops errors!'));
        },
        onCancel() {},
      })
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
