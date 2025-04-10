from email import message
from fileinput import filename
import os
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
    
    res_data['filename']=file.filename
    res_data['task']=task
    return ResponseMessage(200,'upload success', res_data).to_json()

@app.route('/predict', methods=['POST'])
    # 读取文件内容
def predict():  
    res_data = {
        "status": 1,
        "task": None,
        "results": None
    }
    filename = request.files['filename']
    task = request.form.get('task', 'default')
    
    if filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files are allowed'}), 400
    file = request.files['file']
    # 保存文件到输入目录
    input_dir = os.getenv('INPUT_DIR', './data')
    file_path = os.path.join(input_dir, file.filename)
    res_data['filename']=file.filename
    res_data['task']=task
    with open(file_path, 'r') as f:
        data = f.read()
    message={
        'data':data,
        'task':task
    }

    # for topic in TOPICS:
    #     producer.send(topic, value=message)

    #     producer.flush()
    
    # # 等待结果返回
    # time.sleep(10)  # 实际应用中应该使用更可靠的方式等待结果
    return ResponseMessage(200,'upload success', res_data).to_json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)