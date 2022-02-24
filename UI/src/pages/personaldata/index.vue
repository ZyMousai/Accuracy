<template>
  <div class="new-page" :style="`min-height: ${pageMinHeight}px`">
    <a-tabs default-active-key="1" tab-position="left" size="large">
      <a-tab-pane key="1" tab="基本资料">
        <a-row :gutter="16" style="margin: 25px 0 150px 0;">
          <a-col :span="6">
              <a-form-model :model="form" :label-col="labelCol" :wrapper-col="wrapperCol" ref="userruleForm" :rules="userdatarules">
                <a-form-model-item label="姓名"  prop="name">
                  <a-input v-model="form.name" />
                </a-form-model-item>
                <a-form-model-item label="性别" prop="gender">
                  <a-select v-model="form.gender" placeholder="请选择性别">
                    <a-select-option value="true">
                      男
                    </a-select-option>
                    <a-select-option value="false">
                      女
                    </a-select-option>
                  </a-select>
                </a-form-model-item>
                <a-form-model-item label="出生日期" prop="birth">
                  <a-date-picker
                    v-model="form.birth"
                    show-time
                    format="YYYY-MM-DD"
                    type="date"
                    placeholder="请选择"
                    style="width: 100%;"
                  />
                </a-form-model-item>
                <!-- <a-form-model-item label="部门">
                  <a-input v-model="form.name" :disabled='true'/>
                </a-form-model-item>
                <a-form-model-item label="角色">
                  <a-input v-model="form.name" :disabled='true'/>
                </a-form-model-item> -->
                <a-form-model-item label="联系方式" prop="phone">
                  <a-input v-model="form.phone" />
                </a-form-model-item>
                <a-form-model-item label="联系地址"  prop="address">
                  <a-input v-model="form.address" type="textarea" />
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
    <!-- 修改密码表单 -->
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
          :rules="wprules"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
          :layout="form.layout"
        >
        <a-row :gutter="16">
          <a-col :span="10">
            <a-form-model-item label="密码" prop="password">
              <a-input v-model="wdform.password" />
            </a-form-model-item>
          </a-col>
          <a-col :span="10">
            <a-form-model-item label="确认密码" prop="repassword">
              <a-input v-model="wdform.repassword" />
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
  import { UserData, UpUserData } from '@/services/user';
  export default {
    name: 'personaldata',
    data() {
    var checkMobile = (rule, value, cb) => {
      console.log(value);
      const regMobile = /^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/;
      if (regMobile.test(value)) {
          // 合法的手机号码
          return cb() 
      }
      cb(new Error('手机号码格式不正确'))
    }
    // 验证密码是否相同
    var validatePass = (rule, value, callback) => {
      console.log(value);
      if (!value) {
        callback(new Error('请输入新密码！'))
      } else if (value.toString().length < 6) {
        callback(new Error('密码请大于六位数'))
      } else {
        callback()
      }
    }
    var validatePass2 = (rule, value, callback) => {
      console.log(value);
      if (value === '') {
          callback(new Error('请重新输入你的密码！'))
      } else if (value !== this.wdform.password) {
          callback(new Error('两次密码不一致!'))
      } else {
          callback()
      }
    }
      return {
        labelCol: { span: 8 },
        wrapperCol: { span: 15 },
        form: {
          name: '',
          gender: null,
          birth: null,
          address: '',
          phone: ''
        },
        loading: false,
        imageUrl: '',
        data,
        visible: false,
        wdform: {
          password: '',
          repassword: ''
        },
        userdatarules: {
          phone: [{ required: false, trigger: 'blur' },
                  { validator: checkMobile, rtigger:'blur'  }]
        },
        wprules: {
          password: [{ required: true, validator: validatePass, trigger: 'blur' }],
          repassword: [{ required: true, validator: validatePass2, trigger: 'blur' }]
        }
      }
    },
    computed: {
      ...mapState('setting', ['pageMinHeight']),
      desc() {
        return this.$t('description')
      }
    },
    created () {
      this.getuserdata()
    },
    methods: {
      // 获取用户信息
      getuserdata() {
        const id = localStorage.getItem('id')
        UserData(id).then(res => {
          this.form = res.data.data
          this.form.gender = this.form.gender + ''
          console.log(res);
        })
      },
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
        this.$refs.userruleForm.validate(valid => {
        if (valid) {
          this.form.birth = this.form.birth.format("YYYY-MM-DD")
          UpUserData(this.form).then(res => {
            if (res.status === 200) {
              this.$message.success('更新成功！')
              this.getuserdata()
            } else {
              this.$message.error('更新失败！')
            }
          })
        }
      })
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
      },
      handleOk() {
        this.$refs.ruleForm.validate(valid => {
          if (valid) {
            console.log(this.wdform);
          }
        })
      }
    }
  }
</script>

<style scoped lang="less">
@import "index";
</style>