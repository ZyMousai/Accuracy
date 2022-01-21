<template>
  <a-card>
    <div :class="advanced ? 'search' : null">
      <a-form layout="horizontal" :model="query">
        <div :class="advanced ? null: 'fold'">
          <a-row >
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="请选择任务"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-select v-model="query.department" placeholder="请选择">
                <a-select-option v-for="item in departmentoptions" :key="item" :value="item">
                  {{item}}
                </a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24" :offset="1" style="margin-top: 3px;">
            <a-button type="primary">刷新任务</a-button>
          </a-col>
        </a-row>
        <a-row >
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="任务URL"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-input v-model="teakURL" placeholder=" " :disabled='true' />
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24" :offset="1" style="margin-top: 3px;">
            <a-button type="primary">获取URL</a-button>
            <a-button type="primary" style="margin-left: 15px" v-clipboard:copy="teakURL" v-clipboard:success="onCopy" v-clipboard:error="onError">复制URL</a-button>
          </a-col>
        </a-row>
        </div>
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
        @clear="onClear"
        @change="onChange"
      >
        <div slot="description" slot-scope="{text}">
          {{text}}
        </div>
        <div slot="action" slot-scope="{record}">
          <a @click="showdeleConfirm(record.ne)">
            <a-icon type="delete" />删除
          </a>
        </div>
        <template slot="statusTitle">
          <a-icon @click.native="onStatusTitleClick" type="info-circle" />
        </template>
      </standard-table>
      <!-- 表单 -->
      <a-modal v-model="visible" :title="tablename" on-ok="handleOk" :maskClosable="false" @afterClose="handleCancel()" :width='750'>
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
          :layout="form.layout"
        >
            <a-form-model-item ref="filename" label="主任务ID" prop="filename">
              <a-input v-model="form.filename" />
            </a-form-model-item>
            <a-form-model-item ref="filename" label="主任务名" prop="filename">
              <a-input v-model="form.filename" />
            </a-form-model-item>
            <a-form-model-item ref="filename" label="从任务ID" prop="filename">
            <a-input v-model="form.filename" />
          </a-form-model-item>
            <a-form-model-item ref="filename" label="从任务名" prop="filename">
            <a-input v-model="form.filename" />
          </a-form-model-item>
        </a-form-model>
      </template>
    </a-modal>
    </div>
  </a-card>
</template>

<script>
import StandardTable from '@/components/table/StandardTable'
const columns = [
  {
    title: '规则编号',
    dataIndex: 'ne'
  },
  {
    title: '描述',
    dataIndex: 'description',
    scopedSlots: { customRender: 'description' }
  },
  {
    title: '服务调用次数',
    dataIndex: 'callNo',
    needTotal: true,
    customRender: (text) => text + ' 次'
  },
  {
    dataIndex: 'status',
    needTotal: true,
    slots: {title: 'statusTitle'}
  },
  {
    title: '更新时间',
    dataIndex: 'updatedAt'
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
      query: {
        platform: '',
        account: '',
      },
      form: {
        layout: 'vertical',
        filename: '',
        department: '',
        desc: ''
      },
      advanced: true,
      columns: columns,
      dataSource: dataSource,
      selectedRows: [],
      departmentoptions: ['商务部', "技术部"],
      tablename: '',
      visible: false,
      loading: false,
      teakURL: 'sssss',
      rules: {
        filename: [{ required: true, message: '请输入文件名', trigger: 'blur' }],
        department: [{ required: true, message: '请选择部门', trigger: 'change' }],
        desc: [{ required: false, message: 'Please input activity form', trigger: 'blur' }],
      }
    }
  },
  methods: {
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
    // 批量删除
    Batchdelete() {
      this.showdeleConfirm(this.selectedRows)
    },
    // 打开编辑表单
    showModal(id) {
      typeof id === 'number' ? this.tablename = '编辑' : this.tablename = '新增'
      this.visible = true;
    },
    // 提交编辑表单
    handleOk() {
      this.$refs.ruleForm.validate(valid => {
        if (valid) {
          this.loading = true;
          console.log('ok');
        }
      })
    },
    // 关闭编辑表单
    handleCancel() {
      this.visible = false;
      this.$refs.ruleForm.resetFields();
      console.log('ok');
    },
    onCopy () {
      this.$message.success('复制成功！')
    },
    onError () {
      this.$message.error('复制失败！')
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
