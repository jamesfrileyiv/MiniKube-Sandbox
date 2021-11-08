#!/bin/bash

# Docker is the preferred driver for MiniKube, so first we must install docker-engine
#update
sudo apt -y update

# install docker-engine from convenience script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# install minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# set default driver to docker
minikube config set driver docker

# cannot manage minikube as root user, so need to create a docker group
# sudo groupadd docker
# sudo usermod -aG docker vagrant      # vagrant is default user for vagrant provisioned VMs

sudo newgrp docker
sudo usermod -aG docker vagrant # && newgrp docker
