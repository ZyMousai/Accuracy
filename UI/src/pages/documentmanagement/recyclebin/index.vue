<template>
    <a-card>
        <div :class="advanced ? 'search' : null">
            <a-form layout="horizontal" :model="query">
                <div :class="advanced ? null: 'fold'">
                    <a-row>
                        <a-col :md="8" :sm="24">
                            <a-form-item
                                    label="文件名"
                                    :labelCol="{span: 5}"
                                    :wrapperCol="{span: 18, offset: 1}"
                            >
                                <a-input v-model="query.filename" placeholder="请输入"/>
                            </a-form-item>
                        </a-col>
                        <a-col :md="8" :sm="24">
                            <a-form-item
                                    label="上传用户"
                                    :labelCol="{span: 5}"
                                    :wrapperCol="{span: 18, offset: 1}"
                            >
                                <a-input v-model="query.user_name" style="width: 100%" placeholder="请输入"/>
                            </a-form-item>
                        </a-col>
                        <a-col :md="8" :sm="24">
                            <a-form-item
                                    label="开始时间"
                                    :labelCol="{span: 5}"
                                    :wrapperCol="{span: 18, offset: 1}"
                            >
                                <a-date-picker v-model="start_time" style="width: 100%" placeholder="请输入更新日期" format="YYYY-MM-DD"/>
                            </a-form-item>
                        </a-col>
                    </a-row>
                    <a-row>
                        <a-col :md="8" :sm="24">
                            <a-form-item
                                    label="结束时间"
                                    :labelCol="{span: 5}"
                                    :wrapperCol="{span: 18, offset: 1}"
                            >
                                <a-date-picker v-model="end_time" style="width: 100%" placeholder="请输入更新日期" format="YYYY-MM-DD"/>
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
                <a-button type="primary" @click="BatchRecover()">
                    <a-icon type="cloud-download"/>
                    批量恢复
                </a-button>
                <a-button type="primary" @click="Batchdelete()">
                    <a-icon type="delete"/>
                    批量删除
                </a-button>
                <span>小提示：回收站文件系统会至多保留7天</span>
            </a-space>
            <standard-table
                    :columns="columns"
                    :dataSource="dataSource"
                    :selectedRows.sync="selectedRows"
                    :rowKey='record=>record.id'
                    :pagination="false"
                    :loading="tableloading"
            >
                <div slot="description" slot-scope="{text}">
                    {{text}}
                </div>
                <div slot="action" slot-scope="{record}">
                    <a @click="recoverConfirm(record.id)" style="margin-right: 8px">
                        <a-icon type="cloud-download"/>
                        恢复
                    </a>
                    <a @click="showdeleConfirm(record.id)">
                        <a-icon type="delete"/>
                        彻底删除
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
            <!-- 删除确认对话框 -->
            <a-modal
                    title="系统消息"
                    :visible="dialogvisible"
                    ok-text="是"
                    cancel-text="否"
                    @ok="onok"
                    @cancel="onno">
                <p>您确定要删除吗？删除之后无法恢复！</p>
            </a-modal>

            <!-- 恢复确认对话框 -->
            <a-modal
                    title="系统消息"
                    :visible="recovervisible"
                    ok-text="是"
                    cancel-text="否"
                    @ok="onokrecover"
                    @cancel="onnorecover">
                <p>确定恢复此文件吗？</p>
            </a-modal>

        </div>
    </a-card>
</template>

<script>
    import StandardTable from '@/components/table/StandardTable'
    import {
        RecycleDocumentDate,
        RecycleDeleteDocuments,
        RecycleRecoverManagement
    } from '@/services/recyclebinmanagement'

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
            scopedSlots: {customRender: 'action'}
        }
    ];

    const dataSource = [];

    export default {
        name: 'QueryList',
        components: {StandardTable},
        data() {
            return {
                query: {
                    page: 1,
                    page_size: 10,
                    department_id: null,
                    filename: null,
                    user_name: null,
                    end_time: null,
                    start_time: null
                },
                total: 0,
                start_time: '',
                end_time: '',
                tableloading: false,
                advanced: true,
                columns: columns,
                dataSource: dataSource,
                selectedRows: [],
                dialogvisible: false,
                recovervisible: false,
                ids: [],
                headers: {
                    accept: 'application/json',
                    authorization: 'authorization-text',
                },
            }
        },
        created() {
            this.gettabledata()
        },
        methods: {
            // 获取表格数据
            gettabledata() {
                this.tableloading = true
                this.query.department_id = localStorage.getItem('department_id')
                RecycleDocumentDate(this.query).then(res => {
                    if (res.status === 200) {
                      console.log(res);
                      this.dataSource = res.data.data
                      this.total = res.data.total
                      console.log(this.total);
                      this.tableloading = false
                      // 给予序号
                      for (var i = 0; i < this.dataSource.length; i++) {
                          this.dataSource[i]["index"] = i + 1
                      }
                    } else {
                        this.tableloading = false
                        this.$message.error(`获取数据失败！`);
                    }
                })
            },
            toggleAdvanced() {
                this.advanced = !this.advanced
            },
            // 查询
            queryevents() {
                this.query.start_time = this.start_time ? this.start_time.format('YYYY-MM-DD') : null
                this.query.end_time = this.end_time ? this.end_time.format('YYYY-MM-DD') : null
                this.gettabledata();
            },
            async onok() {
                let is_logic_del = '0';
                for (let i = 0; i < this.ids.length; i++) {
                    await RecycleDeleteDocuments(this.ids[i], is_logic_del).then(res => {
                        if (res.status === 200) {
                          this.$message.success(`删除成功！`);
                        } else {
                          this.$message.error(`删除失败！`);
                        }
                    })
                }
                this.gettabledata();
                this.ids = [];
                this.dialogvisible = false
            },
            onno() {
                this.dialogvisible = false
            },

            async onokrecover() {
                for (let i = 0; i < this.ids.length; i++) {
                    await RecycleRecoverManagement(this.ids[i]).then(res => {
                        if (res.status === 200) {
                          this.$message.success(`恢复成功！`);
                        } else {
                          this.$message.error(`恢复失败！`);
                        }
                    })
                }
                this.gettabledata();
                this.ids = [];
                this.recovervisible = false
            },
            onnorecover() {
                this.recovervisible = false
            },

            // 批量恢复
            BatchRecover() {
                this.recovervisible = true;
                console.log(this.selectedRows);
                for (let i = 0; i < this.selectedRows.length; i++) {
                    this.ids.push(this.selectedRows[i].id)
                }
            },


            // 批量删除
            Batchdelete() {
                this.dialogvisible = true;
                console.log(this.selectedRows);
                for (let i = 0; i < this.selectedRows.length; i++) {
                    this.ids.push(this.selectedRows[i].id)
                }
            },
            // 重置查询表单
            resettingqueryform() {
                for (var key in this.query) {
                    this.query[key] = null
                }
                this.query.page = '1'
                this.query.page_size = '10'
                this.gettabledata()
            },
            // 删除对话框
            showdeleConfirm(id) {
                this.ids.push(id);
                this.dialogvisible = true
            },
            // 恢复对话框
            recoverConfirm(id) {
                this.ids.push(id);
                this.recovervisible = true
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
