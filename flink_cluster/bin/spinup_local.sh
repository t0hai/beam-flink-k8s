#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
CONFIG_DIR=$SCRIPT_DIR/..
# use local Kubernetes
kubectl config use-context minikube

# make sure Flink components are able to reference themselves through a Kubernetes service
minikube ssh 'sudo ip link set docker0 promisc on'

# configuration and service definition
kubectl apply -f $CONFIG_DIR/flink-configuration-configmap.yaml
kubectl apply -f $CONFIG_DIR/jobmanager-service.yaml

# create the deployments for the cluster
kubectl apply -f $CONFIG_DIR/jobmanager-session-deployment.yaml
kubectl apply -f $CONFIG_DIR/taskmanager-session-deployment.yaml
