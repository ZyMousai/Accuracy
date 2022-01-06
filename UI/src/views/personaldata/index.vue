<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="auto">
          <my-upload field="img"
        @crop-success="cropSuccess"
        @crop-upload-success="cropUploadSuccess"
        @crop-upload-fail="cropUploadFail"
        v-model="show"
		:width="150"
		:height="150"
		url="/upload"
		:params="params"
		:headers="headers"
        :preview="'图形展示'"
        :noCircle="true"
		img-format="png"></my-upload>
	<img :src="avatar+'?imageView2/1/w/150/h/150'"  @click="toggleShow" class="Headportrait">
      <el-form-item label="姓名：">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="性别：">
        <el-select v-model="form.region" placeholder="选择性别">
          <el-option label="男" value="shanghai" />
          <el-option label="女" value="beijing" />
        </el-select>
      </el-form-item>
      <el-form-item label="出生日期">
          <el-date-picker v-model="form.date1" type="date" placeholder="选择日期" style="width: 100%;" />
      </el-form-item>
      <el-form-item label="部门：">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="角色：">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="联系地址：">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="联系方式：">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">更新</el-button>
        <el-button @click="onCancel">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import 'babel-polyfill'; // es6 shim
import myUpload from 'vue-image-crop-upload/upload-2.vue';

export default {
  data() {
    return {
      show: false,
      params: {
	  	token: '123456798',
	  	name: 'avatar'
	  },
	  headers: {
	  	smail: '*_~'
	  },
	  imgDataUrl: '',
      form: {
        name: '',
        region: '',
        date1: '',
        date2: '',
        delivery: false,
        type: [],
        resource: '',
        desc: ''
      }
    }
  },
  components: {
      'my-upload': myUpload
  },
  computed: {
    ...mapGetters([
      'sidebar',
      'avatar'
    ])
  },
  methods: {
    onSubmit() {
      this.$message('submit!')
    },
    onCancel() {
      this.$message({
        message: 'cancel!',
        type: 'warning'
      })
    },
    toggleShow() {
            this.show = !this.show;
        },
        cropSuccess(imgDataUrl, field){
            console.log('-------- crop success --------');
            this.imgDataUrl = imgDataUrl;
        },
        cropUploadSuccess(jsonData, field){
            console.log('-------- upload success --------');
            console.log(jsonData);
            console.log('field: ' + field);
        },
        cropUploadFail(status, field){
            console.log('-------- upload fail --------');
            console.log(status);
            console.log('field: ' + field);
        }
  }
}
</script>

<style scoped>
.line{
  text-align: center;
}
.Headportrait{
    border-radius: 75px;
    margin-bottom: 15px;
    margin-left: 50px;
}
.app-container{
    width: 30%;
}
</style>

