<template>
  <a-dropdown>
    <div class="header-avatar" style="cursor: pointer">
      <a-avatar class="avatar" size="large" shape="circle" :src="`${this.alone}/PersonnelManagement/users/v1/avatar/` + user.avatar"/>
      <span class="name">{{user.name}}</span>
    </div>
    <a-menu :class="['avatar-menu']" slot="overlay">
      <a-menu-item>
        <a-icon type="user" />
        <span @click="gopersonal">个人资料</span>
      </a-menu-item>
      <a-menu-divider />
      <a-menu-item @click="logout">
        <a-icon style="margin-right: 8px;" type="poweroff" />
        <span>退出登录</span>
      </a-menu-item>
    </a-menu>
  </a-dropdown>
</template>

<script>
import {mapGetters} from 'vuex'
import {logout} from '@/services/user'

export default {
  name: 'HeaderAvatar',
  data () {
    return {
      alone: '',
      name: '',
      avatar: ''
    }
  },
  computed: {
    ...mapGetters('account', ['user']),
  },
    created () {
      this.getuserdata()
    },
  methods: {
    getuserdata() {
      this.name = localStorage.getItem('name')
      this.avatar = localStorage.getItem('avatar')
      this.alone = process.env.VUE_APP_API_ALONE_URL
    },
    logout() {
      logout()
      this.$router.push('/login')
      localStorage.clear()
    },
    gopersonal() {
      this.$router.push('/personaldata')
    }
  }
}
</script>

<style lang="less">
  .header-avatar{
    display: inline-flex;
    .avatar, .name{
      align-self: center;
    }
    .avatar{
      margin-right: 8px;
    }
    .name{
      font-weight: 500;
    }
  }
  .avatar-menu{
    width: 150px;
  }

</style>
