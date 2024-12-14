---
layout: default
title: 3.4 Cluster löschen
parent: 3. Hauptteil
nav_order: 303
---

# 3.4 Cluster löschen

Aus Kostengründen wird der Cluster nach einem Test / in NICHT Betriebszeiten gelöscht.
Ein AWS EKS Cluster laufen zu lassen kann sehr schnell mehrere hundert Franken im Monat kosten.

Einen Cluster zu erstellen kostet jedoch nichts. Daher MUSS nach jedem Testing / Betriebsfenster folgender Command ausgeführt werden, um den Cluster wieder zu löschen.

```bash
eksctl delete cluster --name eks-cluster
```

Alle Ressourcen welche irgendwie mit diesem Cluster verbunden sind, werden somit gelöscht.¨
