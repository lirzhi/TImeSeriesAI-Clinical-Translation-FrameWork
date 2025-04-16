from email import message
from fileinput import filename
from http import client
import os
import shutil
import time
import json
from kafka import KafkaProducer
from flask import Flask, redirect, render_template, request, jsonify, url_for
from flask_cors import CORS
from common_util import ResponseMessage


app = Flask(__name__, static_folder='templates')
CORS(app)  # 允许所有跨域请求
# Kafka配置
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092')
TOPICS = ['autoformer', 'informer']

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# 路由：返回 predict.html
@app.route('/')
def index():
    return redirect(url_for("static", filename='predict.html'))
@app.route('/upload', methods=['POST'])
def upload_file():
    res_data = {
        "status": 1,
        "task": None,
        "filename": None
    }
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    task = request.form.get('task', 'default')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files are allowed'}), 400
    file = request.files['file']
    # 保存文件到输入目录
    input_dir = os.getenv('INPUT_DIR', './data')
    os.makedirs(input_dir, exist_ok=True)
    file_path = os.path.join(input_dir, file.filename)
    file.save(file_path)
    
    # 分发文件到子容器
    distribute_to_containers(file.filename, input_dir)

    res_data['filename']=file.filename
    res_data['task']=task
    return ResponseMessage(200,'upload success', res_data).to_json()

def distribute_to_containers(filename, source_dir):
    """分发文件到子容器"""
    containers = ['mq-autoformer']
    print(containers)
    for container_name in containers:
        # 获取容器对象
        try:
            container = client.containers.get(container_name)
            print(container)
        except:
            print('error:容器未运行')
            return jsonify({'error': f'{container_name}容器未运行'}), 500
        
        # 在子容器中创建目标目录
        dest_dir = f'/dataset/{os.path.splitext(filename)[0]}'
        print(dest_dir)
        cmd = f'mkdir -p {dest_dir}'
        container.exec_run(cmd, workdir='/')
        
        # 复制文件到子容器
        with open(os.path.join(source_dir, filename), 'rb') as f:
            container.put_archive('/dataset/', {
                os.path.splitext(filename)[0]: f.read()
            })
        
        # 修改predict.sh脚本并执行
        modify_and_run_script(container, filename)

def modify_and_run_script(container, filename):
    """修改并执行子容器中的预测脚本"""
    illness_name = os.path.splitext(filename)[0]
    print("illness_name:",illness_name)
    
    # 修改脚本中的路径参数
    sed_cmd = f"""sed -i 's/root_path=.*/root_path=\".\/dataset\/{illness_name}\"/g' ./scripts/predict.sh"""
    container.exec_run(sed_cmd, workdir='/')
    
    sed_cmd = f"""sed -i 's/data_path=.*/data_path=\"{filename}\"/g' ./scripts/predict.sh"""
    container.exec_run(sed_cmd, workdir='/')
    
    # 执行预测脚本
    exec_result = container.exec_run('sh ./scripts/predict.sh', workdir='/')
    return exec_result.output.decode('utf-8')
@app.route('/predict', methods=['POST'])
    # 读取文件内容
def predict():  
    
    filename = request.get('filename')
    task = request.form.get('task', 'default')
    
    if filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files are allowed'}), 400
    # 保存文件到输入目录
    input_dir = os.getenv('INPUT_DIR', './data')
    file_path = os.path.join(input_dir, filename)
    results = []
    containers = ['autoformer', 'informer']
    
    for container_name in containers:
        try:
            container = client.containers.get(container_name)
            # 从容器中获取结果文件
            result_file = f'/results/result.json'
            bits, _ = container.get_archive(result_file)
            
            # 保存结果到本地
            with open('temp_result.tar', 'wb') as f:
                for chunk in bits:
                    f.write(chunk)
            
            # 提取结果
            shutil.unpack_archive('temp_result.tar', 'temp_result')
            with open(os.path.join('temp_result', 'result.json')) as f:
                # 读取所有结果对象
                all_results = json.load(f)
                
                # 确保结果是一个列表
                if not isinstance(all_results, list):
                    all_results = [all_results]
                
                # 提取最新的5个结果（假设列表顺序从旧到新）
                latest_results = all_results[-5:] if len(all_results) >= 5 else all_results
                
                # 构建结果结构
                results.append({
                    'model': container_name,
                    'result': latest_results
                })
        except Exception as e:
            return jsonify({'error': f'获取{container_name}结果失败: {str(e)}'}), 500
            
            # 清理临时文件
            os.remove('temp_result.tar')
            shutil.rmtree('temp_result')

    # for topic in TOPICS:
    #     producer.send(topic, value=message)

    #     producer.flush()
    
    # # 等待结果返回
    # time.sleep(10)  # 实际应用中应该使用更可靠的方式等待结果
    return ResponseMessage(200,'upload success', results).to_json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)