FROM python:3.10.15-slim

# 安装docker客户端（必须与宿主机Docker版本兼容）
RUN apt-get update && \
    apt-get install -y docker.io && \
    rm -rf /var/lib/apt/lists/*

# 验证安装
RUN docker --version
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]