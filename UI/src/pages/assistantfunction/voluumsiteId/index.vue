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
              <a-select v-model="department" placeholder="请选择">
                <a-select-option v-for="item in departmentoptions" :key="item.id" :value="item.id" @change="tasknamechange">
                  {{item.s_name}}
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
            <a-button type="primary" @click="getURL">获取URL</a-button>
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
        :rowKey='record=>record.id'
      >
        <div slot="description" slot-scope="{text}">
          {{text}}
        </div>
        <div slot="action" slot-scope="{record}">
          <a @click="DeleteDate(record.id)">
            <a-icon type="delete" />删除
          </a>
        </div>
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
            <a-form-model-item ref="m_id" label="主任务ID" prop="m_id">
              <a-input v-model="form.m_id" />
            </a-form-model-item>
            <a-form-model-item ref="m_name" label="主任务名" prop="m_name">
              <a-input v-model="form.m_name" />
            </a-form-model-item>
            <a-form-model-item ref="s_id" label="从任务ID" prop="s_id">
            <a-input v-model="form.s_id" />
          </a-form-model-item>
            <a-form-model-item ref="s_name" label="从任务名" prop="s_name">
            <a-input v-model="form.s_name" />
          </a-form-model-item>
        </a-form-model>
      </template>
    </a-modal>
    <!-- 删除确认对话框 -->
    <a-modal
     title="是否删除所选项？"
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
import {GetVoluumsiteIdData, AddDate, DeleteDate} from '@/services/voluumsiteId'
const columns = [
  {
    title: '序号',
    dataIndex: 'index',
    key: 'index',
    width: 80
  },
  {
    title: '主任务ID',
    dataIndex: 'm_id',
    key: 'm_id'
  },
  {
    title: '主任务名',
    dataIndex: 'm_name',
    key: 'm_name'
  },
  {
    title: '从任务ID',
    dataIndex: 's_id',
    key: 's_id'
  },
  {
    title: '从任务名',
    dataIndex: 's_name',
    key: 's_name'
  },
  {
    title: '操作',
    scopedSlots: { customRender: 'action' },
    width: 100
  }
]

const dataSource = []

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
        desc: ''
      },
      department: '',
      advanced: true,
      columns: columns,
      dataSource: dataSource,
      selectedRows: [],
      departmentoptions: [],
      tablename: '',
      visible: false,
      loading: false,
      teakURL: 'sssss',
      rules: {
        m_id: [{ required: true, message: '请输入文件名', trigger: 'blur' }],
        m_name: [{ required: true, message: '请输入文件名', trigger: 'blur' }],
        s_id: [{ required: true, message: '请输入文件名', trigger: 'blur' }],
        s_name: [{ required: true, message: '请输入文件名', trigger: 'blur' }],
      },
      ids: [],
      dialogvisible: false,
      m_taskid: '',
      s_taskid: ''
    }
  },
  created () {
    this.gettabledata()
  },
  methods: {
    gettabledata() {
      GetVoluumsiteIdData(this.query).then(res => {
        console.log(res);
        res.data.data.forEach((i, y) => {
          i['index'] = y + 1
        });
        console.log(res.data.data);
        this.dataSource = res.data.data
        this.departmentoptions = res.data.data
      })
    },
    // 批量删除
    Batchdelete() {
      console.log(this.selectedRows);
      for (let i = 0; i < this.selectedRows.length; i++) {
        this.ids.push(this.selectedRows[i].id)
      }
      this.dialogvisible = true
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
              AddDate(this.form).then(res => {
              console.log(res);
              this.$message.success('添加成功！')
              this.loading = false;
              this.visible = false;
              this.gettabledata();
              this.handleCancel();
          })
        }
      })
    },
    // 关闭编辑表单
    handleCancel() {
      this.visible = false;
      this.$refs.ruleForm.resetFields();
    },
    onCopy () {
      this.$message.success('复制成功！')
    },
    onError () {
      this.$message.error('复制失败！')
    },
    // 删除对话框
    DeleteDate(id) {
      this.ids.push(id);
      this.dialogvisible = true;
    },
    async onok() {
      for (let i = 0; i < this.ids.length; i++) {
        await DeleteDate(this.ids[i]).then(res => {
          console.log(res);
          })
      }
      this.gettabledata()
      this.ids = []
      this.dialogvisible = false
    },
    onno() {
      this.ids = [];
      this.dialogvisible = false
    },
    tasknamechange(value) {
      const rule = this.options.find(item => item.id === value)
      this.m_taskid = rule.m_id
      this.s_taskid = rule.s_id
      console.log(this.m_taskid);
      console.log(this.s_taskid);
    },
    // 获取URL
    getURL() {
      console.log(this.department);
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
