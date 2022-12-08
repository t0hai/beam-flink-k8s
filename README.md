# beam-flink-k8s
Example project for running Beam on Flink in Kubernetes based on Müller [Fourier's Medium article](https://python.plainenglish.io/apache-beam-flink-cluster-kubernetes-python-a1965f37b7cb)

## Requirements
* Python and pip installed
* [docker](https://docs.docker.com/get-docker/) installed
* [minikube](https://minikube.sigs.k8s.io/docs/start/) installed
* [kubectl](https://kubernetes.io/docs/tasks/tools/) installed

## Preparations
Docker service must be running
```
start minikube
```
```
eval $(minikube -p minikube docker-env)
```
```
kubectl get all
```
```
pip install apache-beam==2.43.0
```

## Steps
```
kubectl apply -f flink-configuration-configmap.yaml
```
```
kubectl apply -f jobmanager-service.yaml
```
```
kubectl apply -f jobmanager-session-deployment.yaml
```
```
kubectl apply -f taskmanager-session-deployment.yaml
```
```
kubectl apply -f beam_wordcount_py.yaml
```

## Monitor Jobs
find the `flink-jobmanager` service
```
kubectl get all
```

```
kubectl port-forward <service/flink-jobmanager> 8081:8081
```

open [localhost:8081](http://localhost:8081) for Flink dashboard

## Shutdown Job
```
kubectl detele -f beam_wordcount_py.yaml
```