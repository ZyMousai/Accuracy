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
                                <a-input v-model="query.uploadusers" style="width: 100%" placeholder="请输入"/>
                            </a-form-item>
                        </a-col>
                        <a-col :md="8" :sm="24">
                            <a-form-item
                                    label="上传日期"
                                    :labelCol="{span: 5}"
                                    :wrapperCol="{span: 18, offset: 1}"
                            >
                                <a-date-picker v-model="query.uploaddate" style="width: 100%" placeholder="请输入更新日期"/>
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
                    @clear="onClear"
                    @change="onChange"
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
                <template slot="statusTitle">
                    <a-icon @click.native="onStatusTitleClick" type="info-circle"/>
                </template>
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
                    title="您确定要删除吗？删除之后无法恢复！"
                    :visible="dialogvisible"
                    ok-text="是"
                    cancel-text="否"
                    @ok="onok"
                    @cancel="onno">
                <p style="color: darkred">请认真思考后再进行删除！</p>
            </a-modal>

            <!-- 恢复确认对话框 -->
            <a-modal
                    title="您确定要恢复吗？"
                    :visible="recovervisible"
                    ok-text="是"
                    cancel-text="否"
                    @ok="onokrecover"
                    @cancel="onnorecover">
                <p style="color: darkred">请认真思考后再进行恢复！</p>
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
                    filename: '',
                    uploadusers: '',
                    uploaddate: ''
                },
                total: 0,
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
            remove() {
                this.dataSource = this.dataSource.filter(item => this.selectedRows.findIndex(row => row.key === item.key) === -1)
                this.selectedRows = []
            },
            onClear() {
                this.$message.info('您清空了勾选的所有行')
            },
            onStatusTitleClick() {
                this.$message.info('你点击了状态栏表头')
            },
            onChange(current) {
                console.log(current);
                this.$message.info('表格状态改变了')
            },
            handleMenuClick(e) {
                if (e.key === 'delete') {
                    this.remove()
                }
            },
            // 查询
            queryevents() {
                this.gettabledata();
            },


            async onok() {
                let is_logic_del = '0';
                for (let i = 0; i < this.ids.length; i++) {
                    await RecycleDeleteDocuments(this.ids[i], is_logic_del).then(res => {
                        console.log(res);
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
                        console.log(res);
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
                    this.query[key] = ''
                }
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
