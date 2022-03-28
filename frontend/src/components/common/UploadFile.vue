
<template>
    <el-upload
            class="pop-upload"
            ref="upload"
            action=""
            :file-list="fileList"
            :auto-upload="false"
            :multiple="true"
            :on-change="handleChange"
            :on-remove="handleRemove"
    >
        <el-button size="large" type="primary">选取文件</el-button>        
    </el-upload>
    <el-button style="margin-left: 10px;" size="large" type="success" @click="submitUpload">上传到服务器</el-button>
</template>


<script>
export default {
    name: "UploadFile",
    components: {
        
    },
    props: {
        taskId: {
            type: [Number],
            required: true
        },
        taskName: {
            type: [String],
            required: true
        }
    },

    data () {
        return {
            fileList: []
        }
    },

    emits: ["updateCom"],

    methods: {
        handleChange(file, fileList) {
                this.fileList = fileList
            },
        handleRemove(file, fileList) {
                this.fileList = fileList
            },
        async submitUpload() {
            if (this.fileList.length === 0) {
                return this.$message.warning('请选择文件后再上传')
            }
            const formData = new FormData()
            this.fileList.forEach((file) => {
                    formData.append('files', file.raw)
                })
            formData.append('task_id', this.taskId)
            // 上传文件
            const result = await this.$http.post("/api/tasks/upload_files", formData)
            if (result.data.code === 0) {
                this.$message.success(result.data.message);
            } else {
                this.$message.error(result.data.message);
            }
            this.fileList = []

            this.$emit("updateCom")

        }
    }
}
</script>