<template>
    <h4 class="text-center">MOS评测</h4>
    <h4 class="text-left">任务ID: {{ taskId }}</h4>
    <h4 class="text-left">任务名称: {{ taskName }}</h4>
    <hr>
    
    <table class="table table-bordered table-striped table-hover">
        <thead>
            <tr>
                <th>#</th>
                <th>文件名</th>
                <th>音频</th>
                <th>Mos得分</th>
            </tr>
        </thead>
    <tbody>
      <tr v-for="(item, i) in scoreList" :key="item.id">
        <td>{{ i + 1 }}</td>
        <td>{{ item.file_name }}</td>
        <td><audio :src="'/api/dowanload/?fileId='+item.id" controls></audio></td>
        <td>
            <el-select v-model="item.mos" placeholder="请选择" :key="item.id">
                <el-option v-for="(mosL, j) in mosLevel" :value="mosL"></el-option>
            </el-select>
        </td>
      </tr>
    </tbody>
  </table>

  <el-button size="large" type="success" v-on:click="SubmitScore">提交</el-button>
  <el-button size="large" type="primary" v-on:click="ToTask">返回</el-button>
</template>


<script>
import UploadFile from './UploadFile.vue'

    export default {
    name: "TaskDetail",
    component: {
        "upload_file": UploadFile
    },
    data() {
        return {
            mosLevel: [5, 4.5, 4, 3.5, 3, 2, 1],
            select_value: "",
            scores: [],
            scoreList: [],
            taskName: "",
            taskId: -1
        };
    },
    methods: {
        async GetScoreList() {
            this.scoreList = [];
            const user_id = Number(localStorage.getItem('userid'))
            const result = await this.$http.post("/api/tasks/scoreWavList",
                { 
                    taskId: Number(this.taskId),
                    userId: user_id
                });
            if (result.data.code === 0) {
                const fileList = result.data.result;
                for (var i = 0; i < fileList.length; i++) {

                        this.scoreList.push({
                        mos: fileList[i]["score"],
                        file_name: fileList[i]["file_name"],
                        id: fileList[i]["file_id"]
                    })
                    
                }
            }
            else {
                this.$message.error(result.data.message);
            }
        },
        async SubmitScore(){
            // 上交打分情况
            if(this.scoreList.length > 0){
                const PostData = []
                for (var i = 0; i < this.scoreList.length; i++){
                    PostData.push(
                        {
                            fileId: this.scoreList[i].id,
                            taskId: Number(this.taskId),
                            userId: Number(localStorage.getItem("userid")),
                            score: this.scoreList[i].mos
                        }
                    )
                }
                const postResult = await this.$http.post("/api/scores/postScoreList", PostData);
                if(postResult.data.code == 0) {
                    this.$message.success(postResult.data.message)
                    this.ToTask()
                }
            } else {
                this.$message.error("文件列表为空")
            }
        },

        ToTask(){
             this.$router.push('/home/tasks')
        }

    },
    created() {
        this.taskName = this.$router.currentRoute.value.query.taskName;
        this.taskId = this.$router.currentRoute.value.query.taskId;
        this.GetScoreList();
    },
    components: { UploadFile }
}
</script>