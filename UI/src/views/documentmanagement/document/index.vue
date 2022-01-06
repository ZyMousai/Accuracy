<template>
  <div class="app-container">
    <!--      搜索添加区域-->
      <div style="margin-bottom: 15px">
        <el-row :gutter="20">
        <el-col :span="5">
          <el-input v-model="queryinfo.name" clearable placeholder="名字" @keyup.enter.native="search"></el-input>
        </el-col>
        <el-col :span="5">
          <el-input v-model="queryinfo.user" clearable placeholder="上传用户" @keyup.enter.native="search"></el-input>
        </el-col>
        <el-col :span="5">
        <el-date-picker
          v-model="datedata"
          type="daterange"
          align="right"
          unlink-panels
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期">
        </el-date-picker>
        </el-col>
        <el-col :span="8">
          <el-button type="primary">搜索</el-button>
          <el-button type="primary">批量上传</el-button>
          <el-button type="primary">批量下载</el-button>
          <el-button type="primary">批量删除</el-button>
        </el-col>
      </el-row>
      </div>
    <el-table
      v-loading="listLoading"
      :data="list"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
    >
      <el-table-column align="center" label="序号" width="95">
        <template slot-scope="scope">
          {{ scope.$index }}
        </template>
      </el-table-column>
      <el-table-column align="center" prop="created_at" label="上传时间" width="200">
        <template slot-scope="scope">
          <i class="el-icon-time" />
          <span>{{ scope.row.display_time }}</span>
        </template>
      </el-table-column>
      <el-table-column label="文件名">
        <template slot-scope="scope">
          {{ scope.row.title }}
        </template>
      </el-table-column>
      <el-table-column label="文件大小" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.pageviews }}
        </template>
      </el-table-column>
      <el-table-column class-name="status-col" label="上传人" width="110" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status | statusFilter">{{ scope.row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column align="center" prop="created_at" label="操作" width="230">
        <template>
          <el-button type="primary" size="mini">
            下载
          </el-button>
          <el-button size="mini" type="success">
            修改
          </el-button>
          <el-button size="mini" type="danger">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getList } from '@/api/table'

export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'gray',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      queryinfo: {
          name: '',
          user: ''
      },
      datedata: '',
      list: null,
      listLoading: true
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getList().then(response => {
        this.list = response.data.items
        this.listLoading = false
      })
    },
    search() {}
  }
}
</script>
