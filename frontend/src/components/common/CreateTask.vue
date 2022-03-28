<template>
<form>
  <div class="form-group">
    <label for="exampleInputEmail1">任务名称</label>
    <input class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" v-model="taskname">
  </div>
  <div class="form-group">
    <label for="exampleInputPassword1">说明</label>
    <input class="form-control" id="exampleInputPassword1" v-model="desc">
  </div>

  <button type="submit" class="btn btn-primary m-2" v-on:click="SubmitTask">Submit</button>
  <button type="submit" class="btn btn-primary" v-on:click="Back">后退</button>
</form>
</template>

<script>
export default {
    name: "CreateTask",
    data() {
        return {
            message: "这是 创建任务弹窗",
            taskname: "",
            desc: ""
        }
    },
    methods: {
        Back(){
            this.$router.push('/home/tasks');
        },

        async SubmitTask(){
            const postData = {
                taskname: this.taskname,
                leader_id: Number(localStorage.getItem('userid')),
                desc: this.desc
            }
            const result = await this.$http.post("/api/tasks/create_tasks", postData)
            if(result.data.code === 0){
                this.$message.success("任务创建成功")
            } else {
                this.$message.error("任务创建失败")
            }
            this.$router.push("/home/tasks")
        }
    }

}
    

</script>