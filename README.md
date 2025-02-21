## Airflow learning project

### Start minikube
```bash
minikube start --driver="docker" --cni="auto" --cpus="no-limit" --memory="no-limit" --kubernetes-version='v1.28.6'
```

### Install airflow
```bash
helm repo add apache-airflow https://airflow.apache.org
helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace --values values.yaml
```

## Optional:

### enable metalb
```bash
minikube addons enable metallb
```

Get minikube ip
```bash
minikube ip
```

#### Set Load Balancer Start and End IP:
Example 1:
```bash
$ minikube ip
192.168.49.2
$ minikube addons configure  metallb
-- Enter Load Balancer Start IP: 192.168.49.100
-- Enter Load Balancer End IP: 192.168.49.110
```

Example 2:
```bash
$ minikube ip
10.100.15.2
$ minikube addons configure  metallb
-- Enter Load Balancer Start IP: 10.100.15.100
-- Enter Load Balancer End IP: 10.100.15.110
```

### Install istio
```bash
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update
helm install istio-base istio/base -n istio-system --set defaultRevision=default --create-namespace --version=1.19.1
helm install istiod istio/istiod -n istio-system --wait --version=1.19.1
helm install internal-default istio/gateway -n kube-istio-gateway --wait --create-namespace --version=1.19.1
```

### Add istio virtual service
```bash
kubectl apply -f manifests/virtual-service-airflow.yaml
```

```bash
$ echo "connect to airflow by istio: http://$(kubectl -n kube-istio-gateway get svc internal-default -o jsonpath='{.status.loadBalancer.ingress[0].ip}')/"
connect to airflow by istio: http://192.168.49.100/
```