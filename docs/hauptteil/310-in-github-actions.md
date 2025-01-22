---
layout: default
title: 3.6.1 ...in GitHub Actions
parent: 3.6 HELM Deployment
grandparent: 3. Hauptteil
nav_order: 310
---

# 3.6.1 ...in GitHub Actions

![Risks](../ressources/icons/risks.png){: style="width: 250px" }

[Quelle Bild - Icons](../anhang/600-quellen.html#64-icons)

Mit dem vorhin erklärten HELm Deployment, kann man nun also unser Spiel auf den Cluster bringen. Da dies aber kontinuierlich geschehen muss (CI/CD) wurde das Deployment in die [GitHub Actions Pipelines](../einleitung/208-pipelines.html) integriert.

Dafür wurde der Deploy Step bei beiden Pipelines so konfiguriert, dass dies mittels Secrets funktioniert.

{% raw %}

```yaml
deploy-job:
  runs-on: ubuntu-latest
  environment: gamelobby
  needs: build-job
  steps:
    - name: Checkout Repo
    uses: actions/checkout@main

    - name: Configure AWS credentials
    uses: aws-actions/configure-aws-credentials@main
    with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ vars.AWS_REGION }}

    - name: Create Kubeconfig file 
    run: |
        aws eks update-kubeconfig --name ${{ vars.EKS_CLUSTER_NAME }} --region ${{ vars.AWS_REGION }}
        echo 'KUBE_CONFIG_DATA<<EOF' >> $GITHUB_ENV
        echo $(cat ~/.kube/config | base64) >> $GITHUB_ENV
        echo 'EOF' >> $GITHUB_ENV

    - name: Kubectl and Helm Deploy
    id: command_exec
    uses: koslib/helm-eks-action@master
    env:
        KUBE_CONFIG_DATA: ${{ env.KUBE_CONFIG_DATA }}
    with:
        command: |
        helm upgrade pong-game-lobby ./gamelobby/helm/. -i --force

    - name: Print Response from Kubectl and Helm
    run: echo "${{ steps.command_exec.outputs.response }}"
```

{% endraw %}

Nachfolgend werden die einzelnen Schritte durchgegangen und erklärt.

## Checkout Repo

Dieser Schritt checkt lediglich das Repo aus. Anders gesagt, es holt eine lokale Kopie auf den Runner.

## Configure AWS credentials & Create Kubeconfig file

In diesen beiden Schritten, werden die AWS API Secrets genutzt, damit sich der Runner bei der AWS CLI anmelden kann und das Kubeconfig File erstellen kann. Die Secrets sind in GitHub hinterlegt und sind momentan mit dem Admin User verbunden. Das bedeutet, dass es theoretisch möglich ist, mit diesen Credentials weitere Ressourcen hinzuzufügen.

{: .warning }
Dies ist so sicherheitskritisch und muss korrigiert werden, bevor das Projekt Live geht. Das Problem ist, dass hier der Default Admin User verwendet wird, statt einem spezifischen User für das Deployment.

Die eigentliche Kubeconfig wird in die ``KUBE_CONFIG_DATA`` Variable abgefüllt, damit diese Daten im Actions Image ``koslib/helm-eks-action@master`` auch verfügbar ist. Da dies eine vorkonfigurierte Action ist und als ``DinD`` verwendet wird, wäre das erstellte Kkubeconfig File nicht verfügbar.

## Kubectl and Helm Deploy & Print Response from Kubectl and Helm

In diesen beiden Schritten wird der eigentliche Deploy gemacht. Dazu wird der Command ``helm upgrade pong-game-lobby ./gamelobby/helm/. -i --force`` ausgeführt. Dies mit der Kube Config, welche über die Variable ``KUBE_CONFIG_DATA`` übergeben wird.

Der Helm Command upgraded dazu das Release ``pong-game-lobby``, mit dem HELM Chart in folgendem Unterordner ``./gamelobby/helm/.``. Sollte es dieses Release noch nicht geben, oder falls es dieses bereits gibt, wird es immer überschrieben ``-i --force``.

Zum Ende wird noch der Output dieses Helm Commands geprintet, damit man zu Debug Zwekcen sehen kann, was genau passiert ist.
