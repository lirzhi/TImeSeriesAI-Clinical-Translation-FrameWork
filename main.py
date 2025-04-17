from email import message
from fileinput import filename
from http import client
import os
from pathlib import Path
import shutil
import subprocess
import time
import json
from kafka import KafkaProducer, KafkaConsumer
from flask import Flask, redirect, render_template, request, jsonify, url_for
from flask_cors import CORS
from common_util import ResponseMessage
import threading
import uuid

# 关键配置
from werkzeug.serving import WSGIRequestHandler
WSGIRequestHandler.protocol_version = "HTTP/1.1"

app = Flask(__name__, static_folder='templates')
CORS(app)

# Kafka配置
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092')
RESULT_TOPIC = 'prediction_results'
#脚本目录
SCRIPT_DIR = "./scripts"
# 模型配置
MODELS = {
    'Autoformer': {
        'request_topic': 'autoformer_requests',
        'consumer_group': 'autoformer_group'
    },
    'Informer': {
        'request_topic': 'informer_requests',
        'consumer_group': 'informer_group'
    },
    'iTransformer': {
        'request_topic': 'itransformer_requests',
        'consumer_group': 'itransformer_group'
    },
    'TimeMixer': {
        'request_topic': 'timemixer_requests',
        'consumer_group': 'timemixer_group'
    },
    'Timer': {
        'request_topic': 'timer_requests',
        'consumer_group': 'timer_group'
    }
}

# 全局结果存储和锁
global_results = {}
results_lock = threading.Lock()

# 创建Kafka生产者
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    acks='all',
    retries=3
)

class ModelConsumer(threading.Thread):
    """每个模型独立的消费者线程"""
    def __init__(self, model_name, request_topic, consumer_group):
        super().__init__()
        self.model_name = model_name
        self.request_topic = request_topic
        self.consumer_group = consumer_group
        self.daemon = True
        
    def run(self):
        consumer = KafkaConsumer(
            self.request_topic,
            bootstrap_servers=[KAFKA_BROKER],
            group_id=self.consumer_group,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        print(f"{self.model_name} consumer started on topic {self.request_topic}")
        
        for message in consumer:
            try:
                data = message.value
                print(f"{self.model_name} processing request: {data}")
                
                # 更新模型脚本配置
                self.update_model_script(data['filename'], data.get('is_training', '0'))
                
                # 执行预测脚本
                # script_path = os.path.join('./models', self.model_name, 'scripts', 'predict.sh')
                script_path = os.path.join(SCRIPT_DIR, f"{self.model_name}.sh")
                result = subprocess.run(
                    ["bash", script_path],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # 获取预测结果
                model_results = self.get_latest_results()
                
                # 发送结果
                producer.send(RESULT_TOPIC, value={
                    'request_id': data['request_id'],
                    'model': self.model_name,
                    'results': model_results,
                    'status': 'completed',
                    'timestamp': time.time()
                })
                
            except subprocess.CalledProcessError as e:
                print(f"{self.model_name} prediction failed: {e.stderr}")
                producer.send(RESULT_TOPIC, value={
                    'request_id': data['request_id'],
                    'model': self.model_name,
                    'status': 'failed',
                    'error': str(e.stderr),
                    'timestamp': time.time()
                })
            except Exception as e:
                print(f"{self.model_name} consumer error: {str(e)}")
                producer.send(RESULT_TOPIC, value={
                    'request_id': data['request_id'],
                    'model': self.model_name,
                    'status': 'error',
                    'error': str(e),
                    'timestamp': time.time()
                })
    
    def update_model_script(self, filename, is_training):
        """更新当前模型的脚本配置"""
        clean_name = Path(filename).stem
        script_path = os.path.join('./models', self.model_name, 'scripts', 'predict.sh')
        
        with open(script_path, 'r', encoding='utf-8') as f:
            script_content = f.read()
        
        import re
        script_content = re.sub(
            r'root_path=".*?"', 
            f'root_path="./dataset/{clean_name}/"', 
            script_content
        )
        script_content = re.sub(
            r'data_path=".*?"', 
            f'data_path="{filename}"', 
            script_content
        )
        script_content = re.sub(
            r'is_training=.*', 
            f'is_training={is_training}', 
            script_content
        )
        
        with open(script_path, 'w') as f:
            f.write(script_content)
    
    def get_latest_results(self, num_results=4):
        """获取当前模型的最新结果"""
        result_path = os.path.join('./models', self.model_name, 'results', 'result.json')
        try:
            with open(result_path, 'r') as f:
                results = json.load(f)
            latest_results = results[-num_results:] if len(results) > num_results else results
            return {
                'model': self.model_name,
                'result': latest_results
            }
        except Exception as e:
            return {
                'model': self.model_name,
                'error': str(e)
            }

# 结果收集消费者
def result_consumer():
    consumer = KafkaConsumer(
        RESULT_TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        group_id='results_consumer_group',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    print("Result consumer started, waiting for results...")
    
    for message in consumer:
        try:
            result_data = message.value
            request_id = result_data['request_id']
            
            with results_lock:
                if request_id not in global_results:
                    global_results[request_id] = {
                        'completed': 0,
                        'results': [],
                        'start_time': time.time()
                    }
                
                if result_data['status'] == 'completed':
                    global_results[request_id]['results'].append(result_data['results'])
                
                global_results[request_id]['completed'] += 1
                
        except Exception as e:
            print(f"Error processing result: {str(e)}")

# 启动所有消费者
def start_consumers():
    # 启动模型消费者
    for model_name, config in MODELS.items():
        consumer = ModelConsumer(
            model_name,
            config['request_topic'],
            config['consumer_group']
        )
        consumer.start()
    
    # 启动结果消费者
    t = threading.Thread(target=result_consumer)
    t.daemon = True
    t.start()

@app.route('/')
def index():
    return redirect(url_for("static", filename='predict.html'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    task = request.form.get('task', 'default')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files are allowed'}), 400
    
    filename = file.filename
    clean_name = Path(filename).stem
    
    # 保存文件到输入目录
    file.seek(0)
    input_dir = os.getenv('INPUT_DIR', './data')
    os.makedirs(input_dir, exist_ok=True)
    file_path = os.path.join(input_dir, filename)
    file.save(file_path)
    
    # 保存文件到各模型目录
    for model_name in MODELS:
        file.seek(0)
        model_input_dir = os.path.join('./models', model_name, 'dataset', clean_name)
        os.makedirs(model_input_dir, exist_ok=True)
        model_input_path = os.path.join(model_input_dir, filename)
        if os.path.exists(model_input_path):
            os.remove(model_input_path)
        file.save(model_input_path)
    res_data = {
        "status": 1,
        "task": None,
        "filename": None
    }
    res_data['filename']=file.filename
    res_data['task']=task
    return ResponseMessage(200, 'upload success', res_data).to_json()

@app.route('/predict', methods=['POST'])
def predict():
    filename = request.form.get('filename')
    task = request.form.get('task', 'default')
    is_training = request.form.get('is_training', '0')
    
    if not filename or not filename.endswith('.csv'):
        return jsonify({'error': 'Invalid filename'}), 400
    
    # 生成唯一请求ID
    request_id = str(uuid.uuid4())
    
    # 初始化结果存储
    with results_lock:
        global_results[request_id] = {
            'completed': 0,
            'results': [],
            'start_time': time.time()
        }
    
    # 向每个模型发送预测请求
    for model_name in MODELS:
        producer.send(MODELS[model_name]['request_topic'], value={
            'request_id': request_id,
            'filename': filename,
            'is_training': is_training,
            'task': task,
            'timestamp': time.time()
        })
    
    # 等待结果完成（保持原有同步接口）
    timeout = 300  # 5分钟超时
    while True:
        with results_lock:
            if global_results[request_id]['completed'] >= len(MODELS):
                results = global_results[request_id]['results']
                del global_results[request_id]
                return ResponseMessage(200, 'predict success', results).to_json()
            
            if time.time() - global_results[request_id]['start_time'] > timeout:
                del global_results[request_id]
                return ResponseMessage(408, 'Request timeout', []).to_json()
        
        time.sleep(0.5)

if __name__ == '__main__':
    start_consumers()
    app.run(host='0.0.0.0', port=5000)