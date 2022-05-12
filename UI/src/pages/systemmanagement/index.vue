<template>
  <a-card>
    <div :class="advanced ? 'search' : null">
      <a-form layout="horizontal" :model="query">
        <div :class="advanced ? null : 'fold'">
          <a-row>
            <a-col :md="8" :sm="24">
              <a-form-item
                label="服务名"
                :labelCol="{ span: 5 }"
                :wrapperCol="{ span: 18, offset: 1 }"
              >
                <a-input v-model="query.job_name" placeholder="服务名" />
              </a-form-item>
            </a-col>
            <a-col :md="8" :sm="24">
              <a-form-item
                label="创建时间"
                :labelCol="{ span: 5 }"
                :wrapperCol="{ span: 18, offset: 1 }"
              >
                <a-date-picker
                  style="width: 90%"
                  v-model="query.start_create_time"
                  placeholder="请输入开始时间"
                  :value-format="dateFormat"
                  :format="dateFormat"
                />
              </a-form-item>
            </a-col>
            <a-col :md="8" :sm="24">
              <a-form-item
                style="margin-left: -30px"
                :labelCol="{ span: 5 }"
                :wrapperCol="{ span: 18, offset: 1 }"
              >
                <a-date-picker
                  style="width: 90%"
                  v-model="query.end_create_time"
                  placeholder="请输入结束时间"
                  :value-format="dateFormat"
                  :format="dateFormat"
                />
              </a-form-item>
            </a-col>
          </a-row>
          <a-row>
            <a-col :md="8" :sm="24">
              <a-form-item
                label="是否启用"
                :labelCol="{ span: 5 }"
                :wrapperCol="{ span: 18, offset: 1 }"
              >
                <a-select v-model="query.alarm" placeholder="请选择">
                  <a-select-option
                    v-for="item in alarm_select"
                    :key="item[1]"
                    :value="item[1]"
                  >
                    {{ item[0] }}
                  </a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :md="8" :sm="24">
              <a-form-item
                label="状态"
                :labelCol="{ span: 5 }"
                :wrapperCol="{ span: 18, offset: 1 }"
              >
                <a-select v-model="query.state" placeholder="请选择">
                  <a-select-option
                    v-for="item in state_select"
                    :key="item[1]"
                    :value="item[1]"
                  >
                    {{ item[0] }}
                  </a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
          </a-row>
        </div>
        <span style="float: right; margin-top: 3px">
          <a-button type="primary" @click="queryevents">查询</a-button>
          <a-button style="margin-left: 8px" @click="resettingqueryform"
            >重置</a-button
          >
          <a @click="toggleAdvanced" style="margin-left: 8px">
            {{ advanced ? "收起" : "展开" }}
            <a-icon :type="advanced ? 'up' : 'down'" />
          </a>
        </span>
      </a-form>
    </div>
    <div>
      <a-space class="operator">
        <a-button type="primary" @click="showModal"
          ><a-icon type="plus-circle" />新增</a-button
        >
        <a-button type="primary" @click="Batchdelete()"
          ><a-icon type="delete" />批量删除</a-button
        >
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
        <span slot="alarm" slot-scope="{ record }">
          <a-switch
            disabled="disabled"
            v-model="record.alarm"
            :checked="record.alarm === 0 ? true : false"
          />
        </span>
        <!-- <div slot="alarm" slot-scope="{ record }">
          <div v-if="record.alarm === 0">否</div>
          <div v-else>是</div>
        </div> -->
        <div slot="state" slot-scope="{ record }">
          <!-- 这里可以替换成指示灯 -->
          <div v-if="record.state === 0" class="normal light_frame"></div>
          <div v-else-if="record.state === 1" class="abnormal light_frame"></div>
          <div v-else class="offline light_frame"></div>
        </div>
        <div slot="interval" slot-scope="{ record }">
          {{ record.interval }} 分钟
        </div>

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
            <a-row :gutter="16" v-if="this.tablename === '新增'">
              <a-col :span="16">
                <a-form-model-item label="服务名">
                  <a-input v-model="form.job_name" placeholder="输入框" />
                </a-form-model-item>
              </a-col>
            </a-row>
            <a-row :gutter="16">
              <a-col :span="16">
                <a-form-model-item label="是否启用">
                  <a-switch
                    v-model="form.alarm"
                    :checked="form.alarm ? true : false"
                  />
                </a-form-model-item>
              </a-col>
            </a-row>
            <a-row :gutter="16">
              <a-col :span="16">
                <a-form-model-item label="心跳间隔">
                  <a-input-number
                    v-model="form.interval"
                    :value="form.interval"
                  />分钟
                </a-form-model-item>
              </a-col>
            </a-row>

            <a-row :gutter="16">
              <a-col :span="16">
                <a-form-model-item label="被@人手机号(英文逗号分割，设为all代表全部)">
                  <a-input
                    v-model="form.at"
                    :value="form.at"
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
      <p>是否删除所选服务，并停止对该服务的监测！</p>
    </a-modal>
  </a-card>
</template>

<script>
import StandardTable from "@/components/table/StandardTable";
import { GetServiceNameDate, GetServiceNameDateOne } from "@/services/systemmanagement";
import {
  AddHeartbeatDisplay,
  DeleteHeartbeatDisplay,
  // GetServiceNameDateOne,
  PatchHeartbeatDisplay,
} from "../../services/systemmanagement";

const columns = [
  {title: "id", dataIndex: "id"},
  {title: "服务名", dataIndex: "job_name"},
  {title: "断开时报警时间", dataIndex: "heartbeat_alarm"},
  {title: "创建时间", dataIndex: "create_time"},
  {title: "上次心跳", dataIndex: "last_heartbeat"},
  {
    title: "是否启用",
    dataIndex: "alarm",
    scopedSlots: {customRender: "alarm"},
  },
  {title: "状态", dataIndex: "state", scopedSlots: {customRender: "state"}},
  {
    title: "心跳间隔",
    dataIndex: "interval",
    scopedSlots: {customRender: "interval"},
  },
  {title: "操作", scopedSlots: {customRender: "action"}},
  // {title: "钉钉通知人", dataIndex: "at",colSpan:0,width:0},

];

const dataSource = [];
// const { RangePicker } = DatePicker;
export default {
  name: "QueryList",
  components: { StandardTable },
  data() {
    var checkMobile = (rule, value, cb) => {
      console.log(value);
      const regMobile =
        /^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/;
      if (regMobile.test(value)) {
        // 合法的手机号码
        return cb();
      }
      cb(new Error("手机号码格式不正确"));
    };
    return {
      checked:true,
      disabled:false,
      dateFormat: "YYYY-MM-DD HH:mm:ss",
      query: {
        page: 1,
        page_size: 10,
        start_create_time: null,
        end_create_time: null,
        job_name: null,
        alarm: null,
        state: null,
      },
      form: {
        job_name: "",
        create_time: "",
        last_heartbeat: "",
        heartbeat_alarm: "",
        at: "",
        interval: 0,
        alarm: 0,
        state: 0,
      },
      total: 0,
      advanced: true,
      columns: columns,
      dataSource: dataSource,
      selectedRows: [],
      ids: [],
      tableloading: false,
      genderlist: [
        ["男", "true"],
        ["女", "false"],
      ],
      ruleslist: [],
      alarm_select: [
        ["是", 0],
        ["否", 1],
      ],
      state_select: [
        ["正常", 0],
        ["异常", 1],
        ["离线", 2],
      ],
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
      permissionsform: {
        role_id: "",
        department_id: "",
      },
      repermissionsform: {
        role_id: "",
        department_id: "",
      },
      permissionsrules: {
        department_id: [
          { required: true, message: "请选择部门", trigger: "change" },
        ],
        role_id: [{ required: true, message: "请选择角色", trigger: "change" }],
      },
      rules: {
        account: [{ required: true, message: "请输入用户名", trigger: "blur" }],
        name: [{ required: true, message: "请输入姓名", trigger: "blur" }],
        gender: [{ required: true, message: "请选择性别", trigger: "change" }],
        department_id: [
          { required: true, message: "请选择部门", trigger: "change" },
        ],
        role_id: [{ required: true, message: "请选择角色", trigger: "change" }],
        entry_time: [
          { required: true, message: "请选择入职时间", trigger: "change" },
        ],
        phone: [
          { required: true, message: "请填写手机号", trigger: "blur" },
          { validator: checkMobile, rtigger: "blur" },
        ],
        address: [{ required: true, message: "请输入用户名", trigger: "blur" }],
        birth: [
          { required: true, message: "请选择入职时间", trigger: "change" },
        ],
        condition: [
          { required: true, message: "请选择心跳间隔", trigger: "blur" },
        ],
      },
    };
  },
  created() {
    // this.getdepartmentoptions();
    this.gethearttabledata();
  },
  methods: {
    // 获取心跳表格数据
    gethearttabledata() {
      this.tableloading = true;
      GetServiceNameDate(this.query).then((res) => {
        console.log(res);
        if (res.status === 200) {
          var re_da = res.data.data;
          this.dataSource = res.data.data;
          this.total = res.data.total;
          console.log(this.total);
          console.log("ti");
          //年
          let year = new Date().getFullYear();
          console.log(year)
          //月份是从0月开始获取的，所以要+1;
          let month = (new Date().getMonth() +1).toString().padStart(2,0);
          console.log(month)
          //日
          let day = (new Date().getDate()).toString().padStart(2,0);
          console.log(day)
          console.log("ti");
          this.tableloading = false;
          for (var i = 0; i < re_da.length; i++) {
            // 时间格式转换
            var heartbeat_alarm = re_da[i]["heartbeat_alarm"];
            if (heartbeat_alarm != null) {
              re_da[i]["heartbeat_alarm"] = heartbeat_alarm.replace("T", " ");
            }
            var last_heartbeat = re_da[i]["last_heartbeat"];
            if (last_heartbeat != null) {
              if (last_heartbeat.includes(year + '-' + month + '-' + day)){
                re_da[i]["last_heartbeat"] = last_heartbeat.replace(year + '-' + month + '-' + day + "T", "");
              // }else if(last_heartbeat.includes(year + '-' + month)){
              //   re_da[i]["last_heartbeat"] = last_heartbeat.replace(year + '-' + month + '-', "").replace("T", " ");
              }else if(last_heartbeat.includes(year)){
                re_da[i]["last_heartbeat"] = last_heartbeat.replace(year + '-', "").replace("T", " ");
              }else {
                re_da[i]["last_heartbeat"] = last_heartbeat.replace("T", " ");
              }

            }
            re_da[i]["create_time"] = re_da[i]["create_time"].replace("T", " ");
            // 时间格式转换（使用插件moment）
            // re_da[i]["heartbeat_alarm"] = this.$moment(re_da[i]["heartbeat_alarm"]
            // ).format("YYYY-MM-DD HH:mm:ss");
            // re_da[i]["create_time"] = this.$moment(re_da[i]["create_time"]
            // ).format("YYYY-MM-DD HH:mm:ss");
            // re_da[i]["index"] = i + 1;
            // if (re_da[i]["alarm"] == 0) {
            //   this.alarmswitch=true;
            // }else{
            //   this.alarmswitch=false;
            // }
          }
          this.dataSource = re_da;
        } else {
          this.tableloading = false;
          this.$message.error(`获取数据失败！`);
        }
      });
    },
    async user_onok() {
      for (let i = 0; i < this.ids.length; i++) {
        await DeleteHeartbeatDisplay(this.ids[i]).then((res) => {
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
      this.query.page_size = 10;
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

        GetServiceNameDateOne(data.id).then((res) => {
          this.form = res.data.data;
          this.id = this.form.id;
          this.visible = true;
          console.log(this.form)
        });
        // // 替代方案
        // this.form = data;
        // this.visible = true;
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
      AddHeartbeatDisplay(this.form).then((res) => {
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
      PatchHeartbeatDisplay(this.form).then((res) => {
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
      this.query.page_size = 10;
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
@-webkit-keyframes breathe_normal {
    0% { opacity: .4; box-shadow: 0 1px 2px rgba(22, 223, 0, 0.4), 0 1px 1px rgba(41, 223, 0, 0.1) inset; }
    100% {
        opacity: .8; border: 1px solid rgba(59, 235, 68, 0.7);
        box-shadow: 0 1px 10px #71ff3c, 0 1px 10px #30ff00 inset;
    }
}
@-webkit-keyframes breathe_abnormal {
    0% { opacity: .4; box-shadow: 0 1px 2px rgba(223, 193, 0, 0.4), 0 1px 1px rgba(223, 175, 0, 0.1) inset; }
    100% {
        opacity: .8; border: 1px solid rgba(235, 197, 59, 0.7);
        box-shadow: 0 1px 10px #fff64a, 0 1px 10px #f5ff00 inset;
    }
}
@-webkit-keyframes breathe_offline {
    0% { opacity: .4; box-shadow: 0 1px 2px rgba(139, 139, 139, 0.4), 0 1px 1px rgba(229, 248, 255, 0.1) inset; }
    100% {
        opacity: .8; border: 1px solid rgba(182, 182, 182, 0.7);
        box-shadow: 0 1px 10px #d5d5d5, 0 1px 10px #bfbfbf inset;
    }
}
</style>
