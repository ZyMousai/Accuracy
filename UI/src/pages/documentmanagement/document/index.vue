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
              <a-select v-model="query.department_id" placeholder="请选择" :allowClear="true" :disabled="OperationVerification()">
                <a-select-option v-for="item in departmentoptions" :key="item.id" :value="item.id">
                  {{item.department}}
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
      <a-button type="primary" @click="Batchdelete()"><a-icon type="delete" />批量删除</a-button>
      <a-button type="primary" @click="Batchdwon()" style="margin-left: 5px;"><a-icon type="cloud-download" />批量下载</a-button>
      <a-space class="operator">
        <a-upload
          name="files"
          :multiple="true"
          :action="updocuurl"
          :headers="headers"
          :before-upload="beforeUpload"
          @change="handleChange"
          style="margin-left: 5px;"
        >
        <a-button type="primary"><a-icon type="cloud-upload" />批量上传</a-button>
        </a-upload>
      </a-space>
      <standard-table
        :columns="columns"
        :dataSource="dataSource"
        :selectedRows.sync="selectedRows"
        :rowKey='record=>record.id'
        :loading="tableloading"
        :pagination="false"
      >
        <div slot="action" slot-scope="{record}">
          <a style="margin-right: 8px" @click="downdocument(record.file_url, record.filename)">
            <a-icon type="cloud-download"/>下载
          </a>
          <a @click="showModal(record)" style="margin-right: 8px">
            <a-icon type="edit"/>修改
          </a>
          <a @click="deletedialog(record.id)">
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
              :disabled="true"
            />
          </a-form-model-item>
          <a-form-model-item label="权限部门" prop="department_id">
            <a-select v-model="editform.department_id" placeholder="请选择" :allowClear="true">
              <a-select-option v-for="item in departmentoptions" :key="item.id" :value="item.id">
                {{item.department}}
              </a-select-option>
            </a-select>
          </a-form-model-item>
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
      <p>是否放入回收站</p>
      <p>小提示：如果不放入回收站则直接删除，无法恢复!</p>
    </a-modal>
    </div>
  </a-card>
</template>

<script>
import StandardTable from '@/components/table/StandardTable'
import {DocumentDate, DeleteDocuments, EditDate} from '@/services/documentmanagement'
import {DepartmentDate} from '@/services/personnelmanagement'
import {OperationVerification} from '@/plugins/permissionverify'
import Cookie from 'js-cookie'
const columns = [
  {
    title: '序号',
    dataIndex: 'index',
    width: 80
  },
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
        page: 1,
        page_size: 10,
        filename: null,
        user_name: null,
        department_id: null,
        start_time: null,
        end_time: null,
      },
      total: 0,
      editform: {
        id: '',
        filename: '',
        department_id: ''
      },
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
      dialogvisible: false,
      departmentoptions: [],
      editrules: {
        filename: [{ required: true, message: '请输入文件名', trigger: 'blur' }],
        department_id: [{ required: true, message: '请选择部门权限', trigger: 'change' }]
      },
      tableloading: false,
      alone: '',
      headers: {
        accept: 'application/json',
        authorization: 'authorization-text',
        token: Cookie.get('Authorization')
      }
    }
  },
  created () {
    this.getdepartmentoptions()
  },
  methods: {
    OperationVerification,
    //获取部门列表
    getdepartmentoptions(){
      DepartmentDate().then(res => {
        if (res.status === 200) {
          console.log(this.roles);
          this.departmentoptions = res.data.data
          this.gettabledata()
          this.query.department_id = localStorage.getItem('department_id') - ''
        } else {
          this.$message.error('获取部门列表失败！')
        }
      })
    },
    // 获取表格数据
    gettabledata () {
      this.alone = process.env.VUE_APP_API_ALONE_URL
      this.tableloading = true
      DocumentDate(this.query).then(res => {
        if (res.status === 200) {
          console.log(res);
          this.dataSource = res.data.data
          this.total = res.data.total
          console.log(this.total);
          this.tableloading = false
          for (var i = 0; i < this.dataSource.length; i++) {
            this.dataSource[i]["index"] = i + 1
            this.dataSource[i]["file_url"] = this.alone + '/DocumentManagement/documents/v1/download/' + this.dataSource[i].filename
          }
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
      this.query.department_id = localStorage.getItem('department_id') - ''
      this.gettabledata()
    },
    // 打开编辑表单
    showModal(data) {
      console.log(data);
      this.editform.id = data.id
      this.editform.department_id = data.department_id  - ''
      this.editform.filename = data.filename
      console.log(this.editform);
      this.visible = true;
    },
    // 提交编辑表单
    submitform() {
      this.$refs.ruleForm.validate(valid => {
        if (valid) {
          this.loading = true;
          EditDate(this.editform).then(res => {
            if (res.status === 200) {
              this.$message.success(`编辑成功！`);
              this.loading = false;
              this.visible = false;
              this.gettabledata()
            } else {
              this.$message.error(`编辑失败！`);
              this.loading = false;
              this.visible = false;
              this.gettabledata()
            }
          })
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
      let is_logic_del = '1';
      for (let i = 0; i < this.ids.length; i++) {
        await DeleteDocuments(this.ids[i], is_logic_del).then(res => {
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
    async onno() {
      let is_logic_del = '0';
      for (let i = 0; i < this.ids.length; i++) {
        await DeleteDocuments(this.ids[i], is_logic_del).then(res => {
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
    // 上传文件
    handleChange(info) {
      if (info.file.status !== 'uploading') {
        console.log(info.file, info.fileList);
      }
      if (info.file.status === 'done') {
        this.$message.success(`${info.file.name}文件上传成功！`);
        this.gettabledata()
      } else if (info.file.status === 'error') {
        this.$message.error(`${info.file.name}文件上传失败！`);
      }
    },
    beforeUpload() {
      const user_id  = localStorage.getItem('id')
      const department_id  = localStorage.getItem('department_id')
      this.updocuurl = `${this.alone}/DocumentManagement/documents/v1/upload?user_id=${user_id}&department_id=${department_id}`
    },
    // 自定义删除对话框底部按钮
    modalfooter() {
      return (
        <div>
          <a-button onClick={this.onok}  type="primary">是</a-button>
          <a-button onClick={this.onno}  type="danger">直接删除</a-button>
          <a-button onClick={this.canceldelete}>取消</a-button>
        </div>
      )
    },
    // 文档下载
    downdocument(url, name) {
      console.log(URL);
      const a = document.createElement('a')
      fetch(url).then(res => res.blob()).then(blob => {
        a.href = URL.createObjectURL(blob)
        a.download = name || ''
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(a.href);
        document.body.removeChild(a);
      })
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
    // 批量下载
    Batchdwon() {
      console.log(this.selectedRows);
      for (let i = 0; i < this.selectedRows.length; i++) {
        this.downdocument(this.selectedRows[i].file_url, this.selectedRows[i].filename)
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
