<template>
  <!-- 标题 -->
  <h4 class="text-center">任务管理</h4>

  <button type="button" class="btn btn-primary createTask" v-on:click="CreateTasks">创建任务</button>
  <hr>

  <!-- 用户列表 -->
  <table class="table table-bordered table-striped table-hover">
    <thead>
      <tr>
        <th>#</th>
        <th>任务名称</th>
        <th>负责人</th>
        <th>说明</th>
        <th>统计结果</th>
        <th>操作</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(item, i) in userlist" :key="item.id">
        <td>{{ i + 1 }}</td>
        <td>{{ item.name }}</td>
        <td>{{ item.principal }}</td>
        <td>{{ item.description }}</td>
        <td> <a v-if=" item.mos > 0"> {{ item.mos }}</a> <a v-else> 未评测 </a> </td>
        <td>
          <!-- 展示评测详细情况 -->
          <el-button size="large" type="primary" v-on:click="ToScore(item.id, item.name, item.leader_id)"> 评测 </el-button>
          &nbsp;
          <el-button size="large" type="success" v-on:click="ToDeatil(item.id, item.name, )"> 详细 </el-button>
          &nbsp;
          <el-button v-if="isAdmin(item.leader_id)"
            size="large" type="danger" 
            v-on:click="DeleteTask(item.id, item.name)">
            删除
          </el-button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import CreateTask from '../common/CreateTask.vue'
import UploadFile from '../common/UploadFile.vue'
import {useRouter} from 'vue-router';
const router = useRouter();

export default {


  name: 'Tasks',

  // 注册组件
  components: {
    "create_task": CreateTask,
    "upload_file": UploadFile
  },

  data() {
    return {
      // 用户列表数据
      userlist: [
      ],
    }
  },

  methods: {
    async GetTaskList() {
      this.userlist = []
      const result = await this.$http.get("/api/tasks/get_tasklist")
      const tasks = result.data.result
      if (tasks) {
        for(var i=0; i < tasks.length; i++){
          this.userlist.push(
            {
              id: tasks[i].id,
              name: tasks[i].taskname,
              principal: tasks[i].leader_name,
              leader_id: tasks[i].leader_id,
              description: tasks[i].desc,
              mos: tasks[i].mos
            }
          )
        }
      } else {
        this.$message.error("任务列表为空");
      }
    },

    isAdmin(leaderId){
      // 判断当前用户有无删除权限
      const userId = Number(localStorage.getItem('userid'))
      const userName = localStorage.getItem('username')
      if(leaderId === userId){
        return true
      } else if(userName == "admin") {
        return true
      } else {
        return false
      }
    },

    ToDeatil(task_id, task_name, leader_id) {
      this.$router.push({path:'/home/taskDetail', query:{
        taskId: Number(task_id),
        taskName: task_name,
        leaderId: Number(leader_id)}})
    },

    ToScore(task_id, task_name) {
      this.$router.push({path:'/home/scoreTask', query:{taskId: Number(task_id), taskName: task_name}})
    },

    CreateTasks(){
      this.$router.push('/home/createTask')
    },

    async  DeleteTask(taskId){
      const PostData = {
        "taskId": taskId
      }
      const result = await this.$http.post("/api/tasks/deleteTask", PostData)
      if(result.data.code === 0){
        this.$message.success(result.data.message)
      } else {
        this.$message.error(result.data.message)
      }
      // this.$message.success(result.data.message)
      this.UpdateCom()
    },

    UpdateCom() {
        // 更新组件
        this.$nextTick(()=>{
            this.GetTaskList();
        })
    },
  },

  created() {
    this.GetTaskList();
  },

}
</script>

<style lang="less" scoped>
.createTask {
  position:static;
  left: 10%;
}
</style>
