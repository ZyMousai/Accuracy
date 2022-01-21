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
        @clear="onClear"
        @change="onChange"
      >
        <div slot="description" slot-scope="{text}">
          {{text}}
        </div>
        <div slot="action" slot-scope="{record}">
          <a @click="showModal(record.key)" style="margin-right: 8px">
            <a-icon type="edit"/>修改
          </a>
          <a @click="showdeleConfirm(record.ne)">
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
            <a-form-model-item ref="filename" label="平台" prop="filename">
              <a-input v-model="form.filename" />
            </a-form-model-item>
          </a-col>
          <a-col :span="10">
            <a-form-model-item ref="filename" label="账号" prop="filename">
              <a-input v-model="form.filename" />
            </a-form-model-item>
          </a-col>
        </a-row>
        <a-row :gutter="16">
          <a-col :span="10">
            <a-form-model-item ref="filename" label="密码" prop="filename">
            <a-input v-model="form.filename" />
          </a-form-model-item>
          </a-col>
          <a-col :span="10">
            <a-form-model-item label="权限部门" prop="department">
            <a-select v-model="form.department" placeholder="请选择部门">
              <a-select-option v-for="item in departmentoptions" :key="item" :value="item">
                {{item}}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          </a-col>
        </a-row>
        <a-row :gutter="16">
          <a-col :span="10">
            <a-form-model-item label="权限角色" prop="department">
            <a-select v-model="form.department" placeholder="请选择角色">
              <a-select-option v-for="item in departmentoptions" :key="item" :value="item">
                {{item}}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          </a-col>
          <a-col :span="10">
            <a-form-model-item label="权限人员" prop="department">
            <a-select v-model="form.department" placeholder="请选择人员">
              <a-select-option v-for="item in departmentoptions" :key="item" :value="item">
                {{item}}
              </a-select-option>
            </a-select>
          </a-form-model-item>
          </a-col>
        </a-row>
        <a-row>
          <a-col>
            <a-form-model-item label="备注" prop="desc" :labelCol="{span: 2}" :wrapperCol="{span: 18}">
            <a-input v-model="form.desc" type="textarea" />
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
