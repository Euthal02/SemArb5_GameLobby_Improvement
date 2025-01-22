---
layout: default
title: 3.9 Testing
parent: 3. Hauptteil
nav_order: 350
---

# 3.9 Testing

![Testing](../ressources/icons/testing.png){: style="width: 250px"" }

[Quelle Bild - Icons](../anhang/600-quellen.html#64-icons)

Das Testing der beiden Container Images ist automatisiert in der [Pipeline](../einleitung/208-pipelines.html). Getestet wird lediglich, ob das Image als ganzes funktioniert und gestartet werden kann. Bei je zwei Routen pro Container Applikation und zwei Python Funktionen, wurde bewusst auf Unit Test verzichtet. Sollte dies in Zukunft notwendig werden, muss dies noch integriert werde.

## Health Check

Das Testing ist der eigentliche Healtch Check, welcher auch von Kubernetes / Docker genutzt wird. Dazu wird der Container gestartet, der Webport exposed und anschliessend die `/health` Route aufgerufen.

```yaml
- name: Build and run container
  run: |
    cd gameroom
    docker build -t pong-game-room .
    docker run -d -p 5000:5000 --name pong-game-room-container pong-game-room

- name: Wait for container to be ready
  run: |
    for i in {1..10}; do
    if curl -s http://localhost:5000/health | grep 'OK'; then
        echo "Container is healthy!";
        exit 0;
    else
        echo "Waiting for container to be healthy...";
        sleep 5;
    fi
    done
    echo "Container health check failed.";
    exit 1
```

Der Healtcheck wird auch in der AWS Ingress Config genutzt, damit der Ingress weis, ab wann das Backend erreichbar ist.

```yaml
alb.ingress.kubernetes.io/healthcheck-protocol: HTTP
alb.ingress.kubernetes.io/healthcheck-path: /health
```

Sollte dieser Healthcheck also bereits beim Commit & Push failen, würde der Dienst auf dem Kubernetes Cluster nicht betroffen und würde weiter laufen.
