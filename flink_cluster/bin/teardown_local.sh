#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
CONFIG_DIR=$SCRIPT_DIR/..
# use local Kubernetes
kubectl config use-context minikube

kubectl delete -f $CONFIG_DIR/taskmanager-session-deployment.yaml
kubectl delete -f $CONFIG_DIR/jobmanager-session-deployment-non-ha.yaml
kubectl delete -f $CONFIG_DIR/jobmanager-service.yaml
kubectl delete -f $CONFIG_DIR/flink-configuration-configmap.yaml
