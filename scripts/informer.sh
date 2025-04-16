# docker run -i --rm -v "$(pwd)/models/informer:/app" -w /app -e HOME=/temp mq-informer ./scripts/predict.sh
#!/bin/bash
# 使用宿主机docker执行（需确保宿主机docker可用）
docker run -i --rm -v /var/run/docker.sock:/var/run/docker.sock  -v "$(pwd)/models/informer:/app" -w /app -e HOME=/temp mq-informer ./scripts/predict.sh