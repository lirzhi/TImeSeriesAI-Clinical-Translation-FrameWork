
## Get Started

1. Install Python 3.10.16

### Reproduce with Docker

To easily reproduce the results using Docker, conda and Make,  you can follow the next steps:
1. Pull basic docker images : 
```
docker pull condaforge/mambaforge
docker pull nvidia/cuda
docker pull wurstmeister/zookeeper
docker pull wurstmeister/kafka
``` 
2. Build docker images : 
```
docker-compose up
``` 
if failed , please try:
```
docker-compose bulid autoformer
docker-compose bulid informer
docker-compose bulid itransformer
docker-compose bulid time-mixer
docker-compose bulid large-timer
docker-compose bulid skin-rl
docker-compose bulid main

``` 
3. start kafka
```
docker run -d --name zookeeper -p 2181:2181 -t wurstmeister/zookeeper
docker run -d --name kafka --publish 9092:9092 --link zookeeper \
--env KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
--env KAFKA_ADVERTISED_HOST_NAME=localhost \
--env KAFKA_ADVERTISED_PORT=9092 \
wurstmeister/kafka:latest 
``` 
4. create topic
```
docker exec -it kafka bash
cd /opt/kafka/bin

# 创建模型请求Topics
./kafka-topics.sh --create \
    --bootstrap-server localhost:9092 \
    --topic autoformer_requests \
    --partitions 3 \
    --replication-factor 1 \
    --config retention.ms=604800000  # 保留7天

./kafka-topics.sh --create \
    --bootstrap-server localhost:9092 \
    --topic informer_requests \
    --partitions 3 \
    --replication-factor 1 \
    --config retention.ms=604800000

./kafka-topics.sh --create \
    --bootstrap-server localhost:9092 \
    --topic itransformer_requests \
    --partitions 3 \
    --replication-factor 1 \
    --config retention.ms=604800000

./kafka-topics.sh --create \
    --bootstrap-server localhost:9092 \
    --topic timemixer_requests \
    --partitions 3 \
    --replication-factor 1 \
    --config retention.ms=604800000

./kafka-topics.sh --create \
    --bootstrap-server localhost:9092 \
    --topic timer_requests \
    --partitions 3 \
    --replication-factor 1 \
    --config retention.ms=604800000

# 创建结果Topic
./kafka-topics.sh --create \
    --bootstrap-server localhost:9092 \
    --topic prediction_results \
    --partitions 6 \                # 更多分区以支持高并发结果写入
    --replication-factor 1 \
    --config retention.ms=2592000000  # 保留30天
``` 

5. Usage：http:127.0.0.1:5000

## Main Results


## Citation


## Contact



## Acknowledgement

We appreciate the following github repos a lot for their valuable code base or datasets:

https://github.com/thuml/Autoformer
https://github.com/zhouhaoyi/Informer2020
https://github.com/thuml/iTransformer
https://github.com/thuml/Large-Time-Series-Model
https://github.com/kwuking/TimeMixer
https://github.com/catarina-barata/Skin_RL
https://github.com/zhouhaoyi/ETDataset
