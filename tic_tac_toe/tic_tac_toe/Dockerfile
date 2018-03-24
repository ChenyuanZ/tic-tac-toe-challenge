FROM continuumio/anaconda3
MAINTAINER Chenyuan Zhang <chenyuan.zhang.alpha@gmail.com>
ADD . /tic_tac_toe
WORKDIR /tic_tac_toe
RUN conda update -n base conda && \
    conda install -y -c conda-forge tornado==5.0.1 && \
    conda install -y redis-py==2.10.6
EXPOSE 8888
CMD python main.py