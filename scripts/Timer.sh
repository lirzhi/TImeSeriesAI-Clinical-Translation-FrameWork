# docker run -i --rm -v "$(pwd)/models/Timer:/app" -w /app -e HOME=/temp mq-large-timer ./scripts/predict.sh
docker run -i --rm -v /var/run/docker.sock:/var/run/docker.sock  -v "$(pwd)/models/Timer:/app" -w /app -e HOME=/temp mq-large-timer ./scripts/predict.sh