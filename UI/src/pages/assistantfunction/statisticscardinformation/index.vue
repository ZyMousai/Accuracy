<template>
  <a-card>
    <div :class="advanced ? 'search' : null">
      <a-form layout="horizontal" :model="query">
        <div :class="advanced ? null: 'fold'">
          <a-row >
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="文件名"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-input v-model="query.filename" placeholder="请输入" />
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="上传用户"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-input v-model="query.uploadusers" style="width: 100%" placeholder="请输入" />
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="部门选择"
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
        </a-row>
          <a-row v-if="advanced">
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="上传日期"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-date-picker v-model="query.uploaddate" style="width: 100%" placeholder="请输入更新日期" />
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
        <a-upload
          name="file"
          :multiple="true"
          action="https://www.mocky.io/v2/5cc8019d300000980a055e76"
          :headers="headers"
          :showUploadList="false"
          @change="handleChange"
        >
        <a-button type="primary"><a-icon type="cloud-upload" />批量上传</a-button>
        </a-upload>
        <a-button type="primary"><a-icon type="cloud-download" />批量下载</a-button>
        <a-button type="primary" @click="Batchdelete()"><a-icon type="delete" />批量删除</a-button>
      </a-space>
      <a-table :columns="columns" :data-source="data" class="components-table-demo-nested">
        <a slot="operation" >编辑</a>
        <a slot="operation" style="margin-left: 5px;">删除</a>
        <a-table
          slot="expandedRowRender"
          :columns="innerColumns"
          :data-source="innerData"
          :pagination="false"
        >
          <span slot="operation" class="table-operation">
            <a>编辑</a>
            <a style="margin-left: 5px;">删除</a>
          </span>
        </a-table>
      </a-table>
      <!-- 编辑表单 -->
      <a-modal v-model="visible" title="编辑" on-ok="handleOk" :maskClosable="false" @afterClose="handleCancel()">
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
          :model="editform"
          :rules="editrules"
          :label-col="{ span: 4 }"
          :wrapper-col="{ span: 14 }"
        >
          <a-form-model-item ref="filename" label="文件名" prop="filename">
            <a-input
              v-model="editform.filename"
            />
          </a-form-model-item>
          <a-form-model-item label="权限部门" prop="department">
            <a-radio-group v-model="editform.department">
              <a-radio value="1">
                运营部
              </a-radio>
              <a-radio value="2">
                技术部
              </a-radio>
            </a-radio-group>
          </a-form-model-item>
        </a-form-model>
      </template>
    </a-modal>
    <!-- 删除确认对话框 -->

    </div>
  </a-card>
</template>

<script>
const columns = [
  { title: '卡号', dataIndex: 'name', key: 'name' },
  { title: '有效期', dataIndex: 'platform', key: 'platform' },
  { title: 'cvv', dataIndex: 'version', key: 'version' },
  { title: '面值', dataIndex: 'upgradeNum', key: 'upgradeNum' },
  { title: '余额', dataIndex: 'creator', key: 'creator' },
  { title: '卡姓名地址', dataIndex: 'creator', key: 'creator' },
  { title: '备注', dataIndex: 'creator', key: 'creator' },
  { title: '平台', dataIndex: 'creator', key: 'creator' },
  { title: '卡状态', dataIndex: 'creator', key: 'creator' },
  { title: '保留', dataIndex: 'creator', key: 'creator' },
  { title: '创建日期', dataIndex: 'createdAt', key: 'createdAt' },
  { title: '操作', key: 'operation', scopedSlots: { customRender: 'operation' } },
];

const data = [];
for (let i = 0; i < 3; ++i) {
  data.push({
    key: i,
    name: 'Screem',
    platform: 'iOS',
    version: '10.3.4.5654',
    upgradeNum: 500,
    creator: 'Jack',
    createdAt: '2014-12-24 23:12:00',
  });
}

const innerColumns = [
  { title: '联盟', dataIndex: 'date', key: 'date' },
  { title: '账号', dataIndex: 'name', key: 'name' },
  { title: '任务', dataIndex: 'name', key: 'name' },
  { title: '佣金', dataIndex: 'name', key: 'name' },
  { title: '消耗', dataIndex: 'name', key: 'name' },
  { title: '使用人', dataIndex: 'name', key: 'name' },
  { title: '二次消费', dataIndex: 'name', key: 'name' },
  { title: '使用日期', dataIndex: 'name', key: 'name' },
  {
    title: '操作',
    dataIndex: 'operation',
    key: 'operation',
    scopedSlots: { customRender: 'operation' },
  },
];

const innerData = [];
for (let i = 0; i < 3; ++i) {
  innerData.push({
    key: i,
    date: '2014-12-24 23:12:00',
    name: 'This is production name',
    upgradeNum: 'Upgraded: 56',
  });
}

export default {
  name: 'QueryList',
  data () {
    return {
      data,
      columns,
      innerColumns,
      innerData,
      query: {
        filename: '',
        uploadusers: '',
        department: '',
        uploaddate: ''
      },
      editform: {
        filename: '',
        department: ''
      },
      advanced: true,
      selectedRows: [],
      visible: false,
      loading: false,
      departmentoptions: ['商务部', '技术部'],
      editrules: {
        filename: [{ required: true, message: '请输入文件名', trigger: 'blur' }],
        department: [{ required: true, message: '请选择部门权限', trigger: 'change' }]
      },
      headers: {
        authorization: 'authorization-text',
      }
    }
  },
  methods: {
    toggleAdvanced () {
      this.advanced = !this.advanced
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
      console.log(id);
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
        content: '删除之后会放在回收站',
        onOk() {
          return new Promise((resolve, reject) => {
            console.log(id);
            setTimeout(Math.random() > 0.5 ? resolve : reject, 1000);
          }).catch(() => console.log('Oops errors!'));
        },
        onCancel() {},
      })
    },
    // 上传文件
    handleChange(info) {
      if (info.file.status !== 'uploading') {
        console.log(info.file, info.fileList);
      }
      if (info.file.status === 'done') {
        this.$message.success(`${info.file.name} file uploaded successfully`);
      } else if (info.file.status === 'error') {
        this.$message.error(`${info.file.name} file upload failed.`);
      }
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
