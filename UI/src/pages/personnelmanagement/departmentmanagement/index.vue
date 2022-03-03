<template>
    <a-card>
        <div :class="advanced ? 'search' : null">
            <a-form layout="horizontal" :model="query">
                <div :class="advanced ? null: 'fold'">
                    <a-row>
                        <a-col :md="8" :sm="24">
                            <a-form-item
                                    label="部门名称"
                                    :labelCol="{span: 5}"
                                    :wrapperCol="{span: 18, offset: 1}"
                            >
                                <a-input v-model="query.department" placeholder="请输入"/>
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
                <a-button type="primary" @click="adddepartment">
                    <a-icon type="plus-circle"/>
                    新增
                </a-button>
                <a-button type="primary" @click="Batchdelete()">
                    <a-icon type="delete"/>
                    批量删除
                </a-button>
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
                    <a @click="editdepartment(record.id)" style="margin-right: 8px">
                        <a-icon type="edit"/>
                        修改
                    </a>
                    <a @click="showdeleConfirm(record.id)">
                        <a-icon type="delete"/>
                        删除
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
                    title="您确定要删除吗？不可恢复噢！"
                    :visible="dialogvisible"
                    ok-text="是"
                    cancel-text="否"
                    @ok="onok"
                    @cancel="onno">
                <p style="color: darkred">请认真思考后再进行删除噢！</p>
            </a-modal>

        </div>
    </a-card>
</template>

<script>
    import StandardTable from '@/components/table/StandardTable'
    import {DepartmentDate, DeleteDepartment} from '@/services/personnelmanagement'

    const columns = [
        {
            title: '序号',
            dataIndex: 'index'
        },
        {
            title: '部门名称',
            dataIndex: 'department'
        },
        {
            title: '创建人',
            dataIndex: 'creator'
        },
        {
            title: '创建时间',
            dataIndex: 'create_time'
        },
        {
            title: '操作',
            scopedSlots: {customRender: 'action'}
        }
    ]

    const dataSource = []
    export default {
        name: 'QueryList',
        components: {StandardTable},
        data() {
            return {
                query: {
                    page: 1,
                    page_size: 10,
                    department: ''
                },
                total: 0,
                tableloading: false,
                advanced: true,
                columns: columns,
                dataSource: dataSource,
                selectedRows: [],
                dialogvisible: false,
                ids: [],
                departmentoptions: ['商务', "技术"],
                headers: {
                    accept: 'application/json',
                    authorization: 'authorization-text',
                }
            }
        },
        created() {
            this.gettabledata()
        },
        // 监听路由变化
        watch: {
          $route: {
            handler: function(val){
              if (val.fullPath === '/personnelmanagement/departmentmanagement') {
                this.gettabledata()
              }
            },
            immediate: true
          }
        },
        methods: {
            // 获取表格数据
            gettabledata() {
                this.tableloading = true
                DepartmentDate(this.query).then(res => {
                    if (res.status === 200) {
                      this.dataSource = res.data.data
                      this.total = res.data.total
                      this.tableloading = false
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
            handleMenuClick(e) {
                if (e.key === 'delete') {
                    this.remove()
                }
            },
            // 查询
            queryevents() {
                this.gettabledata();
            },
            // 批量删除
            Batchdelete() {
                this.dialogvisible = true;
                console.log(this.selectedRows);
                for (let i = 0; i < this.selectedRows.length; i++) {
                    this.ids.push(this.selectedRows[i].id)
                }
            },
            async onok() {
                for (let i = 0; i < this.ids.length; i++) {
                    await DeleteDepartment(this.ids[i]).then(res => {
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
                this.dialogvisible = false
            },
            // 重置查询表单
            resettingqueryform() {
                for (var key in this.query) {
                    this.query[key] = ''
                }
                this.query.page = 1
                this.query.page_size = 10
                this.gettabledata()
            },
            // 新增角色
            adddepartment() {
                this.$router.push('/personnelmanagement/adddepartment')
            },
            // 编辑角色
            editdepartment(id) {
                this.$router.push('/personnelmanagement/editdepartment/?' + id)
            },
            // 删除对话框
            showdeleConfirm(id) {
                this.ids.push(id);
                this.dialogvisible = true
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
