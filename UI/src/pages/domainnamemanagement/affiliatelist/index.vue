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
              <a-input v-model="query.name_or_url" placeholder="请输入" />
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="跟踪域链接"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-input v-model="query.track_url" style="width: 100%" placeholder="请输入" />
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
      <a-table :columns="columns" :data-source="dataSource" class="components-table-demo-nested" :rowKey='record=>record.id' >
        <div slot="action" slot-scope="record">
          <a slot="operation" @click="showModal(record)">编辑</a>
          <a slot="operation" style="margin-left: 5px;" @click="subshowModal(record.id)">添加跟踪域</a>
          <a-popconfirm
            title="你确定要删除此项?"
            ok-text="是"
            cancel-text="否"
            @confirm="confirmdelete(record.id)"
            @cancel="cancel"
            slot="operation">
            <a style="margin-left: 5px;">删除</a>
          </a-popconfirm>
        </div>
        <a-table
          slot="expandedRowRender"
          slot-scope="record"
          :columns="innerColumns"
          :data-source="record.track_url"
          :pagination="false"
          :showHeader="false"
        >
          <a-popconfirm
            slot-scope="record"
            title="你确定要删除此项?"
            ok-text="是"
            cancel-text="否"
            @confirm="confirmdeletetaskurl(record.id)"
            @cancel="cancel"
            slot="operation">
            <a style="margin-left: 5px;">删除</a>
          </a-popconfirm>
        </a-table>
      </a-table>
      <!-- 父表表单 -->
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
          :label-col="{ span: 3 }"
          :wrapper-col="{ span: 18 }"
          :layout="layout"
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
      <a-modal v-model="subvisible" title="添加跟踪域" on-ok="subhandleOk" :maskClosable="false" @afterClose="subhandleCancel()" :width='850'>
        <template slot="footer">
          <a-button key="back" @click="subhandleCancel">
            取消
          </a-button>
          <a-button key="submit" type="primary" :loading="loading" @click="subhandleOk">
            提交
          </a-button>
        </template>
        <template>
          <a-form-model
            ref="subruleForm"
            :model="subforms"
            :rules="subrules"
            :label-col="{ span: 3 }"
            :wrapper-col="{ span: 18 }"
            :layout="layout"
          >
          <a-row>
            <a-col>
              <a-form-model-item label="跟踪域链接" prop="track_url" :labelCol="{span: 3}" :wrapperCol="{span: 18}">
              <a-input v-model="subforms.track_url" type="textarea" />
            </a-form-model-item>
            </a-col>
          </a-row>
          </a-form-model>
        </template>
      </a-modal>
      <a-pagination
      style="margin-top: 15px;"
      v-model="query.page"
      :total="total"
      show-size-changer
      @showSizeChange="onShowSizeChange"
      :show-total="total => `一共 ${total} 条`"
      @change="pageonChange" />
    </div>
  </a-card>
</template>

<script>
import {GetAffiliatelistDate, AddDate, AddTaskUrlDate, EditDate, DeleteDate, DeleteTaskUrlDate} from '@/services/affiliatelist'
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
    key: 'action',
    scopedSlots: { customRender: 'action' } 
  },
]

const innerColumns = [{
  title: '链接',
  dataIndex: 'track_url',
  key: 'track_url'
  },
  { title: '操作',
    key: 'operation',
    width: 450,
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
        name_or_url: '',
        track_url: '',
      },
      form: {
        name: '',
        url: ''
      },
      subforms: {
        track_url: '',
        alliance_id: ''
      },
      total: 0,
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
        name: [{ required: true, message: '请输入联盟名称', trigger: 'blur' }],
        url: [{ required: false, trigger: 'blur' }],
      },
      subrules: {
        track_url: [{ required: true, message: '请输入跟踪链接', trigger: 'blur' }],
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
        });
        console.log(res.data.data);
        this.dataSource = res.data.data
        this.total = res.data.total
        console.log(this.total);
      })
    },
    toggleAdvanced () {
      this.advanced = !this.advanced
    },
    onClear() {
      this.$message.info('您清空了勾选的所有行')
    },
    // 查询
    queryevents() {
      this.query.page = 1
      this.query.page_size = 10
      this.gettabledata()
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
    // 打开父表表单
    showModal(data) {
      data.id ? this.tablename = '编辑' : this.tablename = '新增'
      this.form.name = data.name
      this.form.url = data.url
      this.form.id = data.id
      this.visible = true;
    },
    // 提交父表表单
    handleOk() {
      this.$refs.ruleForm.validate(valid => {
        if (valid) {
          if (!this.form.id) {
              this.loading = true;
              AddDate(this.form).then(res => {
              console.log(res);
              this.$message.success('添加成功！')
              this.loading = false;
              this.visible = false;
              this.gettabledata();
            })
          } else {
            this.loading = true;
              EditDate(this.form).then(res => {
              console.log(res);
              this.$message.success('编辑成功！')
              this.loading = false;
              this.visible = false;
              this.gettabledata();
            })
          }
        }
      })
    },
    // 关闭父表表单
    handleCancel() {
      this.visible = false;
      this.$refs.ruleForm.resetFields();
    },
    // 打开子表表单
    subshowModal(id) {
      console.log(id);
      this.subforms.alliance_id = id
      this.subvisible = true;
    },
    // 关闭子表表单
    subhandleCancel() {
      this.subvisible = false;
      this.$refs.subruleForm.resetFields();
    },
    // 提交子表表单
    subhandleOk() {
      this.$refs.subruleForm.validate(valid => {
        if (valid) {
          this.loading = true;
          AddTaskUrlDate(this.subforms).then(res => {
            console.log(res);
            this.$message.success('添加成功！')
            this.loading = false;
            this.subhandleCancel()
            this.gettabledata();
          })
        }
      })
    },
    // 删除确认框
    confirmdelete(id) {
      const ids = []
      ids.push(id)
      DeleteDate(ids).then(res => {
        console.log(res);
        this.$message.success('删除成功！');
        this.gettabledata()
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
    cancel(e) {
      console.log(e);
      this.$message.error('取消删除！');
    },
    // 删除跟踪域
    confirmdeletetaskurl(id) {
      const ids = []
      ids.push(id)
      DeleteTaskUrlDate(ids).then(res => {
        console.log(res);
        this.$message.success('删除成功！');
        this.gettabledata()
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
