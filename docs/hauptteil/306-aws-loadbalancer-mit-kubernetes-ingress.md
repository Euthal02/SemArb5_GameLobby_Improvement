---
layout: default
title: 3.5.1 AWS Loadbalancer mit Kubernetes Ingress
parent: 3.5 K8S Plugins
grandparent: 3. Hauptteil
nav_order: 306
---

# 3.5.1 AWS Loadbalancer mit Kubernetes Ingress

Von Seite AWS wird vorgeschlagen, ihren Loadbalancer als Ingress für Kubernetes zu verwenden. Dies ermöglicht es, den Ingress schnell und einfach öffentlich erreichbar zu machen.

![AWS Loadbalancer](../ressources/images/aws/loadbalancer.jpg)

[Quelle Bild - AWS Loadbalancer](../anhang/600-quellen.html#616-aws-loadbalancer)

Unter diesem Link ist eine sehr detailierte ANleitung zu finden:

<https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html>

Das ganze ist auch bereits in dem Build Script integriert, so dass dieser Schritt nicht mehr manuell auszuführen ist.

Sollte dies trotzdem der Fall sein, werden hier die Schritte erklärt und die Beweggründe dahinter.

## Installation

Zuerst  muss eine neue IAM Rolle erstellt werde.

Dies aus dem Grund, dass der Kubernetes Cluster bei einem Ingress Deployment, selbstständig neue Ressourcen generieren muss. Die benötigten Rechte bekommt man mit dem IAM Service Account.

### IAM User erstellen

AWS bietet hier eine Vorlage, welche man 1 zu 1 kopieren kann. Sie erlaubt dem Cluster alle Ressourcen zu erstellen welche er braucht. Mehr Informationen findet man im Code Fenster.

```bash
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.7.2/docs/install/iam_policy.json
aws iam create-policy --policy-name AWSLoadBalancerControllerIAMPolicy --policy-document file://iam_policy.json
eksctl create iamserviceaccount --cluster=eks-cluster --namespace=kube-system --name=aws-load-balancer-controller --role-name AmazonEKSLoadBalancerControllerRole --attach-policy-arn=arn:aws:iam::*********:policy/AWSLoadBalancerControllerIAMPolicy --approve
```

Auf Seiten AWS ist nun also alles bereit, damit der Cluster die Ressourcen erstellen kann.
Als nächstes müssen wir den Cluster dementsprechend konfigurieren.

### HELM Software Komponenten Install on Cluster

AWS bietet auch dazu einen einfachen Weg an, dies mit einem HELM Chart zu erledigen.

```bash
helm repo add eks https://aws.github.io/eks-charts
helm install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system --set clusterName=eks-cluster --set serviceAccount.create=false --set serviceAccount.name=aws-load-balancer-controller
wget https://raw.githubusercontent.com/aws/eks-charts/master/stable/aws-load-balancer-controller/crds/crds.yaml
kubectl apply -f crds.yaml
```

### Test Applikation

Um zu testen ob dies auch wirklich funktioniert bietet sich eine kleine Testapplikation an.

```bash
mka@Tuxedo-Laptop:~$ kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.7.2/docs/examples/2048/2048_full.yaml
namespace/game-2048 created
deployment.apps/deployment-2048 created
service/service-2048 created
ingress.networking.k8s.io/ingress-2048 created
mka@Tuxedo-Laptop:~$ kubectl get ingress/ingress-2048 -n game-2048
NAME           CLASS   HOSTS   ADDRESS                                                                      PORTS   AGE
ingress-2048   alb     *       k8s-game2048-ingress2-04c19700e8-1901553064.eu-central-2.elb.amazonaws.com   80      15s
```

Dies erstellt einen Loadbalancer, welcher den Traffic auf der URl weiterleitet an die Nodes.

<http://k8s-game2048-ingress2-04c19700e8-608089310.eu-central-2.elb.amazonaws.com/>

![Loadbalancer](../ressources/images/kubernetes/loadbalancer.PNG){: style="width: 450px" }

Wenn wir die URL des Loadbalancers in einem Browser aufrufen, ist der Service direkt verfügbar.

![Spiel](../ressources/images/kubernetes/2048_spiel.PNG){: style="width: 250px" }

Das Deployment dieses Spiel ist dabei sehr einfach.

```yaml
---
apiVersion: v1
kind: Namespace
metadata:
  name: game-2048
---
apiVersion: apps/v1
kind: Deployment
metadata:
  namespace: game-2048
  name: deployment-2048
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: app-2048
  replicas: 2
  template:
    metadata:
      labels:
        app.kubernetes.io/name: app-2048
    spec:
      containers:
      - image: public.ecr.aws/l6m2t8p7/docker-2048:latest
        imagePullPolicy: Always
        name: app-2048
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  namespace: game-2048
  name: service-2048
spec:
  ports:
    - port: 80
      targetPort: 80
      protocol: TCP
  type: NodePort
  selector:
    app.kubernetes.io/name: app-2048
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  namespace: game-2048
  name: ingress-2048
  annotations:
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
spec:
  ingressClassName: alb
  rules:
    - http:
        paths:
        - path: /
          pathType: Prefix
          backend:
            service:
              name: service-2048
              port:
                number: 80
```

## Konfiguration für das eigene Spiel

Für unsere Apllikationen bedeutet dies lediglich das hinzufügen einiger Annotations im Helm Chart. Sobald der Ingress mit diesem Chart deployed wird, werden diese Annotations genutzt um den Ingress auf der AWS Seite zu konfigurieren.

```yaml
alb.ingress.kubernetes.io/scheme: internet-facing
alb.ingress.kubernetes.io/target-type: ip
alb.ingress.kubernetes.io/backend-protocol: HTTP
alb.ingress.kubernetes.io/healthcheck-protocol: HTTP
alb.ingress.kubernetes.io/healthcheck-path: /health
alb.ingress.kubernetes.io/listen-ports: '[{"HTTP": 80}]'
alb.ingress.kubernetes.io/load-balancer-attributes: 'idle_timeout.timeout_seconds=3600'
```

Damit wird ein Standard Ingress erstellt, mit welchem der Service erreichbar ist.
