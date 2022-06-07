<template>
  <a-card>
    <div :class="advanced ? 'search' : null">
      <a-form layout="horizontal" :model="query">
        <div :class="advanced ? null : 'fold'">
          <a-row>
            <a-col :md="8" :sm="24">
              <a-form-item
                label="ip"
                :labelCol="{ span: 5 }"
                :wrapperCol="{ span: 18, offset: 1 }"
              >
                <a-input v-model="query.machine_ip" placeholder="ip" />
              </a-form-item>
            </a-col>
          </a-row>
        </div>
        <span style="float: right; margin-top: 3px">
          <a-button type="primary" @click="queryevents">查询</a-button>
          <a-button style="margin-left: 8px" @click="resettingqueryform">重置</a-button>
          <a @click="toggleAdvanced" style="margin-left: 8px">
            {{ advanced ? "收起" : "展开" }}
            <a-icon :type="advanced ? 'up' : 'down'" />
          </a>
        </span>
      </a-form>
    </div>
    <div>
      <a-space class="operator">
        <a-button type="primary" @click="showModal">
          <a-icon type="plus-circle" />新增
        </a-button>
        <a-button type="primary" @click="Batchdelete()">
          <a-icon type="delete" />批量删除
        </a-button>
      </a-space>
      <standard-table
        :columns="columns"
        :dataSource="dataSource"
        :selectedRows.sync="selectedRows"
        :rowKey="(record) => record.id"
        :expandedRowKeys="expandedRowKeys"
        @expand="expandinnerlist"
        :loading="tableloading"
        :pagination="false"
      >
        <span slot="restart_authorization" slot-scope="{ record }">
          <a-switch
            disabled="disabled"
            v-model="record.restart_authorization"
            :checked="record.restart_authorization === 0 ? true : false"
          />
        </span>
        <div slot="action" slot-scope="{ record }">
          <a @click="showModal(record)" style="margin-right: 8px">
            <a-icon type="edit" />修改
          </a>
          <a @click="showdeleConfirm(record.id)">
            <a-icon type="delete" />删除
          </a>
        </div>
      </standard-table>
      <a-pagination
        style="margin-top: 15px"
        v-model="query.page"
        :total="total"
        show-size-changer
        @showSizeChange="onShowSizeChange"
        :show-total="(total) => `一共 ${total} 条`"
        @change="pageonChange"
      />
      <!-- 表单 -->
      <a-modal
        v-model="visible"
        :title="tablename"
        on-ok="handleOk"
        :maskClosable="false"
        @afterClose="handleCancel()"
        :width="850"
      >
        <template slot="footer">
          <a-button key="back" @click="handleCancel"> 取消 </a-button>
          <a-button
            key="submit"
            type="primary"
            :loading="loading"
            @click="handleOk"
          >
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
            layout="vertical"
          >
            <a-row :gutter="16">
              <a-col :span="16">
                <a-form-model-item label="ip">
                  <a-input v-model="form.machine_ip" placeholder="输入框" />
                </a-form-model-item>
              </a-col>
            </a-row>

            <a-row :gutter="16">
              <a-col :span="16">
                <a-form-model-item label="范围">
                  <a-input
                    v-model="form.scope"
                    :value="form.scope"
                  />
                </a-form-model-item>
              </a-col>
            </a-row>

            <a-row :gutter="16">
              <a-col :span="16">
                <a-form-model-item label="是否启用">
                  <a-switch
                    v-model="form.restart_authorization"
                    :checked="form.restart_authorization ? true : false"
                  />
                </a-form-model-item>
              </a-col>
            </a-row>
          </a-form-model>
        </template>
      </a-modal>
      <!-- 权限修改表单 -->
      <a-modal
        v-model="permissionsvisible"
        :title="tablename"
        on-ok="permissionsOkhandleOk"
        :maskClosable="false"
        @afterClose="permissionshandleCancel()"
        :width="850"
      >
        <template slot="footer">
          <a-button key="back" @click="permissionshandleCancel">
            取消
          </a-button>
          <a-button
            key="submit"
            type="primary"
            :loading="permissionsloading"
            @click="permissionsOkhandleOk"
          >
            提交
          </a-button>
        </template>
        <template>
          <a-form-model
            ref="permissionsruleForm"
            :model="permissionsform"
            :rules="permissionsrules"
            :label-col="{ span: 6 }"
            :wrapper-col="{ span: 14 }"
            layout="vertical"
          >
          </a-form-model>
        </template>
      </a-modal>
    </div>
    <!-- 删除确认对话框 -->
    <a-modal
      title="系统消息"
      :visible="dialogvisible"
      ok-text="是"
      cancel-text="否"
      @ok="user_onok"
      @cancel="user_onno"
    >
      <p>是否删除</p>
    </a-modal>
  </a-card>
</template>

<script>
import StandardTable from "@/components/table/StandardTable";
import {MachineAdd, MachineDate, MachineDelete, MachineEdit} from "../../../services/machine";

const columns = [
  {title: "ip", dataIndex: "machine_ip"},
  {title: "范围", dataIndex: "scope"},
  {
    title: "是否启用",
    dataIndex: "restart_authorization",
    scopedSlots: {customRender: "restart_authorization"},
  },
  {title: "操作", scopedSlots: {customRender: "action"}},

];

const dataSource = [];
// const { RangePicker } = DatePicker;
export default {
  name: "QueryList",
  components: { StandardTable },
  data() {
    return {
      checked:true,
      disabled:false,
      dateFormat: "YYYY-MM-DD HH:mm:ss",
      query: {
        page: 1,
        page_size: 30,
        machine_ip: null,
      },
      form: {
        machine_ip: "",
        scope: "",
        restart_authorization: 0,
      },
      total: 0,
      advanced: true,
      columns: columns,
      dataSource: dataSource,
      selectedRows: [],
      ids: [],
      tableloading: false,
      ruleslist: [],
      departmentoptions: [],
      dialogvisible: false,
      tablename: "",
      visible: false,
      loading: false,
      id: "",
      permissionsloading: false,
      permissionsvisible: false,
      isdisabled: false,
      expandedRowKeys: [],
    };
  },
  created() {
    // this.getdepartmentoptions();
    this.gethearttabledata();
  },
  methods: {
    // 获取表格数据
    gethearttabledata() {
      this.tableloading = true;
      MachineDate(this.query).then((res) => {
        console.log(res);
        if (res.status === 200) {
          var re_da = res.data.data;
          this.dataSource = res.data.data;
          this.total = res.data.total;
          this.dataSource = re_da;
        } else {
          this.$message.error(`获取数据失败！`);
        }
        this.tableloading = false;
      });
    },
    async user_onok() {
      for (let i = 0; i < this.ids.length; i++) {
        await MachineDelete(this.ids[i]).then((res) => {
          if (res.status === 200) {
            this.$message.success(`删除成功！`);
          } else {
            this.$message.error(`删除失败！`);
          }
        });
      }
      const totalPage = Math.ceil((this.total - 1) / this.query.page_size);
      this.query.page =
        this.query.page > totalPage ? totalPage : this.query.page;
      this.query.page = this.query.page < 1 ? 1 : this.query.page;
      this.gethearttabledata();
      this.ids = [];
      this.dialogvisible = false;
    },
    async user_onno() {
      this.ids = [];
      this.dialogvisible = false;
    },
    toggleAdvanced() {
      this.advanced = !this.advanced;
    },
    // 查询
    queryevents() {
      this.query.page = 1;
      this.query.page_size = 30;
      this.gethearttabledata();
    },
    // 批量删除
    Batchdelete() {
      this.ids = [];
      for (let i = 0; i < this.selectedRows.length; i++) {
        this.ids.push(this.selectedRows[i].id);
      }
      this.dialogvisible = true;
    },

    // 打开编辑表单
    showModal(data) {
      this.form = {};
      if (data.id) {
        console.log(data);
        this.tablename = "编辑";
        this.isdisabled = true;

        // GetServiceNameDateOne(data.id).then((res) => {
        //   this.form = res.data.data;
        //   this.id = this.form.id;
        //   this.visible = true;
        //   console.log(this.form)
        // });
        // 替代方案
        this.form = data;
        this.visible = true;
      } else {
        this.tablename = "新增";
        this.isdisabled = false;
        this.visible = true;
      }
    },
    // 提交编辑表单
    handleOk() {
      this.$refs.ruleForm.validate((valid) => {
        if (valid) {
          // this.form.creator = localStorage.getItem("name");
          this.loading = true;
          this.tablename === "新增" ? this.addadta() : this.ediddata();
        }
      });
    },
    addadta() {
      MachineAdd(this.form).then((res) => {
        if (res.status === 200) {
          this.$message.success(`${this.tablename}成功！`);
          this.gethearttabledata();
          this.loading = false;
          this.visible = false;
        } else {
          this.$message.error(`${this.tablename}失败！`);
          this.loading = false;
        }
      });
    },
    // 编辑的提交
    ediddata() {
      MachineEdit(this.form).then((res) => {
        if (res.status === 200) {
          this.$message.success(`${this.tablename}成功！`);
          this.gethearttabledata();
          this.loading = false;
          this.visible = false;
        } else {
          this.$message.error(`${this.tablename}失败！`);
          this.loading = false;
        }
      });
    },

    // 提交权限编辑表单
    permissionsOkhandleOk() {
      this.$refs.permissionsruleForm.validate((valid) => {
        if (valid) {
          this.deleteuserrole(this.repermissionsform);
        }
      });
    },
    // 关闭权限编辑表单
    permissionshandleCancel() {
      this.permissionsvisible = false;
      this.$refs.permissionsruleForm.resetFields();
    },

    // 关闭编辑表单
    handleCancel() {
      this.visible = false;
      this.$refs.ruleForm.resetFields();
    },
    // 删除对话框
    showdeleConfirm(id) {
      this.ids.push(id);
      this.dialogvisible = true;
    },
    // 分页配置
    onShowSizeChange(current, pageSize) {
      this.query.page = 1;
      this.query.page_size = pageSize;
      this.gethearttabledata();
    },
    pageonChange(pageNumber) {
      this.query.page = pageNumber;
      this.gethearttabledata();
    },
    // 重置查询表单
    resettingqueryform() {
      for (var key in this.query) {
        this.query[key] = null;
      }
      this.query.page = 1;
      this.query.page_size = 30;
      this.gethearttabledata();
    },
    expandinnerlist(expanded, record) {
      if (this.expandedRowKeys.length > 0) {
        let index = this.expandedRowKeys.indexOf(record.id);
        if (index > -1) {
          this.expandedRowKeys.splice(index, 1);
        } else {
          this.expandedRowKeys.splice(0, this.expandedRowKeys.length);
          this.expandedRowKeys.push(record.id);
        }
      } else {
        this.expandedRowKeys.push(record.id);
      }
      this.innerData = record.task_set;
    },
  },
};
</script>

<style lang="less" scoped>
.search {
  margin-bottom: 54px;
}
.fold {
  width: calc(100% - 216px);
  display: inline-block;
}
.operator {
  margin-bottom: 18px;
}
@media screen and (max-width: 900px) {
  .fold {
    width: 100%;
  }
}
/deep/.ant-modal-footer {
  text-align: center;
}
.normal {
  background: #00cc00;
  -webkit-animation-name: breathe_normal;

}
.abnormal {
  background: yellow;
  -webkit-animation-name: breathe_abnormal;
}
.offline {
  background: gray;
  -webkit-animation-name: breathe_offline;
}
.light_frame{
  width: 15px;
  height: 15px;
  margin-left: 5px;
  border: 1px solid #2b92d4;
  border-radius: 50%;
  text-align: center;
  cursor: pointer;
  //margin:auto;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  -webkit-animation-timing-function: ease-in-out;
  -webkit-animation-duration: 1500ms;
  -webkit-animation-iteration-count: infinite;
  -webkit-animation-direction: alternate;
}
</style>
