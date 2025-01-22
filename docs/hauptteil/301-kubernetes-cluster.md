---
layout: default
title: 3.1 Kubernetes Cluster
parent: 3. Hauptteil
nav_order: 301
---

# 3.1 Kubernetes Cluster

Wie bereits in der Einleitung erwähnt, ist es eine Basisanforderung an dieses Projekt, dass das ganze auf Kubernetes gehostet wird.
Deshalb wird die technische Umsetzung damit starten, sobald dies erledigt ist, kann die Entwicklung des Services starten.

![Kubernetes](../ressources/images/kubernetes/logo.png){: width="250px" }

[Quelle Bild - Icons](../anhang/600-quellen.html#64-icons)

Auf Hinweis von [Fabio Beti (Mitstudent von Marco Kälin)](https://github.com/fo-b) wird der Kubernetes Cluster auf AWS aufgesetzt.
Zuerst war der Plan, dies nach dem folgendem Tutorial zu erstellen.

<https://medium.com/@lubomir-tobek/eks-cluster-with-aws-cli-d72e4d77a11b>

Ziemlich rasch wurde jedoch klar, dass das Tool `EKSCTL` das Ganze nochmals vereinfachen kann.
[Mehr dazu im Kapitel 3.3](./303-cluster-erstellen.html)

Bevor jedoch diese Anleitung umgesetzt werden kann, muss überhaupt [ein AWS Account erstellt werden.](./302-aws-informationen.html)
