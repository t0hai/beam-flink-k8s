# beam-flink-k8s
Example project for running Beam on Flink in Kubernetes based on [Müller Fourier's Medium article](https://python.plainenglish.io/apache-beam-flink-cluster-kubernetes-python-a1965f37b7cb).

## Requirements
* [kubectl](https://kubernetes.io/docs/tasks/tools/) installed

<details>
    <summary><b><i>Local Deployment</i></b></summary>

### Additional Requirements
* [docker](https://docs.docker.com/get-docker/) installed
* [minikube](https://minikube.sigs.k8s.io/docs/start/) installed

### Preparations
Docker service must be running:
```
start minikube
```
```
eval $(minikube -p minikube docker-env)
```
```
kubectl get all
```

</details>

<details>
    <summary><b><i>EKS Deployment</i></b></summary>

### Additional Requirements
* [eksctl](https://eksctl.io/introduction/#installation) installed

### Preparations
Activate AWS profile **if needed**:
```
export AWS_PROFILE=<your_profile>
```

Set AWS region:
```
export AWS_REGION=<your_region>
```

Set KMS key used for envelope encryption of Kubernetes secrets:
_(create a new customer managed KMS key if needed)_

```
export AWS_KMS_KEY_EKS=<your_key_arn>
```

Launch cluster (`envsubst` will substitute the evironment variables in the `.yaml` file for you):
```
envsubst < eks-flink-cluster.yaml | eksctl create cluster -f -
```

Check that your nodes have been created:
```
kubectl get nodes
```

Update the kubeconfig file to interact with you cluster:
```
aws eks update-kubeconfig --name beam-flink-eks
```

</details>
<br>

## Spin up Flink cluster

Create configuration and servive definitions:
```
kubectl apply -f flink-configuration-configmap.yaml
```
```
kubectl apply -f jobmanager-service.yaml
```

Launch Jobmanager (orchestrator) and Taskmanager (worker) deployments:
```
kubectl apply -f jobmanager-session-deployment.yaml
```
```
kubectl apply -f taskmanager-session-deployment.yaml
```

## Run Beam job

Check that jobmanager and taskmanager deployments & pods are ready:
```
kubectl get all
```

Init env variable to point to the endpoint of the jobmanager
```
export JOBMANAGER_ENDPOINT=$(k get pods -l app=flink,component=jobmanager -o jsonpath='{.items[].status.podIP}')
```

Submit job (`envsubst` will substitute the `JOBMANGER_ENDPOINT` for you):
```
envsubst < beam_wordcount_py.yaml | kubectl apply -f -
```

Monitor jobs by port forwarding and opening [localhost:8081](http://localhost:8081) for Flink dashboard
```
kubectl port-forward <service/flink-jobmanager> 8081:8081
```

Delete job (if needed):
```
kubectl delete -f beam_wordcount_py.yaml
```

## Shutdown Cluster

```
kubectl delete -f taskmanager-session-deployment.yaml
kubectl delete -f jobmanager-session-deployment.yaml
kubectl delete -f jobmanager-service.yaml
kubectl delete -f flink-configuration-configmap.yaml
```

<details>
    <summary><b><i>Local Deployment</i></b></summary>

```
minikube stop
```
</details>

<details>
    <summary><b><i>EKS Deployment</i></b></summary>

```
eksctl delete cluster --name beam-flink-eks
```
</details>