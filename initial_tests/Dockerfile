FROM registry.esss.lu.se/ics-docker/miniconda:latest

USER root

RUN yum install -y gcc-c++ \
  && /opt/conda/bin/conda config --system --add channels conda-eee \
  && conda create -n epics environment pvaccesscpp make cmake \
