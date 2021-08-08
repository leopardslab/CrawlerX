# Helm Chart for deployment of CrawlerX - Develop Extensible, Distributed, Scalable Crawler System

## Prerequisites

* Install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), [Helm](https://helm.sh/docs/intro/install/)
(and Tiller) and [Kubernetes client](https://kubernetes.io/docs/tasks/tools/install-kubectl/) in order to run the 
steps provided in the below.

* An already setup [Kubernetes cluster](https://kubernetes.io/docs/setup/)

* Install [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/deploy/). You can find the Git release [`nginx-0.30.0`](https://github.com/kubernetes/ingress-nginx/releases/tag/nginx-0.30.0) here.

![Helm Deployment](../resources/helm.png)

## Quick Start Guide

>In the context of this document,
>* `HELM_HOME` will refer to `CrawlerX/crawlerx_helm` directory.

#### 1. Clone the Kubernetes Resources for CrawlerX Git repository.
```
git clone https://github.com/leopardslab/CrawlerX.git
```

#### 2. Provide configurations.

Open the `<HELM_HOME>/values.yaml` and provide the following values.

##### User Docker registry authentication parameters
| Parameter          | Description                         | Default Value               |
|--------------------|-------------------------------------|-----------------------------|
| crawlerx.subscription.username          |   Docker registry username                       | ""               |
| crawlerx.subscription.password          |   Docker registry password                       | ""               |

##### CrawlerX web application configurations
| Parameter          | Description                         | Default Value               |
|--------------------|-------------------------------------|-----------------------------|
| crawlerx.deployment.webApp.dockerRegistry          |   Docker registry of web application          | ""               |
| crawlerx.deployment.webApp.imageName          |   Docker image of web application          | "scorelabs/crawlerx-app"               |
| crawlerx.deployment.webApp.imageTag          |   Docker image tag of web application          | "1.0.0"               |
| crawlerx.deployment.webApp.imagePullSecrets          |   Docker image pull secret          | ""               |
| crawlerx.deployment.webApp.replicas          |   Web application number of instances          | 1               |
| crawlerx.deployment.webApp.strategy.rollingUpdate.maxSurge          |   Pod max surge          | 1               |
| crawlerx.deployment.webApp.strategy.rollingUpdate.maxUnavailable          |   Pod max unavailable          | 0               |
| crawlerx.deployment.webApp.livenessProbe.initialDelaySeconds  |   Number of seconds after the container has started before liveness probes are initiated.          | 35               |
| crawlerx.deployment.webApp.livenessProbe.periodSeconds      |  How often (in seconds) to perform the probe.       | 10              |
| crawlerx.deployment.webApp.readinessProbe.initialDelaySeconds      |  Number of seconds after the container has started before readiness probes are initiated.       | 35              |
| crawlerx.deployment.webApp.readinessProbe.initialDelaySeconds      |  How often (in seconds) to perform the probe.       | 10             |
| crawlerx.deployment.webApp.resources.requests.memory  |  The minimum amount of memory that should be allocated for a Pod   | "512Mi"             |
| crawlerx.deployment.webApp.resources.requests.cpu  |  The minimum amount of CPU that should be allocated for a Pod   | "400m"             |
| crawlerx.deployment.webApp.resources.limits.memory  |  The maximum amount of memory that should be allocated for a Pod   | "1Gi"             |
| crawlerx.deployment.webApp.resources.limits.cpu  |  The maximum amount of CPU that should be allocated for a Pod   | "1000m"            |
| crawlerx.deployment.webApp.envs  |  Environment variables for the deployment.   | ""            |


##### CrawlerX backend application configurations
| Parameter          | Description                         | Default Value               |
|--------------------|-------------------------------------|-----------------------------|
| crawlerx.deployment.backend.dockerRegistry          |   Docker registry of backend application          | ""               |
| crawlerx.deployment.backend.imageName          |   Docker image of backend application          | "scorelabs/crawlerx-backend"               |
| crawlerx.deployment.backend.imageTag          |   Docker image tag of backend application          | "1.0.0"               |
| crawlerx.deployment.backend.imagePullSecrets          |   Docker image pull secret          | ""               |
| crawlerx.deployment.backend.replicas          |   Backend application number of instances          | 1               |
| crawlerx.deployment.backend.strategy.rollingUpdate.maxSurge          |   Pod max surge          | 1               |
| crawlerx.deployment.backend.strategy.rollingUpdate.maxUnavailable          |   Pod max unavailable          | 0               |
| crawlerx.deployment.backend.livenessProbe.initialDelaySeconds  |   Number of seconds after the container has started before liveness probes are initiated.          | 35               |
| crawlerx.deployment.backend.livenessProbe.periodSeconds      |  How often (in seconds) to perform the probe.       | 10              |
| crawlerx.deployment.backend.readinessProbe.initialDelaySeconds      |  Number of seconds after the container has started before readiness probes are initiated.       | 35              |
| crawlerx.deployment.backend.readinessProbe.initialDelaySeconds      |  How often (in seconds) to perform the probe.       | 10             |
| crawlerx.deployment.backend.resources.requests.memory  |  The minimum amount of memory that should be allocated for a Pod   | "512Mi"             |
| crawlerx.deployment.backend.resources.requests.cpu  |  The minimum amount of CPU that should be allocated for a Pod   | "400m"             |
| crawlerx.deployment.backend.resources.limits.memory  |  The maximum amount of memory that should be allocated for a Pod   | "1Gi"             |
| crawlerx.deployment.backend.resources.limits.cpu  |  The maximum amount of CPU that should be allocated for a Pod   | "1000m"            |
| crawlerx.deployment.backend.envs  |  Environment variables for the deployment.   | ""            |

##### CrawlerX Scrapy application configurations
| Parameter          | Description                         | Default Value               |
|--------------------|-------------------------------------|-----------------------------|
| crawlerx.deployment.scrapyApp.dockerRegistry          |   Docker registry of Scrapy application          | ""               |
| crawlerx.deployment.scrapyApp.imageName          |   Docker image of Scrapy application          | "scorelabs/crawlerx-scrapy-app"              |
| crawlerx.deployment.scrapyApp.imageTag          |   Docker image tag of Scrapy application          | "1.0.0"               |
| crawlerx.deployment.scrapyApp.imagePullSecrets          |   Docker image pull secret          | ""               |
| crawlerx.deployment.scrapyApp.replicas          |   Scrapy application number of instances          | 1               |
| crawlerx.deployment.scrapyApp.strategy.rollingUpdate.maxSurge          |   Pod max surge          | 1               |
| crawlerx.deployment.scrapyApp.strategy.rollingUpdate.maxUnavailable          |   Pod max unavailable          | 0               |
| crawlerx.deployment.scrapyApp.livenessProbe.initialDelaySeconds  |   Number of seconds after the container has started before liveness probes are initiated.          | 35               |
| crawlerx.deployment.scrapyApp.livenessProbe.periodSeconds      |  How often (in seconds) to perform the probe.       | 10              |
| crawlerx.deployment.scrapyApp.readinessProbe.initialDelaySeconds      |  Number of seconds after the container has started before readiness probes are initiated.       | 35              |
| crawlerx.deployment.scrapyApp.readinessProbe.initialDelaySeconds      |  How often (in seconds) to perform the probe.       | 10             |
| crawlerx.deployment.scrapyApp.resources.requests.memory  |  The minimum amount of memory that should be allocated for a Pod   | "512Mi"             |
| crawlerx.deployment.scrapyApp.resources.requests.cpu  |  The minimum amount of CPU that should be allocated for a Pod   | "400m"             |
| crawlerx.deployment.scrapyApp.resources.limits.memory  |  The maximum amount of memory that should be allocated for a Pod   | "1Gi"             |
| crawlerx.deployment.scrapyApp.resources.limits.cpu  |  The maximum amount of CPU that should be allocated for a Pod   | "1000m"            |
| crawlerx.deployment.scrapyApp.envs  |  Environment variables for the deployment.   | ""            |

##### CrawlerX Celery Beat and Worker configurations
| Parameter          | Description                         | Default Value               |
|--------------------|-------------------------------------|-----------------------------|
| crawlerx.deployment.celery.dockerRegistry          |   Docker registry of Celery application          | ""               |
| crawlerx.deployment.celery.imageName          |   Docker image of Celery application          | "scorelabs/crawlerx-backend"             |
| crawlerx.deployment.celery.imageTag          |   Docker image tag of Celery application          | "1.0.0"               |
| crawlerx.deployment.celery.imagePullSecrets          |   Docker image pull secret          | ""               |
| crawlerx.deployment.celery.beat.replicas          |   Celery beat number of instances          | 1               |
| crawlerx.deployment.celery.worker.replicas          |   Celery worker number of instances          | 1               |
| crawlerx.deployment.celery.strategy.rollingUpdate.maxSurge          |   Pod max surge          | 1               |
| crawlerx.deployment.celery.strategy.rollingUpdate.maxUnavailable          |   Pod max unavailable          | 0               |
| crawlerx.deployment.celery.livenessProbe.initialDelaySeconds  |   Number of seconds after the container has started before liveness probes are initiated.          | 35               |
| crawlerx.deployment.celery.livenessProbe.periodSeconds      |  How often (in seconds) to perform the probe.       | 10              |
| crawlerx.deployment.celery.readinessProbe.initialDelaySeconds      |  Number of seconds after the container has started before readiness probes are initiated.       | 35              |
| crawlerx.deployment.celery.readinessProbe.initialDelaySeconds      |  How often (in seconds) to perform the probe.       | 10             |
| crawlerx.deployment.celery.resources.requests.memory  |  The minimum amount of memory that should be allocated for a Pod   | "512Mi"             |
| crawlerx.deployment.celery.resources.requests.cpu  |  The minimum amount of CPU that should be allocated for a Pod   | "400m"             |
| crawlerx.deployment.celery.resources.limits.memory  |  The maximum amount of memory that should be allocated for a Pod   | "1Gi"             |
| crawlerx.deployment.celery.resources.limits.cpu  |  The maximum amount of CPU that should be allocated for a Pod   | "1000m"            |
| crawlerx.deployment.celery.envs  |  Environment variables for the deployment.   | ""            |

##### CrawlerX environment variables
| Parameter          | Description                         | Default Value               |
|--------------------|-------------------------------------|-----------------------------|
| crawlerx.env.webApp.VUE_APP_FIREBASE_API_KEY  |  Firebase app key   | ""            |
| crawlerx.env.webApp.VUE_APP_FIREBASE_AUTH_DOMAIN  |  Firebase auth domain   | ""            |
| crawlerx.env.webApp.VUE_APP_FIREBASE_DB_DOMAIN  |  Firebase db domain   | ""            |
| crawlerx.env.webApp.VUE_APP_FIREBASE_PROJECT_ID  |  Firebase project id   | ""            |
| crawlerx.env.webApp.VUE_APP_FIREBASE_STORAGE_BUCKET  |  Firebase storage bucket   | ""            |
| crawlerx.env.webApp.VUE_APP_FIREBASE_MESSAGING_SENDER_ID  |  Firebase messaging sender id   | ""            |
| crawlerx.env.webApp.VUE_APP_FIREBASE_APP_ID  |  Firebase app id   | ""            |
| crawlerx.env.webApp.VUE_APP_FIREBASE_MEASURMENT_ID  |  Firebase measurement id   | ""            |
| crawlerx.env.webApp.VUE_APP_DJANGO_PROTOCOL  |  backend server protocol   | "http"            |
| crawlerx.env.webApp.VUE_APP_DJANGO_PORT  |  backend server port   | "8000"            |
| crawlerx.env.webApp.VUE_APP_DJANGO_PORT  |  backend server port   | "8000"            |
| crawlerx.env.backend.DJANGO_ADMIN_USERNAME  |  backend admin username  | "admin"            |
| crawlerx.env.backend.DJANGO_ADMIN_PASSWORD  |  backend admin password  | "admin"            |
| crawlerx.env.backend.DJANGO_ADMIN_EMAIL  |  backend admin email  | "admin@scorelab.org"            |
| crawlerx.env.elasticsearch.ELASTIC_SEARCH_USERNAME  |  elasticsearch username  | "admin"            |
| crawlerx.env.elasticsearch.ELASTIC_SEARCH_PASSWORD  |  elasticsearch password  | "admin"            |
| mongodb.auth.database  |  Mongodb database name  | "crawlerx_db"            |
| mongodb.auth.port  |  Mongodb database port  | 27017            |
| rabbitmq.auth.username  |  RabbitMQ admin username  | "guest"            |
| rabbitmq.auth.password  |  RabbitMQ admin password  | "guest"            |
| rabbitmq.service.port  |  RabbitMQ service port  | 5672           |


#### 3. Deploy CrawlerX distributed crawling platform.

- **Helm v2**

    ```
    kubectl create ns <NAMESPACE>
    helm dependency update
    helm install --name <RELEASE_NAME> <HELM_HOME> --namespace <NAMESPACE>
    ```

- **Helm v3**
 
    ```
    helm install <RELEASE_NAME> <HELM_HOME> --namespace <NAMESPACE> --dependency-update --create-namespace
    ```

`NAMESPACE` should be the Kubernetes Namespace in which the resources are deployed

![Helm Deployment](https://github.com/leopardslab/CrawlerX/blob/master/resources/helm/helm_5.png)

#### 4. Access CrawlerX dashboard.

1. Obtain the external IP (`EXTERNAL-IP`) of the Ingress resources by listing down the Kubernetes Ingresses.

```
kubectl get ing -n <NAMESPACE>
```

```
NAME                                            HOSTS                      ADDRESS         PORTS     AGE
<RELEASE_NAME>-web-app-ingress                  app.crawlerx.com           <EXTERNAL-IP>   80        3m
```

2. Add the above host as an entry in `/etc/hosts` file as follows:

```
<EXTERNAL-IP>	app.crawlerx.com
```

3. Open `http://app.crawlerx.com` to view the CrawlerX web UI in the browser.

#### 5. Access Other Resources.

1. Get Pods
```
kubectl get pods -n <NAMESPACE>
```
![Pods](https://github.com/leopardslab/CrawlerX/blob/master/resources/helm/helm_1.png)

2. Get Services
```
kubectl get svc -n <NAMESPACE>
```
![Pods](https://github.com/leopardslab/CrawlerX/blob/master/resources/helm/helm_2.png)

3. Get Ingress
```
kubectl get ing -n <NAMESPACE>
```
![Pods](https://github.com/leopardslab/CrawlerX/blob/master/resources/helm/helm_3.png)

4. Get Config Maps
```
kubectl get configmaps -n <NAMESPACE>
```
![Pods](https://github.com/leopardslab/CrawlerX/blob/master/resources/helm/helm_4.png)
