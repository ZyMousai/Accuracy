<template>
    <a-card>
        <div :class="advanced ? 'search' : null">
            <a-form layout="horizontal" :model="query">
                <div :class="advanced ? null: 'fold'">
                    <a-row>
                        <a-col :md="8" :sm="24">
                            <a-form-item
                                    label="卡号查询"
                                    :labelCol="{span: 5}"
                                    :wrapperCol="{span: 18, offset: 1}"
                            >
                                <a-input v-model="query.card_number" placeholder="请输入卡号"/>
                            </a-form-item>
                        </a-col>

                        <a-col :md="8" :sm="24">
                            <a-form-item
                                    label="平台查询"
                                    :labelCol="{span: 5}"
                                    :wrapperCol="{span: 18, offset: 1}"
                            >
                                <a-input v-model="query.platform" placeholder="请输入平台"/>
                            </a-form-item>
                        </a-col>

                    </a-row>
                </div>
                <span style="float: right; margin-top: 3px;">
          <a-button type="primary" @click="queryevents">查询</a-button>
          <a-button style="margin-left: 8px" @click="resettingqueryform">重置</a-button>
          <a @click="toggleAdvanced" style="margin-left: 8px">
            {{advanced ? '收起' : '展开'}}
            <a-icon :type="advanced ? 'up' : 'down'"/>
          </a>
        </span>
            </a-form>
        </div>
        <div>
            <a-space class="operator">
                <a-upload
                        name="file"
                        :multiple="true"
                        :action="updocuurl"
                        :headers="headers"
                        :showUploadList="false"
                        :before-upload="beforeUpload"
                        @change="handleChange"
                >
                    <a-button type="primary">
                        <a-icon type="cloud-upload"/>
                        上传excel
                    </a-button>
                </a-upload>
                <a-button type="primary" @click="showModaluid">
                    <a-icon type="plus-circle" />
                    uid消耗与佣金查询
                </a-button>
                <a-button type="primary" @click="showaddcadrModaluid">
                    <a-icon type="plus-circle" />
                    新增单个卡号
                </a-button>
                <!-- <a-button type="primary" @click="Batchdelete()"><a-icon type="delete" />批量删除</a-button> -->
            </a-space>
            <a-table
              :columns="columns"
              :data-source="data"
              class="components-table-demo-nested"
              :rowKey='record=>record.id'
              :expandedRowKeys="expandedRowKeys"
              @expand="expandinnerlist"
              :pagination="false"
              :key="componentKey"
            >
                <!--        note-->

                <div slot="note" slot-scope="record">
                    <a-input
                            slot="note"
                            v-if="record.note_editable"
                            style="margin: -5px 0"
                            :value="text"
                            @change="e => handleChange(e.target.value, record.key, col)"
                    />
                    <template v-else>
                        {{ text }}
                    </template>
                </div>


                <div slot="cardstatus" slot-scope="record">
                    <a-switch slot="cardstatus" :loading="record.card_status_loading" default-checked
                              :checked="record.card_status ? true : false"
                              @change="record.card_status_loading=true;card_status_change(record.card_status, record.id)"/>
                </div>
                <div slot="retain_" slot-scope="record">
                    <a-switch slot="retain_" :loading="record.retain_loading" default-checked
                              :checked="record.retain ? true : false"
                              @change="record.retain_loading=true;retain_change(record.retain, record.id)"/>
                </div>
                <div slot="operation" slot-scope="record">
                    <a slot="operation" @click="edit(record)">编辑</a>
                    <a slot="operation" style="margin-left: 5px;" @click="table_delete(record.id)">删除</a>
                    <a slot="operation" style="margin-left: 5px;" @click="table_add(record.id)">新增子表</a>
                </div>
                <a-table
                        slot="expandedRowRender"
                        :columns="innerColumns"
                        :data-source="innerData"
                        :pagination="false"
                        :title="onHeaderCell"
                        :rowKey='record=>record.id'
                >
                    <div slot="secondary_consumption" slot-scope="record">
                        <a-switch slot="secondary_consumption" :loading="record.secondary_consumption_loading"
                                  default-checked
                                  :checked="record.secondary_consumption ? true : false"
                                  @change="
                        record.secondary_consumption_loading=true;
                        secondary_consumption_change(record.secondary_consumption, record.id);
                      "
                        />
                    </div>
                    <div slot="inneroperation" class="table-operation" slot-scope="record">
                        <a slot="inneroperation" @click="inneredit(record)">编辑</a>
                        <a slot="inneroperation" style="margin-left: 5px;" @click="innerdelete(record.id)">删除</a>
                    </div>
                </a-table>
            </a-table>
            <!-- 编辑表单 -->
            <a-modal v-model="visible" title="卡编辑" on-ok="handleOk" :maskClosable="false" @afterClose="handleCancel()">
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
                            :rules="editrules"
                            :label-col="{ span: 4 }"
                            :wrapper-col="{ span: 14 }"
                    >
                        <a-row :gutter="16">
                            <a-col :span="10">
                                <a-form-model-item ref="card_number" label="卡号" prop="creator">
                                    <a-input v-model="form.card_number" />
                                </a-form-model-item>
                            </a-col>
                            <a-col :span="10">
                                <a-form-model-item ref="valid_period" label="有效期" prop="creator">
                                    <a-input v-model="form.valid_period" />
                                </a-form-model-item>
                            </a-col>
                        </a-row>
                        <a-row :gutter="16">
                            <a-col :span="10">
                                <a-form-model-item ref="cvv" label="cvv" prop="creator">
                                    <a-input v-model="form.cvv" />
                                </a-form-model-item>
                            </a-col>
                            <a-col :span="10">
                                <a-form-model-item ref="face_value" label="面值" prop="creator">
                                    <a-input v-model="form.face_value" />
                                </a-form-model-item>
                            </a-col>
                        </a-row>
                        <a-row :gutter="16">
                            <a-col :span="10">
                                <a-form-model-item ref="name" label="卡姓名地址" prop="creator">
                                    <a-input v-model="form.name" />
                                </a-form-model-item>
                            </a-col>
                            <a-col :span="10">
                                <a-form-model-item ref="note" label="备注" prop="creator">
                                    <a-input v-model="form.note" />
                                </a-form-model-item>
                            </a-col>
                        </a-row>
                        <a-row :gutter="16">
                            <a-col :span="10">
                                <a-form-model-item ref="platform" label="平台" prop="creator">
                                    <a-input v-model="form.platform" />
                                </a-form-model-item>
                            </a-col>
                        </a-row>
                    </a-form-model>
                </template>
            </a-modal>
            <!-- 编辑表单 -->
            <a-modal v-model="innervisible" :title="taskname" on-ok="innerhandleOk" :maskClosable="false" @afterClose="innerhandleCancel()">
                <template slot="footer">
                    <a-button key="back" @click="innerhandleCancel">
                        取消
                    </a-button>
                    <a-button key="submit" type="primary" :loading="innerloading" @click="innerhandleOk">
                        提交
                    </a-button>
                </template>
                <template>
                    <a-form-model
                            ref="innerruleForm"
                            :model="innerform"
                            :rules="editrules"
                            :label-col="{ span: 4 }"
                            :wrapper-col="{ span: 14 }"
                    >
                        <a-row :gutter="32">
                            <!--              <a-col :span="10">-->
                            <!--                <a-form-model-item ref="uid" label="uuid" prop="creator">-->
                            <!--                  <a-input v-model="innerform.uid" />-->
                            <!--                </a-form-model-item>-->
                            <!--              </a-col>-->
                            <a-col :span="15">
                              <a-form-model-item ref="uid" label="UUID" prop="creator">
                                <a-select mode="tags" v-model="innerform.uid" placeholder="uuid" @click.native="uuidclick" @change="selecthandleChange">
                                  <!--                <a-select mode="tags" label="uuid" placeholder="uuid"  @change="selecthandleChange">-->
                                  <a-select-option v-for="item in uuidSelect" :key="item.id.toString()" :value="'uuid'+item.id.toString()">
                                      {{ item.uid }}
                                  </a-select-option>
                                </a-select>
                              </a-form-model-item>
<!--                              <a-button type="primary" :loading="innerloading" @click="searchTask">-->
<!--                                  搜索任务名-->
<!--                              </a-button>-->
                            </a-col>
                            <a-col :span="15">
                                <a-form-model-item ref="task" label="任务名" prop="creator">
                                    <a-input v-model="innerform.task" />
                                </a-form-model-item>
                            </a-col>
                        </a-row>
                        <a-row :gutter="16">
                            <a-col :span="15">
                                <a-form-model-item ref="commission" label="佣金" prop="creator">
                                    <a-input v-model="innerform.commission" />
                                </a-form-model-item>
                            </a-col>
                            <a-col :span="15">
                                <a-form-model-item ref="consume" label="消耗" prop="creator">
                                    <a-input v-model="innerform.consume" />
                                </a-form-model-item>
                            </a-col>
                        </a-row>
                        <a-row :gutter="16">
                            <a-col :span="15">
                                <a-form-model-item ref="user" label="使用人" prop="creator">
                                    <a-input v-model="innerform.user" />
                                </a-form-model-item>
                            </a-col>
                        </a-row>
                    </a-form-model>
                </template>
            </a-modal>
            <!-- 新增单个卡号表单 -->
            <a-modal v-model="addcadrvisible" title="新增号" on-ok="addcadrhandleOk" :maskClosable="false" @afterClose="addcadrhandleCancel()" :width='850'>
            <template slot="footer">
              <a-button key="back" @click="addcadrhandleCancel">
                取消
              </a-button>
              <a-button key="submit" type="primary" :loading="loading" @click="addcadrhandleOk">
                提交
              </a-button>
            </template>
            <template>
              <a-form-model
                ref="addcadrruleForm"
                :model="addcadrform"
                :rules="addcadrrules"
                :label-col="{ span: 6 }"
                :wrapper-col="{ span: 14 }"
                layout="vertical"
              >
              <a-row :gutter="16">
                <a-col :span="10">
                  <a-form-model-item ref="card_number" label="卡号" prop="card_number">
                    <a-input v-model="addcadrform.card_number" />
                  </a-form-model-item>
                </a-col>
                <a-col :span="10">
                  <a-form-model-item ref="name" label="持卡人姓名" prop="name">
                    <a-input v-model="addcadrform.name" />
                  </a-form-model-item>
                </a-col>
              </a-row>
              <a-row :gutter="16">
                <a-col :span="10">
                  <a-form-model-item ref="face_value" label="面值" prop="face_value">
                    <a-input v-model="addcadrform.face_value" />
                  </a-form-model-item>
                </a-col>
                <a-col :span="10">
                  <a-form-model-item ref="cvv" label="cvv" prop="cvv">
                    <a-input v-model="addcadrform.cvv" />
                  </a-form-model-item>
                </a-col>
              </a-row>
              <a-row :gutter="16">
                <a-col :span="10">
                  <a-form-model-item ref="valid_period" label="有效期" prop="valid_period">
                    <a-input v-model="addcadrform.valid_period" />
                  </a-form-model-item>
                </a-col>
                <a-col :span="10">
                  <a-form-model-item label="卡状态" prop="card_status">
                  <a-select v-model="addcadrform.card_status" placeholder="请选择卡状态">
                    <a-select-option v-for="item in card_statuslist" :key="item.vlaue" :value="item.vlaue">
                      {{item.name}}
                    </a-select-option>
                  </a-select>
                </a-form-model-item>
                </a-col>
              </a-row>
              <a-row :gutter="16">
                <a-col :span="10">
                  <a-form-model-item ref="platform" label="平台" prop="platform">
                    <a-input v-model="addcadrform.platform" />
                  </a-form-model-item>
                </a-col>
                <a-col :span="10">
                  <a-form-model-item ref="note" label="备注" prop="note">
                    <a-input v-model="addcadrform.note" />
                  </a-form-model-item>
                </a-col>
              </a-row>
              <a-row :gutter="16">
                <a-col :span="10">
                  <a-form-model-item ref="card_name" label="卡姓名地址" prop="card_name">
                    <a-input v-model="addcadrform.card_name" />
                  </a-form-model-item>
                </a-col>
                <a-col :span="10">
                  <a-form-model-item label="是否保留" prop="retain">
                  <a-select v-model="addcadrform.retain" placeholder="请选择是否保留">
                    <a-select-option v-for="item in card_statuslist" :key="item.vlaue" :value="item.vlaue">
                      {{item.name}}
                    </a-select-option>
                  </a-select>
                </a-form-model-item>
                </a-col>
              </a-row>
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
            <!-- 删除子表任务确认对话框 -->
            <a-modal
                    title="是否删除所选项？"
                    :visible="dialogvisibleson"
                    ok-text="是"
                    cancel-text="否"
                    @ok="onokson"
                    @cancel="onnoson">
                <p>删除后将无法恢复！</p>
            </a-modal>

            <!-- uid对应的消耗和佣金 -->
            <a-modal v-model="visibleuid" title="消耗和佣金" on-ok="handleOk" :maskClosable="false" @afterClose="handleCanceluid()" :width='850'>
                <template slot="footer">
                    <a-button key="back" @click="handleCanceluid">
                        取消
                    </a-button>
                    <a-button key="submit" type="primary" :loading="loading" @click="uidhandleOk">
                        提交
                    </a-button>
                </template>
                <template>
                    <a-form-model
                    :label-col="{ span: 6 }"
                    :wrapper-col="{ span: 14 }"
                    layout="vertical"
                    >
                            <!--ref="ruleForm"-->
                            <!--:model="form"-->
                            <!--:rules="rules"-->
                        <a-row :gutter="16">
                            <a-col :span="10">
                                <a-form-model-item ref="uid" label="uid" prop="uid">
                                    <a-input v-model="uid" />
                                </a-form-model-item>
                            </a-col>
                        </a-row>
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

                        <div>消耗：{{ this.consume }} <br> 佣金：{{ this.commission }}</div>
                    </a-form-model>
                </template>
            </a-modal>

            <!-- 分页组件 -->
<!--            <a-pagination-->
<!--                style="margin-top: 15px;"-->
<!--                v-model="query.page"-->
<!--                :total="total"-->
<!--                show-size-changer-->
<!--                @showSizeChange="onShowSizeChange"-->
<!--                :show-total="total => `一共 ${total} 条`"-->
<!--                @change="pageonChange" />-->
            <a-pagination
              v-model="current"
              :page-size-options="pageSizeOptions"
              :total="total"
              show-size-changer
              :page-size="pageSize"
              @showSizeChange="onShowSizeChange"
            >
              <template slot="buildOptionText" slot-scope="props">
                <span v-if="props.value !== '60'">{{ props.value }}条/页</span>
                <span v-if="props.value === '60'">全部</span>
              </template>
            </a-pagination>

        </div>
    </a-card>
</template>

<script>
    import {CreditCardListData} from '@/services/statisticscardinformation'
    import {
      PatchCardListData,
      PatchTaskListData,
      table_delete,
      innerdelete,
      CardAccountListData,
      CommissionConsumetion,
      AddCardAccount,
      AddCreditTask,
      AddOneCard,
      GetAccountTaskNameData
    } from "../../../services/statisticscardinformation";
    import Cookie from "js-cookie";

    const columns = [
        {title: '卡号', dataIndex: 'card_number', key: 'card_number'},
        {title: '有效期', dataIndex: 'valid_period', key: 'valid_period'},
        {title: 'cvv', dataIndex: 'cvv', key: 'cvv'},
        {title: '面值', dataIndex: 'face_value', key: 'face_value'},
        {title: '余额', dataIndex: 'balance', key: 'balance'},
        {title: '卡姓名地址', dataIndex: 'name', key: 'name'},
        {title: '备注', dataIndex: 'note', key: 'note'},
        // { title: '备注', dataIndex: 'note', scopedSlots: { customRender: 'note' },},
        {title: '平台', dataIndex: 'platform', key: 'platform'},
        {title: '卡状态', key: 'cardstatus', scopedSlots: {customRender: 'cardstatus'}},
        {title: '保留', key: 'retain_', scopedSlots: {customRender: 'retain_'}},
        {title: '创建时间', dataIndex: 'create_time', key: 'create_time'},
        {title: '操作', key: 'operation', scopedSlots: {customRender: 'operation'}},
    ];

    const data = [];

    const innerColumns = [
        { title: 'uuid', dataIndex: 'uid', key: 'uid' },
        { title: '任务', dataIndex: 'task', key: 'task', scopedSlots: { customRender: 'task' } },
        { title: '佣金', dataIndex: 'commission', key: 'commission', scopedSlots: { customRender: 'commission' } },
        { title: '消耗', dataIndex: 'consume', key: 'consume', scopedSlots: { customRender: 'consume' } },
        { title: '使用人', dataIndex: 'user', key: 'user', scopedSlots: { customRender: 'user' } },
        { title: '二次消费', key: 'secondary_consumption', scopedSlots: { customRender: 'secondary_consumption' } },
        { title: '使用日期', dataIndex: 'creation_date', key: 'creation_date' },
        { title: '操作', key: 'inneroperation', scopedSlots: { customRender: 'inneroperation' }},
    ];

    const innerData = [];

  export default {
    name: 'QueryList',
    data () {
      var checkMobile = (rule, value, callback) => {
        if (!value) {
          callback('请输入面值')
        } else {
          /[^\d]+/g.test(value) ? callback('必须是数字类型') : callback();
        }
      }
      this.cacheData = innerData.map(item => ({ ...item }));
      return {
        pageSizeOptions: ['50'],
        current: 1,
        pageSize: 50,
        total: 60,

        isRouterAlive: true,
        data,
        columns,
        innerColumns,
        innerData,
        query: {
          page: 1,
          page_size: 50,
          card_number: '',
          platform: '',
        },
        form: {
          uid: '',
          id: '',
          card_number: '',
          valid_period: '',
          cvv: '',
          face_value: '',
          name: '',
          platform: '',
          note: '',
        },
        innerform: {
          id: '',
          uid: '',
          account_id: '',
          card_id: '',
          task: '',
          commission: '',
          consume: '',
          user: '',
        },
        headers: {
          accept: 'application/json',
          authorization: 'authorization-text',
          token: Cookie.get('Authorization')
        },
        addcadrform: {
          card_number: '',
          face_value: '',
          valid_period: '',
          cvv: '',
          card_status: 1,
          name: '',
          platform: '',
          note: '',
          retain: 1,
          card_name: ''
        },
        start_time: '',
        end_time: '',
        uuidSelect: {},
        updocuurl: "",
        advanced: true,
        componentKey: 0,
        selectedRows: [],
        tablename: '',
        taskname: '',
        visible: false,
        visibleuid: false,
        innervisible: false,
        loading: false,
        innerloading: false,
        dialogvisible: false,
        dialogvisibleson: false,
        commission: '',
        consume: '',
        uid: '',
        ids: [],
        addcadrvisible: false,
        card_statuslist: [{vlaue: 1, name: '是'}, {vlaue: 0, name: '否'}],
        expandedRowKeys: [],
        editrules: {
          filename: [{ required: true, message: '请输入文件名', trigger: 'blur' }],
          department: [{ required: true, message: '请选择部门权限', trigger: 'change' }]
        },
        addcadrrules: {
          card_number: [{ required: true, message: '请输入卡号', trigger: 'blur' }],
          face_value: [{ required: true, validator: checkMobile, trigger: 'blur' }]
        },
        timer : {},
        editingKey: ''
      }
    },
    created () {
      this.gettabledata()
    },
    // 监听路由变化开启自动更新
    // watch: {
    //   $route: {
    //     handler: function(val){
    //       if (val.fullPath === '/assistantfunction/statisticscardinformation') {
    //         this.timer = setInterval(() => {
    //           this.gettabledata()
    //         }, 15000);
    //       } else {
    //         clearInterval(this.timer)
    //       }
    //     },
    //     immediate: true
    //   }
    // },
    methods: {
      gettabledata() {
        CreditCardListData(this.query).then(res => {
          var re_da = res.data.data;
          // 给予序号
          for (var i = 0; i < re_da.length; i++) {
            re_da[i]['create_time'] = re_da[i]['create_time'].split(' ')[0];
            re_da[i]["index"] = i + 1
            re_da[i]["card_status_loading"] = false
            re_da[i]["secondary_consumption_loading"] = false
            re_da[i]["retain_loading"] = false
            re_da[i]["note_editable"] = false
          }
          this.data = re_da
          this.total = res.data.total
          console.log(res);
          // this.componentKey = this.componentKey === 0 ? 1 : 0;
        })
      },
      toggleAdvanced () {
        this.advanced = !this.advanced
      },
      // 批量删除
      Batchdelete() {
        this.showdeleConfirm(this.selectedRows)
      },
      // 重置查询表单
      resettingqueryform() {
        for (var key in this.query) {
          this.query[key] = ''
        }
      },
      // 打开编辑表单
      showModal(id) {
        console.log(id);
        this.visible = true;
      },
      // 打开uid的消耗表单
      showModaluid(id) {
          console.log(id);
          this.visibleuid = true;
      },
      // 查询
      queryevents() {
        // this.query.page = 1
        // this.query.page_size = 10
        this.gettabledata()
      },
      // uid提交编辑表单
      uidhandleOk() {
        console.log(this.uid)
        console.log(this.start_time)
        console.log(this.end_time)
        var data = {
          "uid":this.uid,
          "start_time":this.start_time ? this.start_time.format('YYYY-MM-DD') : null,
          "end_time":this.end_time ? this.end_time.format('YYYY-MM-DD') : null
        }
        CommissionConsumetion(data).then(res =>{
            this.consume = res.data.total_consume;
            this.commission = res.data.total_commission;
        })
      },
      // 提交编辑表单
      handleOk() {
        this.$refs.ruleForm.validate(valid => {
          if (valid) {
            this.loading = true;
            PatchCardListData(this.form).then(res => {
              console.log("成功")
              console.log(res)
              this.loading = false;
              this.gettabledata()
              this.visible = false;
            })
            console.log('ok');
          }
        })
      },
      // 关闭编辑表单
      handleCancel() {
        this.visible = false;
        this.$refs.ruleForm.resetFields();
      },
      // 关闭uid编辑表单
      handleCanceluid() {
          this.visibleuid = false;
          this.$refs.ruleForm.resetFields();
          console.log('ok');
      },
      // 打开编辑表单
      innershowModal(id) {
        console.log(id);
        this.innervisible = true;
      },
      // 提交子表的编辑表单
      innerhandleOk() {
        this.$refs.innerruleForm.validate(valid => {
          // "secondary_consumption": 0
          if (valid) {
            this.innerloading = true;
            console.log(this.innerform)
            var addinnerform = {
              "card_id": this.innerform.card_id,
              "account_id": this.innerform.account_id,
              "task": this.innerform.task,
              "note": this.innerform.note,
              "commission": this.innerform.commission,
              "consume": this.innerform.consume,
              "user": this.innerform.user,
              "secondary_consumption": 0
            }
            if (this.innerform.uid.indexOf("uuid") != -1){
              console.log("uuid")
              console.log(this.innerform.uid)
              this.innerform.account_id = this.innerform.uid.split("uuid")[1]
              addinnerform["account_id"] = this.innerform.account_id
              if (this.taskname === "任务编辑"){
                PatchTaskListData(this.innerform).then(res => {
                  console.log("修改成功")
                  console.log(res)
                  // this.innerloading = false;
                  // this.gettabledata()
                  // this.innervisible = false;
                  location.reload()
                  // this.componentKey = this.componentKey === 0 ? 1 : 0;
                })
              } else {
                AddCreditTask(addinnerform).then(res => {
                  console.log("创建成功")
                  console.log(res)
                  // this.innerloading = false;
                  // this.gettabledata()
                  // this.innervisible = false;
                  location.reload()
                  // this.componentKey = this.componentKey === 0 ? 1 : 0;
                })
              }
            }else{
              console.log("uuid+++++")
              console.log(this.innerform.uid)
              AddCardAccount({uid: this.innerform.uid}).then(res => {
                console.log("创建成功")
                console.log(res)
                var id = res.data.data
                console.log(id)
                this.innerform.account_id = id
                addinnerform["account_id"] = id
                if (this.taskname === "任务编辑") {
                  PatchTaskListData(this.innerform).then(res => {
                    console.log("成功")
                    console.log(res)
                    // this.innerloading = false;
                    // this.gettabledata()
                    // this.innervisible = false;
                    location.reload()
                    // this.componentKey = this.componentKey === 0 ? 1 : 0;
                  })
                } else {
                  AddCreditTask(addinnerform).then(res => {
                    console.log("创建成功")
                    console.log(res)
                    // this.innerloading = false;
                    // this.gettabledata()
                    // this.innervisible = false;
                    location.reload()
                    // this.componentKey = this.componentKey === 0 ? 1 : 0;
                  })
                }
              })
            }
          }
        })
      },
      // 关闭编辑表单
      innerhandleCancel() {
        this.innervisible = false;
        this.$refs.innerruleForm.resetFields();
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
      // 修改主表卡状态
      card_status_change(card_status, id) {
        console.log(id);
        // id.loadingchanr = true
        PatchCardListData({card_status: card_status ? 0 : 1, id: id}).then(res => {
          console.log("成功")
          console.log(res)
          this.gettabledata()
        })
      },
      uuidclick(){
        // uuidSelect
        CardAccountListData().then(res => {
          var re_da = res.data.data;
          this.uuidSelect = re_da
          console.log(res)
        })
      },
      // 修改子表二次消费状态
      secondary_consumption_change(secondary_consumption, id) {
        console.log(id);
        PatchTaskListData({secondary_consumption: secondary_consumption ? 0 : 1, id: id}).then(res => {
          console.log("成功")
          console.log(res)
          // this.gettabledata()
          //此处未完成，需要刷新子表，或重新展开，暂定刷新页面
          location.reload()
          // this.componentKey = this.componentKey === 0 ? 1 : 0;
        })
      },
      // 修改主表是否保留
      retain_change(retain, id) {
        console.log(retain)
        PatchCardListData({retain: retain ? 0 : 1, id: id}).then(res => {
          // console.log("成功")
          console.log(res)
          this.gettabledata()

        })
      },
      // 上传文件
      handleChange(info) {
        if (info.file.status !== 'uploading') {
          console.log("uploading")
          console.log(info.file, info.fileList);
        }
        if (info.file.status === 'done') {
          console.log("done")
          // AddCardsExcel(info.file.name).then(res => {
          //   // console.log("成功")
          //   console.log(res)
          //   this.gettabledata()
          //
          // })
          this.$message.success(`${info.file.name} file uploaded successfully`);
        } else if (info.file.status === 'error') {
          console.log("error")
          this.$message.error(`${info.file.name} file upload failed.`);
        }
      },
      beforeUpload() {
        // this.alone = process.env.VUE_APP_API_ALONE_URL
        this.updocuurl = process.env.VUE_APP_API_BASE_URL + `/Clerk/card/v1/cards/excel`
      },
      selecthandleChange(data){
        console.log(data[0])
        if (data[0] != undefined){
          this.innerform.uid = data[0]
          console.log(this.innerform.uid)
          if (this.innerform.uid.indexOf("uuid") != -1){
            console.log("uuid")
            console.log(this.innerform.uid)
            this.innerform.account_id = this.innerform.uid.split("uuid")[1]
            GetAccountTaskNameData({"account_id": this.innerform.account_id}).then(res => {
              try {
                this.innerform.task = res.data.data.task
              }catch{
                this.innerform.task = ""
              }
            })
          }else{
            console.log("uuid+++++")
            console.log(this.innerform.uid)
            AddCardAccount({uid: this.innerform.uid}).then(res => {
              console.log("创建成功")
              console.log(res)
              var id = res.data.data
              console.log(id)
              this.innerform.account_id = id
              GetAccountTaskNameData({"account_id": this.innerform.account_id}).then(res => {
                try {
                this.innerform.task = res.data.data.task
              }catch{
                this.innerform.task = ""
              }
              })
            })
          }
        }

      },
      edit (data){
        console.log(data)
        this.form.id = data.id
        this.form.card_number = data.card_number
        this.form.valid_period = data.valid_period
        this.form.card_id = data.card_id
        this.form.cvv = data.cvv
        this.form.face_value = data.face_value
        this.form.name = data.name
        this.form.platform = data.platform
        this.form.note = data.note
        this.visible = true;

      },
      // 子表添加按钮
      onHeaderCell() {
      //   return (
      //           <div style="text-align:left">
      //           <a-button onClick={this.inneredit} size="small">新增数据</a-button>
      //           </div>
      // )
      },
      innerhandleChange(value, id, column) {
        const newData = [...this.innerData];
        console.log(newData);
        const target = newData.filter(item => id === item.id)[0];
        if (target) {
          target[column] = value;
          this.innerData = newData;
        }
      },
      //显示新增子表的模态框
      table_add(id){
        console.log(id)
        this.taskname = '任务新增'
        this.innervisible = true;
        this.innerform.card_id= id
        this.innerform.uid = []
        this.innerform.account_id = ""
        this.innerform.task = ""
        this.innerform.commission = ""
        this.innerform.consume = ""
        this.innerform.user = ""
        console.log(this.innerform);
      },
      //修改子表
      inneredit(data) {
        // const newData = [...this.innerData];
        // console.log(newData);
        // const target = newData.filter(item => id === item.id)[0];
        // console.log(target);
        // this.editingKey = id;
        // if (target) {
        //   target.editable = true;
        //   this.innerData = newData;
        // }
        // console.log(this.innerData);
        console.log(data);
        this.innervisible = true;
        // console.log("任务编辑")
        this.taskname = "任务编辑"
        this.innerform.id = data.id
        this.innerform.uid = data.uid
        this.innerform.account_id = data.account_id
        this.innerform.card_id = data.card_id
        this.innerform.task = data.task
        this.innerform.commission = data.commission
        this.innerform.consume = data.consume
        this.innerform.user = data.user
      },
      innersave(id) {
          const newData = [...this.innerData];
          const newCacheData = [...this.cacheData];
          const target = newData.filter(item => id === item.id)[0];
          const targetCache = newCacheData.filter(item => id === item.id)[0];
          if (target && targetCache) {
              delete target.editable;
              this.innerData = newData;
              Object.assign(targetCache, target);
              this.cacheData = newCacheData;
          }
          this.editingKey = '';
      },
      innercancel(id) {
          const newData = [...this.innerData];
          const target = newData.filter(item => id === item.id)[0];
          this.editingKey = '';
          if (target) {
              Object.assign(target, this.cacheData.filter(item => id === item.id)[0]);
              delete target.editable;
              this.innerData = newData;
          }
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
          this.innerData = record.task_set
      },
      // 子表删除
      innerdelete(id) {
          this.ids.push(id);
          console.log(this.ids);
          this.dialogvisibleson = true;
      },
      // 主表删除
      table_delete(id) {
          this.ids.push(id);
          console.log(this.ids);
          this.dialogvisible = true;
      },
      async onok() {
          for (let i = 0; i < this.ids.length; i++) {
              await table_delete(this.ids[i]).then(res => {
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
          this.gettabledata()
          this.ids = []
          this.dialogvisible = false
      },


      async onokson() {
          for (let i = 0; i < this.ids.length; i++) {
              await innerdelete(this.ids[i]).then(res => {
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
          this.gettabledata()
          this.ids = []
          this.dialogvisibleson = false
      },

      onno() {
          this.ids = [];
          this.dialogvisible = false
      },

      onnoson() {
          this.ids = [];
          this.dialogvisibleson = false
      },

      // 分页配置
      onShowSizeChange(current, pageSize) {
          // this.query.page = 1
          this.query.page_size = pageSize
          this.gettabledata()
      },
      pageonChange(pageNumber) {
          this.query.page = pageNumber
          this.gettabledata()
      },
      showaddcadrModaluid() {
        this.addcadrvisible = true
      },
      addcadrhandleOk() {
        console.log(this.addcadrform);
        this.$refs.addcadrruleForm.validate(valid => {
          if (valid) {
            this.loading = true
            AddOneCard(this.addcadrform).then(res => {
              if (res.status === 200) {
                this.$message.success('添加成功！')
                this.addcadrhandleCancel()
                this.gettabledata()
                this.loading = false
              } else {
                this.$message.success('添加失败！')
                this.loading = false
              }
            })
          }
        })
      },
      addcadrhandleCancel() {
        this.addcadrvisible = false
        this.$refs.addcadrruleForm.resetFields();
      },
    }
  }
</script>

<style lang="less" scoped>
    .search {
        margin-bottom: 54px;
    }

    .fold {
        width: calc(100% - 216px);
        display: inline-block
    }

    .operator {
        margin-bottom: 18px;
    }

    @media screen and (max-width: 900px) {
        .fold {
            width: 100%;
        }
    }
</style>
