# FROM continuumio/miniconda3:4.7.12
FROM condaforge/mambaforge:latest
ADD ./environment.yml ./environment.yml

# RUN conda install -n base -c conda-forge mamba && \
#     mamba env update -n base -f ./environment.yml && \
#     conda clean -afy
# 先安装 mamba
RUN conda update -y conda
RUN conda install -n base -c conda-forge mamba
# RUN conda install reformer-pytorch==1.4.4
# 再更新环境
RUN mamba env update -n base -f ./environment.yml

# 最后清理缓存
RUN conda clean -afy
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     gcc \
#     python3-dev
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install reformer-pytorch==1.4.4