<template>
  <a-card>
    <div :class="advanced ? 'search' : null">
      <a-form layout="horizontal" :model="query">
        <div :class="advanced ? null: 'fold'">
          <a-row >
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="Offer链接"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-input v-model="query.url" placeholder="请输入" />
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="设备类型"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-select v-model="query.platform" placeholder="请选择">
                <a-select-option v-for="item in devicetypelist" :key="item" :value="item">
                  {{item}}
                </a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :md="8" :sm="24" >
            <a-form-item
              label="国家"
              :labelCol="{span: 5}"
              :wrapperCol="{span: 18, offset: 1}"
            >
              <a-select v-model="query.country" placeholder="请选择">
                <a-select-option v-for="item in countrylist" :key="item" :value="item">
                  {{item}}
                </a-select-option>
              </a-select>
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
      <standard-table
        :columns="columns"
        :dataSource="dataSource"
        :selectedRows.sync="selectedRows"
        @clear="onClear"
        @change="onChange"
        :rowKey='record=>record.index'
      >
      </standard-table>
    </div>
  </a-card>
</template>

<script>
import StandardTable from '@/components/table/StandardTable'
import {FollowLinkDate} from '@/services/followlink'
const columns = [
  {
    title: '序号',
    dataIndex: 'index',
    width: 80
  },
  {
    title: '耗时',
    dataIndex: 'loadTime',
    width: 80
  },
  {
    title: '状态',
    dataIndex: 'code',
    width: 80
  },
  {
    title: '追踪链接',
    dataIndex: 'url'
  },
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
        url: '',
        platform: '',
        country: '',
      },
      advanced: true,
      columns: columns,
      dataSource: dataSource,
      selectedRows: [],
      departmentoptions: ['iphone', "android", "ipad", "desktop"],
      devicetypelist: ['iphone', "android", "ipad", "desktop"],
      countrylist: ['jp', "us", "tw", "gb", "de"],
    }
  },
  methods: {
    // 获取表格数据
    gettabledata () {
      FollowLinkDate(this.query).then(res => {
        for (let i = 0; i < res.data.urls.length; i++) {
          res.data.urls[i]['index'] = i + 1
        }
        this.dataSource = res.data.urls
      })
    },
    toggleAdvanced () {
      this.advanced = !this.advanced
    },
    onClear() {
      this.$message.info('您清空了勾选的所有行')
    },
    onChange() {
      this.$message.info('表格状态改变了')
    },
    // 查询
    queryevents() {
      this.gettabledata()
    },
    // 重置查询表单
    resettingqueryform() {
      for(var key in this.query) {
        this.query[key] = ''
      }
      this.query.page = '1'
      this.query.page_size = '10'
      this.dataSource = []
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
