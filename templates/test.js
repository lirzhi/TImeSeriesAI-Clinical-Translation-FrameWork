const SERVER_HOST = '127.0.0.1'

// 创建Vue实例
new Vue({
    el: '#app',
    
    data() {
        return {
            file:"",
            fileList:[],
            options: [  // 推荐使用数组形式
                { label: '时序预测', value: 'time-series' },
                { label: '动态决策', value: 'rl' }
              ],
            uploadForm:{
                task:'',

            },

            
            

        }
    },

    created() {
       
    },
    mounted(){
       

    },
    beforeDestroy() {
       
      },
    watch: {
      
    },
    computed:{
        
    },    
    methods: {
        
        //上传文件
        async submitUpload() {
            const formData = new FormData();
            const file = this.fileList[0];
            console.log("file为",file.raw)
            formData.append('file', file.raw);
            const task = this.uploadForm.task;
            formData.append('task', task);
            console.log("formData为",formData)
            try {
                const response = await fetch(`http://${SERVER_HOST}:5000/upload`,  {
                    
                    method: 'POST',
                    body: formData, // 注意：不要手动设置 Content-Type
                });
                 res = await response.json();
                 console.log("res.data为：",res)
                if (res.data.status === 1) {
                  this.$message.success('上传成功');
                  this.fileList = [];
                  console.log("res.data为：",res.data)
                //   this.getEctdList();
                }
                else{
                    this.$message.error(res.data.msg);

                }
            } catch (error) {
                this.$message.error('文件上传失败');
                console.log("error为：",error,)
            }
        },
        handlePreview(file,fileList){
            console.log("file为：",file)
        },
         //修改文件列表
        handleChange(file, fileList) {
            this.fileList = fileList;
            console.log("fileList 为：",fileList )
        },
        beforeUpload(file) {
            this.fileList.push(file);
            console.log("fileList 为：",fileList )
            return false; // 阻止默认上传行为
        },
        //删除文件列表里的文件
        handleRemove(file, fileList) {
            this.fileList = fileList; // 更新文件列表
            this.$message({
                message: '文件删除成功',
                type: 'info'
            });
        },
    }
}
        
    
);
