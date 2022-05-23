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
                    @change="datepicker"
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
                  <a-button type="primary" @click="onSubmit" :loading="buttonloading">
                    更新
                  </a-button>
                </a-form-model-item>
              </a-form-model>
          </a-col>
          <a-col :span="6" :offset="1">
            <a-upload
              name="file"
              list-type="picture-card"
              class="avatar-uploader"
              :show-upload-list="false"
              :action="upactionurl"
              :headers="headers"
              :before-upload="beforeUpload"
              @change="handleChange"
            >
              <img v-if="imageUrl" :src="imageUrl" alt="avatar" width="150px" />
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
            <a-list-item-meta>
              <a slot="title" style="float: left;" @click="showModal"><a-button type="primary"><a-icon type="user" />{{ item.title }}</a-button></a>
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
        <a-button key="submit" type="primary"  :loading="buttonloading" @click="handleOk">
          提交
        </a-button>
      </template>
      <template>
        <a-form-model
          ref="ruleForm"
          :model="wdform"
          :rules="wprules"
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 14 }"
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
  const data = [
    {
      title: '修改密码',
    }
  ];
  import {mapMutations, mapState, mapGetters} from 'vuex'
  import { UserData, UpUserData, UpPassword, logout } from '@/services/user';
  export default {
    name: 'personaldata',
    data() {
    var checkMobile = (rule, value, cb) => {
      const regMobile = /^(0|86|17951)?(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$/;
      if (regMobile.test(value)) {
          // 合法的手机号码
          return cb() 
      }
      cb(new Error('手机号码格式不正确'))
    }
    // 验证密码是否相同
    var validatePass = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入新密码！'))
      } else if (value.toString().length < 6) {
        callback(new Error('密码请大于六位数'))
      } else {
        callback()
      }
    }
    var revalidatePass = (rule, value, callback) => {
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
        upactionurl: '',
        data,
        visible: false,
        buttonloading: false,
        alone: '',
        wdform: {
          password: '',
          repassword: ''
        },
        userdatarules: {
          phone: [{ required: false, trigger: 'blur' },
                  { validator: checkMobile, rtigger:'blur'}]
        },
        wprules: {
          password: [{ required: false, trigger: 'blur' },
                     { validator: validatePass, rtigger:'blur'}],
          repassword: [{ required: false, trigger: 'blur' },
                           { validator: revalidatePass, rtigger:'blur'}]
        },
        headers: {
          accept: 'application/json'
        }
      }
    },
    computed: {
      ...mapMutations('account', ['setUser']),
      ...mapState('setting', ['pageMinHeight']),
      ...mapGetters('account', ['user']),
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
        this.alone = process.env.VUE_APP_API_ALONE_URL
        const id = localStorage.getItem('id')
        UserData(id).then(res => {
          this.form = res.data.data
          localStorage.name = this.form.name
          localStorage.avatar = this.form.avatar
          this.form.gender = this.form.gender + ''
          this.imageUrl = `${this.alone}/PersonnelManagement/users/v1/avatar/${this.form.avatar}`;
          this.user.avatar = this.form.avatar
          this.user.name = this.form.name
        })
      },
      handleChange(info) {
        console.log(info);
        if (info.file.status === 'uploading') {
          this.loading = true;
          return;
        }
        if (info.file.status === 'done') {
            this.$message.success('上传成功！')
            this.getuserdata()
            this.loading = false;
        }
      },
      beforeUpload(file) {
        const id = localStorage.getItem('id')
        const account = localStorage.getItem('account')
        this.upactionurl = `${this.alone}/PersonnelManagement/users/v1/upload_avatar?account=${account}&user_id=${id}`
        const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
        if (!isJpgOrPng) {
          this.$message.error('You can only upload JPG file!');
        }
        const isLt2M = file.size / 1024 / 1024 < 2;
        if (!isLt2M) {
          this.$message.error('文件不能大于2MB!');
        }
        return isJpgOrPng && isLt2M;
      },
      // 处理时间格式
      datepicker() {
        this.form.birth = this.form.birth.format("YYYY-MM-DD")
      },
      onSubmit() {
        this.$refs.userruleForm.validate(valid => {
        if (valid) {
          this.buttonloading = true
          UpUserData(this.form).then(res => {
            if (res.status === 200) {
              this.$message.success('更新成功！')
              this.getuserdata()
              this.buttonloading = false
            } else {
              this.buttonloading = false
              this.$message.error('更新失败！')
            }
          })
        }
      })
      },
      // 打开编辑表单
      showModal() {
        this.visible = true;
      },
      // 关闭编辑表单
      handleCancel() {
        this.visible = false;
        this.$refs.ruleForm.resetFields();
      },
      handleOk() {
        console.log(this.wdform);
        this.$refs.ruleForm.validate(valid => {
          if (valid) {
            this.buttonloading = true
            const data = {
              id: this.user.id,
              password: this.wdform.password
            }
            UpPassword(data).then(res => {
              if (res.status === 200) {
                this.$message.success('修改密码成功，请重新登陆！')
                this.$refs.ruleForm.resetFields();
                this.buttonloading = false
                this.visible = false
                logout()
                this.$router.push('/login')
                localStorage.clear()
              } else {
                this.$message.error('更新失败！')
                this.buttonloading = false
              }
            })
          }
        })
      }
    }
  }
</script>

<style scoped lang="less">
@import "index";
</style>