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
              <a-input v-model="query.user_name" style="width: 100%" placeholder="请输入" />
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="部门选择"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-select v-model="query.department_id" placeholder="请选择">
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
              label="开始日期"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-date-picker v-model="start_time" style="width: 100%" placeholder="请输入更新日期" format="YYYY-MM-DD"/>
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="结束日期"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-date-picker v-model="end_time" style="width: 100%" placeholder="请输入更新日期" format="YYYY-MM-DD" />
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
          name="files"
          :multiple="true"
          action="http://192.168.50.115:8000/api/DocumentManagement/documents/v1/upload?user_id=1&department_id=2"
          :headers="headers"
          :showUploadList="false"
          @change="handleChange"
        >
        <a-button type="primary"><a-icon type="cloud-upload" />批量上传</a-button>
        </a-upload>
        <a-button type="primary"><a-icon type="cloud-download" />批量下载</a-button>
        <a-button type="primary" @click="Batchdelete()"><a-icon type="delete" />批量删除</a-button>
      </a-space>
      <standard-table
        :columns="columns"
        :dataSource="dataSource"
        :selectedRows.sync="selectedRows"
        @clear="onClear"
        @change="onChange"
        :rowKey='record=>record.id'
      >
        <div slot="action" slot-scope="{record}">
          <a style="margin-right: 8px">
            <a-icon type="cloud-download"/>下载
          </a>
          <a @click="showModal(record.id)" style="margin-right: 8px">
            <a-icon type="edit"/>修改
          </a>
          <a @click="deletedialog(record.id)">
            <a-icon type="delete" />删除
          </a>
        </div>
      </standard-table>
      <!-- 编辑表单 -->
      <a-modal v-model="visible" title="编辑" on-ok="handleOk" :maskClosable="false" @afterClose="closeform()">
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
    <a-modal
     title="是否将所选项放入回收站"
     :visible="dialogvisible"
     ok-text="是"
     cancel-text="否"
     @ok="onok"
     @cancel="onno">
      <p>如果不放入回收站则直接删除，无法恢复</p>
    </a-modal>
    </div>
  </a-card>
</template>

<script>
import StandardTable from '@/components/table/StandardTable'
import {DocumentDate, DeleteDocuments} from '@/services/documentmanagement'
const columns = [
  {
    title: '上传时间',
    dataIndex: 'created_time'
  },
  {
    title: '文件名',
    dataIndex: 'filename'
  },
  {
    title: '文件大小',
    dataIndex: 'file_size'
  },
  {
    title: '上传人',
    dataIndex: 'uploader_name'
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
        page: '1',
        page_size: '10',
        filename: null,
        user_name: null,
        department_id: null,
        start_time: null,
        end_time: null,
      },
      editform: {
        filename: '',
        department: ''
      },
      advanced: true,
      columns: columns,
      dataSource: dataSource,
      selectedRows: [],
      ids: [],
      visible: false,
      loading: false,
      start_time: '',
      end_time: '',
      dialogvisible: false,
      departmentoptions: ['商务部', '技术部'],
      editrules: {
        filename: [{ required: true, message: '请输入文件名', trigger: 'blur' }],
        department: [{ required: true, message: '请选择部门权限', trigger: 'change' }]
      },
      headers: {
        accept: 'application/json',
        authorization: 'authorization-text',
      }
    }
  },
  created () {
    this.gettabledata()
  },
  methods: {
    // 获取表格数据
    gettabledata () {
      DocumentDate(this.query).then(res => {
        this.dataSource = res.data.data
      })
    },
    toggleAdvanced () {
      this.advanced = !this.advanced
    },
    onClear() {
      this.$message.info('您清空了勾选的所有行')
    },
    onChange(current) {
      this.query.page = current.current
      this.gettabledata()
      this.$message.info('表格状态改变了')
    },
    // 查询
    queryevents() {
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
        this.query[key] = ''
      }
      this.query.page = '1'
      this.query.page_size = '10'
      this.gettabledata()
    },
    // 打开编辑表单
    showModal(id) {
      console.log(id);
      this.visible = true;
    },
    // 提交编辑表单
    submitform() {
      this.$refs.ruleForm.validate(valid => {
        if (valid) {
          this.loading = true;
          console.log('ok');
        }
      })
    },
    // 关闭编辑表单
    closeform() {
      this.visible = false;
      this.$refs.ruleForm.resetFields();
      console.log('ok');
    },
    deletedialog(id) {
      this.ids.push(id)
      this.dialogvisible = true
    },
    async onok() {
      let is_logic_del = '0'
      for (let i = 0; i < this.ids.length; i++) {
        await DeleteDocuments(this.ids[i], is_logic_del).then(res => {
          console.log(res);
          })
      }
      this.gettabledata()
      this.ids = []
      this.dialogvisible = false
    },
    async onno() {
      let is_logic_del = '1'
      for (let i = 0; i < this.ids.length; i++) {
        await DeleteDocuments(this.ids[i], is_logic_del).then(res => {
          console.log(res);
          })
      }
      this.gettabledata()
      this.ids = []
      this.dialogvisible = false
    },
    // 上传文件
    handleChange(info) {
      if (info.file.status !== 'uploading') {
        console.log(info.file, info.fileList);
      }
      if (info.file.status === 'done') {
        this.$message.success(`${info.file.name} file uploaded successfully`);
        this.gettabledata()
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
