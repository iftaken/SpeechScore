<template>
  <el-header>  
      <el-row>
        <el-col :span="12">
          <div class="grid-content bg-purple">
            <h2 class="UserNameShow">用户: {{ this.$store.state.username }}</h2>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="grid-content bg-purple-light">
              <el-button class="LoginOutBtn" type="danger" @click="onLogout">退出登录</el-button>
          </div>
        </el-col>
    </el-row>
  </el-header>
</template>

<script>
export default {
  name: 'MyHeader',
  methods: {
    onLogout() {
      localStorage.removeItem('token')
      this.$router.push('/login')
    }
  },
  created () {
    if(!this.$store.state.username){
      this.$store.commit('changeUserName', localStorage.getItem("username"))
    }
    if(!this.$store.state.userid){
      this.$store.commit('changeUserId', localStorage.getItem("userid"))
    }
  }
}
</script>

<style lang="less" scoped>

.UserNameShow {
    position:static;
    left: 0%;
}

.LoginOutBtn {
    position:static;
    right: 0%;
}

</style>