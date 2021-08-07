# Helm Chart for deployment of CrawlerX - Develop Extensible, Distributed, Scalable Crawler System

## Prerequisites

* Install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git), [Helm](https://helm.sh/docs/intro/install/)
(and Tiller) and [Kubernetes client](https://kubernetes.io/docs/tasks/tools/install-kubectl/) in order to run the 
steps provided in the below.

* An already setup [Kubernetes cluster](https://kubernetes.io/docs/setup/)

* Install [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/deploy/). You can find the Git release [`nginx-0.30.0`](https://github.com/kubernetes/ingress-nginx/releases/tag/nginx-0.30.0) here.

## Quick Start Guide

>In the context of this document,
>* `HELM_HOME` will refer to `CrawlerX/crawlerx_helm` directory.

#### 1. Clone the Kubernetes Resources for CrawlerX Git repository.
```
git clone https://github.com/leopardslab/CrawlerX.git
```

#### 2. Provide configurations.

Open the `<HELM_HOME>/values.yaml` and provide the following values.

| Parameter          | Description                         | Default Value               |
|--------------------|-------------------------------------|-----------------------------|
| crawlerx.subscription.username          |   Docker registry username                       | ""               |
| crawlerx.subscription.password          |   Docker registry password                       | ""               |

#### 3. Deploy CrawlerX distributed crawling platform.

- **Helm v2**

    ```
    helm install --name <RELEASE_NAME> <HELM_HOME> --namespace <NAMESPACE>
    ```

- **Helm v3**
 
    ```
    helm install <RELEASE_NAME> <HELM_HOME> --namespace <NAMESPACE>
    ```

`NAMESPACE` should be the Kubernetes Namespace in which the resources are deployed

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
