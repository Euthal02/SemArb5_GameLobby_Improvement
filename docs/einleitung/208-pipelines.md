---
layout: default
title: 2.8 Pipelines
parent: 2. Einleitung
nav_order: 208
---

# 2.8 Pipelines

![Pipeline Execution](../ressources/icons/upload.png){: width="250px" }

[Quelle Bild - Icons](./600-quellen.html#64-icons)

Ich werde bei dieser Semesterarbeit die gleiche Methode für die Pipelines verfolgen, wie bei der letzten. Jedes Teilsystem der Arbeit sollte eine eigene Pipeline haben, welche nur auf dem Main Branch ausgeführt wird.

Die Unterscheidung zwischen den einzelnen Komponenten wird mit Unterordner erreicht. Nur falls Änderungen in den Unterordner gibt, werden diese Pipelines auch ausgeführt.

Hier zum Beispiel die Config für GitHub Pages. Nur falls es Änderungen im Unterordner "docs" gibt, welche auf den "main" Branch gepusht werden, wird diese Pipeline ausgeführt.

``` yaml
# build on push
on: 
  push:
    # this means that the workflow will only trigger if there are changes in this directory
    paths:
      - 'docs/**'
    branches:
      - main
```

[Die einzelnen Workflows finden sich hier.](https://github.com/Euthal02/SemArb4_GameLobby/tree/main/.github/workflows)

Genauere Informationen was jede Pipeline genau macht, werde ich im Hauptteil zu den einzelnen Teilsystemen spezifizieren.
