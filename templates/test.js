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
                is_training:0

            },
            predictLoading:false,
            showResults: false,
            apiResponse: null,
            nameList:['sl36_pl24','sl36_pl36','sl36_pl48','sl36_pl60'],
            models:[],
            tableData: [
                // {
                //     name: "测试集 1",
                //     Autoformer: { mse: 3.379, mae: 1.289 },
                //     informer: { mse: 3.598, mae: null },
                //     iTransformer: { mse: 3.436, mae: 1.123 }
                // }
            ]

            
            

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
            this.filename = file.name
            console.log("filename为",this.filename)
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
        // 执行预测
        async performPredict() {
            if (!this.filename) {
                this.$message.error('请先上传文件');
                return;
              }
              
            this.predictLoading = true;
            this.showResults = false;
            const formData = new FormData();
            formData.append('filename',this.filename)
            formData.append('task',this.uploadForm.task)
            formData.append('is_training',this.uploadForm.is_training)       
            try { 
                const response = await fetch(`http://${SERVER_HOST}:5000/predict`, {
                    method: 'POST',
                    body: formData
                });
                const res = await response.json();
                console.log("res为：",res)
                
                if (res.code === 200) {
                    this.showResults = true;
                    this.$message.success('预测完成');
                    this.apiResponse = res;
                    this.processResults(res.data);

                } else {
                    this.$message.error(res.error);
                }
                } catch (error) {
                    this.$message.error('预测失败');
                }finally {
                    this.predictLoading = false;
                }                         
        },
        // 处理预测结果
         // 处理预测结果
         processResults(data) {
            this.models = data.map(item => item.model);
            
            // 找出最大结果数，用于确定表格行数
            const maxResults = Math.max(...data.map(item => item.result.length));
            
            // 生成表格数据
            this.tableData = Array.from({ length: maxResults }, (_, index) => {
                const row = { name: this.nameList[index] };
                
                data.forEach(modelData => {
                    const result = modelData.result[index];
                    if (result) {
                        row[modelData.model] = {
                            mse: result.mse,
                            mae: result.mae
                        };
                    }
                });
                
                return row;
            });
            
            console.log("Processed table data:", this.tableData);
        }
    }
}
        
    
);
