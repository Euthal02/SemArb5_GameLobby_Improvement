---
layout: default
title: 2.8 Pipelines
parent: 2. Einleitung
nav_order: 208
---

# 2.8 Pipelines

![Pipeline Execution](../ressources/icons/upload.png){: width="250px" }

[Quelle Bild - Icons](../anhang/600-quellen.html#64-icons)

Bei dieser Semesterarbeit wird die gleiche Methode für die Pipelines verfolgt, wie bei den letzten Arbeiten von Marco Kälin. Jedes Teilsystem der Arbeit sollte eine eigene Pipeline haben, welche nur auf dem Main Branch ausgeführt wird.

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

Genauere Informationen was jede Pipeline genau macht, wird im Hauptteil zu den einzelnen Teilsystemen spezifiziert.

## Vorkonfigurierte Aktionen

In GitHub Actions hat man die Möglichkeit vordefinierte Aktionen zu verwenden, welche es vereinfachen Operation in Actions vorzunehmen. So zum Beispiel die folgende Aktion ``docker/login-action@master``, welche sich bei einer Docker Registry anmeldet. Als User muss man nur noch die entsprechenden Anmeldedaten angeben und der Rest wird von dieser Action definiert.

```yaml
    - name: Log in to GHCR
      uses: docker/login-action@master
      with:
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
        registry: ${{ vars.REGISTRY }}
```

Mehr zu vordefinierten Actions hier:

[Link zur GitHub Dokuemntation](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/using-pre-written-building-blocks-in-your-workflow)
