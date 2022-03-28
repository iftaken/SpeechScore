<template>
  <div class="login-container">
    <div class="login-box">
      <!-- 头像区域 -->
      <div class="text-center avatar-box">
        <img src="../assets/logo.png" class="img-thumbnail avatar" alt="" />
      </div>

      <!-- 表单区域 -->
      <div class="form-login p-4">
        <!-- 登录名称 -->
        <div class="form-group form-inline">
          <label for="username">登录名称</label>
          <input
            type="text"
            class="form-control ml-2"
            id="username"
            placeholder="请输入登录名称"
            autocomplete="off"
            v-model.trim="username"
          />
        </div>
        <!-- 登录密码 -->
        <div class="form-group form-inline">
          <label for="password">登录密码</label>
          <input
            type="password"
            class="form-control ml-2"
            id="password"
            placeholder="请输入登录密码"
            v-model.trim="password"
          />
        </div>
        <!-- 登录和重置按钮 -->
        <div class="form-group form-inline d-flex justify-content-end">
          <!-- <button type="button" class="btn btn-secondary mr-2">重置</button> -->
          <button type="button" class="btn btn-primary mr-2" @click="onLoginClick">
            登录
          </button>
          <button type="button" class="btn btn-primary" @click="onRegisterClick">
            注册
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>import { withCtx } from "vue"

export default {
  name: 'MyLogin',
  data() {
    return {
      username: '',
      password: '',
    }
  },
  methods: {

    async onRegisterClick() {
      const postData = {
        'username': this.username,
        'password': this.password
      }
      const result = await this.$http.post("/api/user/register", postData)
      this.$message.success(result.data.message)
    },


    async onLoginClick() {
      // 向后端请求服务，验证服务
      const postData = {
        'username': this.username,
        'password': this.password
      }
      const result = await this.$http.post("/api/user/login", postData)
      // 检查是否登录成功
      if (result.data.code === 0) {
        this.$store.commit('changeUserName', result.data.result.username)
        this.$store.commit("changeUserId", result.data.result.id)

        localStorage.setItem('username', result.data.result.username)
        localStorage.setItem('userid', result.data.result.id)
        localStorage.setItem('token', result.data.result.token)

        this.$router.push('/home')
        
      } else {
        localStorage.clear()
        alert(result.data.message)
      }
    },
  },
}
</script>

<style lang="less" scoped>
.login-container {
  background-color: #35495e;
  height: 100%;
  .login-box {
    width: 400px;
    height: 250px;
    background-color: #fff;
    border-radius: 3px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 6px rgba(255, 255, 255, 0.5);
    .form-login {
      position: absolute;
      bottom: 0;
      left: 0;
      width: 100%;
      box-sizing: border-box;
    }
  }
}

.form-control {
  flex: 1;
}

.avatar-box {
  position: absolute;
  width: 100%;
  top: -65px;
  left: 0;
  .avatar {
    width: 120px;
    height: 120px;
    border-radius: 50% !important;
    box-shadow: 0 0 6px #efefef;
  }
}
</style>
