---
layout: default
title: 3.6 HELM Deployment
parent: 3. Hauptteil
nav_order: 306
---

# 3.6 HELM Deployment

Um nun den GameRoom und die GameLobby auf den Cluster zu bringen, haben wir folgende Helm Chart geschrieben:

<https://github.com/Euthal02/SemArb4_GameLobby/tree/main/helm>

Das values File beinhaltet all Variablen, welche wir im Chart verwenden.

```yaml
#file: values.yaml

namespace: pong-game

room:
  replicaCount: 1
  image:
    repository: ghcr.io/euthal02/pong-gameroom
    tag: latest
    pullPolicy: Always
  service:
    port: 5000
    targetport: 5000
    protocol: TCP
    type: NodePort
  ingress:
    enabled: true
    className: alb
    annotations:
      alb.ingress.kubernetes.io/scheme: internet-facing
      alb.ingress.kubernetes.io/target-type: ip
      alb.ingress.kubernetes.io/backend-protocol: HTTP
      alb.ingress.kubernetes.io/healthcheck-protocol: HTTP
      alb.ingress.kubernetes.io/healthcheck-path: /health
      alb.ingress.kubernetes.io/load-balancer-attributes: 'idle_timeout.timeout_seconds=3600'
    tls: 
      enabled: false
      secretName: ""
```

Für jedes Deployment in unserem Cluster möchten wir einen neuen Namespace erstellen. Dasselbe gilt auch für den GameRoom und die GameLobby. Wie man in diesem Value File sehen kann, nutzen wir den Namespace ``pong-game``.

Wichtig hervorzuheben sind die Ingress Attribute. Mit Ihnen wird der AWS LoadBalancer konfiguriert. Alle Werte entsprechen einer Config Option des ALB. Hier zum Beispiel wird der ALB öffentlich erreichbar konfiguriert und ein Healthcheck konfiguriert.

```yaml
alb.ingress.kubernetes.io/scheme: internet-facing
alb.ingress.kubernetes.io/target-type: ip
alb.ingress.kubernetes.io/backend-protocol: HTTP
alb.ingress.kubernetes.io/healthcheck-protocol: HTTP
alb.ingress.kubernetes.io/healthcheck-path: /health
alb.ingress.kubernetes.io/load-balancer-attributes: 'idle_timeout.timeout_seconds=3600'
```

Die Variablen aus dem Value File werden anschliessend in den eigentlichen Konfigurationsfile verwendet.

Zum Beispiel bei den Services. Hier werden zwei Services erstellt, zum einen für den GameRoom und zum anderen für die GameLobby.

```yaml
apiVersion: v1
kind: Service
metadata:
  namespace: {{ .Values.namespace }}
  name: "{{ .Release.Name }}room"
  labels:
    app: "{{ .Release.Name }}room"
spec:
  type: {{ .Values.room.service.type }}
  ports:
  - port: {{ .Values.room.service.port }}
    targetPort: {{ .Values.room.service.targetport }}
    protocol: {{ .Values.room.service.protocol }}
  selector:
    app: "{{ .Release.Name }}room"
---
apiVersion: v1
kind: Service
metadata:
  namespace: {{ .Values.namespace }}
  name: "{{ .Release.Name }}lobby"
  labels:
    app: "{{ .Release.Name }}lobby"
spec:
  type: {{ .Values.lobby.service.type }}
  ports:
  - port: {{ .Values.lobby.service.port }}
    targetPort: {{ .Values.lobby.service.targetport }}
    protocol: {{ .Values.lobby.service.protocol }}
  selector:
    app: "{{ .Release.Name }}lobby"
```

Für den Gameroom wird jeder Service, Ingress und Pod 10-fach erstellt. Das eigentliche Ziel das ganze Variabel zu skalieren kann jedoch später noch eingebaut werden.
