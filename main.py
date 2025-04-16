from email import message
from fileinput import filename
from http import client
import os
from pathlib import Path
import shutil
import subprocess
import time
import json
from unittest import result
# from kafka import KafkaProducer
from flask import Flask, redirect, render_template, request, jsonify, url_for
from flask_cors import CORS
from common_util import ResponseMessage

# 关键配置：延长请求超时时间
from werkzeug.serving import WSGIRequestHandler
WSGIRequestHandler.protocol_version = "HTTP/1.1"  # 保持持久连接

app = Flask(__name__, static_folder='templates')
CORS(app)  # 允许所有跨域请求
# Kafka配置
# KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092')
# TOPICS = ['autoformer', 'informer']

# producer = KafkaProducer(
#     bootstrap_servers=[KAFKA_BROKER],
#     value_serializer=lambda x: json.dumps(x).encode('utf-8')
# )
# 脚本目录
SCRIPT_DIR = "./scripts"
models=['Autoformer','informer','iTransformer','TimeMixer','Timer']

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
    filename = file.filename  # "file.csv"
    clean_name = Path(filename).stem
    # 保存文件到输入目录
    file.seek(0)  # 重置指针到文件开头
    input_dir = os.getenv('INPUT_DIR', './data')
    os.makedirs(input_dir, exist_ok=True)
    file_path = os.path.join(input_dir, filename)
    file.save(file_path)
    #保存文件到模型目录
    for model in models:
        file.seek(0)  # 重置指针到文件开头
        model_input_dir = os.path.join('./models', model, 'dataset', clean_name)
        os.makedirs(model_input_dir, exist_ok=True)
            # 完整的文件保存路径
        model_input_path = os.path.join(model_input_dir, filename)
        if os.path.exists(model_input_path):
            os.remove(model_input_path)  # 先删除旧文件
        file.save(model_input_path)
         # 2. 修改对应模型的 predict.sh 脚本
        model_script_path = os.path.join('./models', model, 'scripts', 'predict.sh')
        
        # 读取脚本内容
        with open(model_script_path, 'r', encoding='utf-8') as f:
            script_content = f.read()
        
        # 替换变量值
        new_root_path = f'root_path="./dataset/{clean_name}/"'
        new_data_path = f'data_path="{filename}"'
        
        # 使用正则表达式替换更可靠
        import re
        script_content = re.sub(r'root_path=".*?"', new_root_path, script_content)
        script_content = re.sub(r'data_path=".*?"', new_data_path, script_content)
        
        # 写回修改后的脚本
        with open(model_script_path, 'w') as f:
            f.write(script_content)


    res_data['filename']=file.filename
    res_data['task']=task
    return ResponseMessage(200,'upload success', res_data).to_json()

def run_model_script(model_name):
    """执行对应模型的 .sh 脚本"""
    script_path = os.path.join(SCRIPT_DIR, f"{model_name}.sh")
    
    # 检查脚本是否存在
    if not os.path.exists(script_path):
        print(f"Error: Script {script_path} not found!")
        return False
    
    # 执行脚本
    try:
        print(f"Running script: {script_path}")
        result = subprocess.run(
            ["bash", script_path],
            check=True,  # 如果脚本返回非0状态码，抛出异常
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"Output:\n{result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Script failed with error:\n{e.stderr}")
        return False
    
def get_latest_results(model_name, num_results=4):
    """获取指定模型的最新结果"""
    # 构建结果文件路径
    result_path = os.path.join('./models', model_name, 'results', 'result.json')
    print(result_path)
    try:
        # 读取JSON文件
        with open(result_path, 'r') as f:
            results = json.load(f)
        print(results)
        # 获取最新的num_results条记录（假设新记录在列表末尾）
        latest_results = results[-num_results:] if len(results) > num_results else results
        print(latest_results)
        return {
            'model': model_name,
            'result': latest_results
        }
    except FileNotFoundError:
        print(f"Warning: Results file not found for model {model_name}")
        return { 
            'model': model_name,
            'result': [],
            'error': 'Results file not found'
        }
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON format in results file for model {model_name}")
        return {
            'model': model_name,
            'result': [],
            'error': 'Invalid results format'
        }
def istraining(is_training):
    #保存文件到模型目录
    for model in models:
        #修改对应模型的 predict.sh 脚本
        model_script_path = os.path.join('./models', model, 'scripts', 'predict.sh')
        
        # 读取脚本内容
        with open(model_script_path, 'r', encoding='utf-8') as f:
            script_content = f.read()
        
        # 替换变量值
        new_is_training = f'is_training={is_training}'
        
        # 使用正则表达式替换更可靠
        import re
        script_content = re.sub(r'is_training=".*?"', new_is_training, script_content)
        
        # 写回修改后的脚本
        with open(model_script_path, 'w') as f:
            f.write(script_content)
    return True
@app.route('/predict', methods=['POST'])
    # 读取文件内容
def predict():  
    filename = request.form.get('filename')
    task = request.form.get('task', 'default')
    is_training= request.form.get('is_training', 'default')
    istraining(is_training)
    if filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files are allowed'}), 400
    if task == 'time-series':
        for model in models:
            print(f"\n=== Processing model: {model} ===")
            success = run_model_script(model)
            if success:
                print(f"Model {model} executed successfully!")
            else:
                print(f"Model {model} execution failed.")
    results=[]
    for model in models:
        model_results = get_latest_results(model)
        results.append(model_results)
    return ResponseMessage(200,'upload success', results).to_json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)