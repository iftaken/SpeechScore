<template>
  <el-aside width="150px">
    <el-menu 
      default-active="2"
      class="el-menu-vertical-demo"
    >
      <el-menu-item v-on:click="ToTask">任务列表</el-menu-item>
      <!-- <el-menu-item>
          <router-link to="/home/tasks">任务列表</router-link>
      </el-menu-item> -->
      
    </el-menu>
  </el-aside>
</template>

<script>
export default {
  name: 'MyAside',

  methods: {
    ToTask() {
      this.$router.push("/home/tasks")
    }
  }
}
</script>

<style lang="less" scoped>
.layout-aside-container {
  width: 250px;
  height: 100%;
  border-right: 1px solid #eaeaea;
}

.menu {
  list-style-type: none;
  padding: 0;
  .menu-item {
    line-height: 50px;
    font-weight: bold;
    font-size: 14px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
      Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    &:hover {
      background-color: #efefef;
      cursor: pointer;
    }
    a {
      display: block;
      color: black;
      padding-left: 30px;
      &:hover {
        text-decoration: none;
      }
    }
  }
}

// 设置路由高亮效果
.router-link-active {
  background-color: #efefef;
  box-sizing: border-box;
  position: relative;
  // 伪元素实现路由高亮效果
  &::before {
    content: ' ';
    display: block;
    width: 4px;
    height: 100%;
    position: absolute;
    left: 0;
    top: 0;
    background-color: #42b983;
  }
}
</style>
