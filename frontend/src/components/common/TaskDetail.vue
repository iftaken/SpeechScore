<template>
    <h4 class="text-center">Task详细</h4>
    <h4 class="text-left">任务ID: {{ taskId }}</h4>
    <h4 class="text-left">任务名称: {{ taskName }}</h4>
    
    <hr>
    <upload-file :taskId = "taskId" :taskName="taskName" @updateCom="UpdateCom"></upload-file>
    <hr>
    <table class="table table-bordered table-striped table-hover">
        <thead>
            <tr>
                <th>#</th>
                <th>文件名</th>
                <th>音频</th>
                <th>Mos得分</th>
                <th>打分人次</th>
                <th>操作</th>
            </tr>
        </thead>
    <tbody>
      <tr v-for="(item, i) in scoreList" :key="item.id">
        <td>{{ i + 1 }}</td>
        <td>{{ item.file_name }}</td>
        <td><audio :src="'/api/dowanload/?fileId='+item.id" controls></audio></td>
        <td>{{ item.mos }}</td>
        <td>{{ item.cnt }}</td>
        <td>
          <!-- 展示评测详细情况 -->
          <el-button v-if="isAdmin(leaderId)" slot="trigger" size="large" type="primary" v-on:click="DeleteFile(item.id)">删除</el-button>
        </td>
      </tr>
    </tbody>
  </table>
<el-button slot="trigger" size="large" type="primary" v-on:click="ToTask">返回</el-button>

</template>


<script>
import UploadFile from './UploadFile.vue'

    export default {
    name: "ScoreTask",
    component: {
        "upload_file": UploadFile
    },
    data() {
        return {
            scoreList: [],
            taskName: "",
            taskId: -1,
            leaderId: -1,
        };
    },
    methods: {
        async GetScoreList() {
            this.scoreList = [];
            const result = await this.$http.post("/api/tasks/getScoreList", { taskId: this.taskId });
            if (result.data.code === 0) {
                const fileList = result.data.result;
                for (var i = 0; i < fileList.length; i++) {
                    this.scoreList.push({
                        mos: fileList[i]["mos"],
                        cnt: fileList[i]["cnt"],
                        file_name: fileList[i]["file_name"],
                        id: fileList[i]["file_id"]
                    });
                }
            }
            else {
                this.$message.error(result.data.message);
            }
        },
        async DeleteFile(fileId){
            const result = await this.$http.post("/api/tasks/dropFileId", { fileId: fileId });
            if (result.data.code === 0) {
                this.$message.success(result.data.message)
                this.UpdateCom()
            } else {
                this.$message.success(result.data.message)
            }
        },
        ToTask(){
            this.$router.push('/home/tasks')
        },
        UpdateCom() {
            // 更新组件
            this.$nextTick(()=>{
                this.GetScoreList();
            })
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
    },
    created() {
        this.taskName = this.$router.currentRoute.value.query.taskName;
        this.taskId = Number(this.$router.currentRoute.value.query.taskId);
        this.leaderId = Number(this.$router.currentRoute.value.query.leaderId);
        this.GetScoreList();
    },
    components: { UploadFile }
}
</script>