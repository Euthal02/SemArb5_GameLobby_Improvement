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
bash eks/delete.sh
```

Alle Ressourcen welche irgendwie mit diesem Cluster verbunden sind, werden somit gelöscht.

Dafür reicht es aus, den Cluster selbst zu löschen und alle selbst erstellten Policies:

````bash
eksctl delete cluster --name eks-cluster
ALB_POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`AWSLoadBalancerControllerIAMPolicy`].Arn' --output text)
DNS_POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`AllowExternalDNSUpdatesPolicy`].Arn' --output text)
CERT_MANAGER_POLICY_ARN=$(aws iam list-policies --query 'Policies[?PolicyName==`cert-manager-acme-dns01-route53`].Arn' --output text)
aws iam delete-policy --policy-arn=$ALB_POLICY_ARN
aws iam delete-policy --policy-arn=$DNS_POLICY_ARN
aws iam delete-policy --policy-arn=$CERT_MANAGER_POLICY_ARN
```
