<template>
  <div class="new-page" :style="`min-height: ${pageMinHeight}px`">
    <a-tabs default-active-key="1" tab-position="left" size="large">
      <a-tab-pane key="1" tab="基本资料">
        <a-row :gutter="16" style="margin: 25px 0 150px 0;">
          <a-col :span="6">
              <a-form-model :model="form" :label-col="labelCol" :wrapper-col="wrapperCol">
                <a-form-model-item label="姓名">
                  <a-input v-model="form.name" />
                </a-form-model-item>
                <a-form-model-item label="性别">
                  <a-select v-model="form.region" placeholder="请选择性别">
                    <a-select-option value="shanghai">
                      男
                    </a-select-option>
                    <a-select-option value="beijing">
                      女
                    </a-select-option>
                  </a-select>
                </a-form-model-item>
                <a-form-model-item label="出生日期">
                  <a-date-picker
                    v-model="form.date1"
                    show-time
                    type="date"
                    placeholder="请选择"
                    style="width: 100%;"
                  />
                </a-form-model-item>
                <a-form-model-item label="部门">
                  <a-input v-model="form.name" />
                </a-form-model-item>
                <a-form-model-item label="角色">
                  <a-input v-model="form.name" />
                </a-form-model-item>
                <a-form-model-item label="联系方式">
                  <a-input v-model="form.name" />
                </a-form-model-item>
                <a-form-model-item label="联系地址">
                  <a-input v-model="form.desc" type="textarea" />
                </a-form-model-item>
                <a-form-model-item :wrapper-col="{ span: 14, offset: 4 }">
                  <a-button type="primary" @click="onSubmit">
                    更新
                  </a-button>
                </a-form-model-item>
              </a-form-model>
          </a-col>
          <a-col :span="6" :offset="1">
            <a-upload
              name="avatar"
              list-type="picture-card"
              class="avatar-uploader"
              :show-upload-list="false"
              action="https://www.mocky.io/v2/5cc8019d300000980a055e76"
              :before-upload="beforeUpload"
              @change="handleChange"
            >
              <img v-if="imageUrl" :src="imageUrl" alt="avatar" />
              <div v-else>
                <a-icon :type="loading ? 'loading' : 'plus'" />
                <div class="ant-upload-text">
                  上传头像
                </div>
              </div>
            </a-upload>
          </a-col>
        </a-row>
      </a-tab-pane>
      <a-tab-pane key="2" tab="安全设置">
        <a-list item-layout="horizontal" :data-source="data" >
          <a-list-item slot="renderItem" slot-scope="item">
            <a slot="actions" style="margin-right: 15px;" @click="showModal">修改</a>
            <a-list-item-meta>
              <a slot="title" style="float: left;">{{ item.title }}</a>
            </a-list-item-meta>
          </a-list-item>
        </a-list>
      </a-tab-pane>
    </a-tabs>
    <!-- 表单 -->
      <a-modal v-model="visible" title="修改密码" on-ok="handleOk" :maskClosable="false" @afterClose="handleCancel()" :width='850'>
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
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          :layout="form.layout"
        >
        <a-row :gutter="16">
          <a-col :span="10">
            <a-form-model-item ref="filename" label="密码" prop="filename">
              <a-input v-model="wdform.filename" />
            </a-form-model-item>
          </a-col>
          <a-col :span="10">
            <a-form-model-item ref="filename" label="确认密码" prop="filename">
              <a-input v-model="wdform.filename" />
            </a-form-model-item>
          </a-col>
        </a-row>
        </a-form-model>
      </template>
    </a-modal>
  </div>
</template>

<script>
  function getBase64(img, callback) {
    const reader = new FileReader();
    reader.addEventListener('load', () => callback(reader.result));
    reader.readAsDataURL(img);
  }
  const data = [
    {
      title: '账户密码',
    }
  ];
  import {mapState} from 'vuex'
  export default {
    name: 'personaldata',
    data() {
      return {
        labelCol: { span: 8 },
        wrapperCol: { span: 15 },
        form: {
          name: '',
          region: undefined,
          date1: undefined,
          delivery: false,
          type: [],
          resource: '',
          desc: '',
        },
        loading: false,
        imageUrl: '',
        data,
        visible: false,
        wdform: {
          layout: 'vertical',
          filename: '',
          department: '',
          desc: ''
        },
      }
    },
    computed: {
      ...mapState('setting', ['pageMinHeight']),
      desc() {
        return this.$t('description')
      }
    },
    methods: {
      handleChange(info) {
      if (info.file.status === 'uploading') {
        this.loading = true;
        return;
      }
      if (info.file.status === 'done') {
        // Get this url from response in real world.
        getBase64(info.file.originFileObj, imageUrl => {
          this.imageUrl = imageUrl;
          this.loading = false;
        });
      }
      },
      beforeUpload(file) {
        const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
        if (!isJpgOrPng) {
          this.$message.error('You can only upload JPG file!');
        }
        const isLt2M = file.size / 1024 / 1024 < 2;
        if (!isLt2M) {
          this.$message.error('Image must smaller than 2MB!');
        }
        return isJpgOrPng && isLt2M;
      },
      onSubmit() {
        console.log('submit!', this.form);
      },
      // 打开编辑表单
      showModal(id) {
        typeof id === 'number' ? this.tablename = '编辑' : this.tablename = '新增'
        this.visible = true;
      },
      // 关闭编辑表单
      handleCancel() {
        this.visible = false;
        this.$refs.ruleForm.resetFields();
        console.log('ok');
      },
    }
  }
</script>

<style scoped lang="less">
@import "index";
</style>