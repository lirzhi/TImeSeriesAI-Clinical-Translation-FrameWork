
## Get Started

1. Install Python 3.10.16

### Reproduce with Docker

To easily reproduce the results using Docker, conda and Make,  you can follow the next steps:
1. Pull basic docker images : 
```
docker pull condaforge/mambaforge
docker pull nvidia/cuda
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
3. Usage：http:127.0.0.1:5000

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
