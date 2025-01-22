---
layout: default
title: 3.2 AWS Informationen
parent: 3. Hauptteil
nav_order: 302
---

# 3.2 AWS Informationen

Das Projekt / die Arbeit ist auf der AWS Cloud gehostet.
Dies beinhaltet einige Eigenheiten dieser Cloud, welche hier augelistet und erklärt werden.

![AWS Logo](../ressources/images/aws/aws_logo.png){: style="width: 250px" }

[Quelle Bild - AWS Logo](../anhang/600-quellen.html#614-aws-logo)

## EMail Alias

Da zu erwarten ist, dass dieses Projekt nach Abschluss des Semesters 24/25 nicht mehr von Marco Kälin unterhalten wird, wurde von ihm ein Alias aufgesetzt, welcher nach dieser Arbeit wieder gelöscht wird. Dies bedeutet auch, dass der AWS Account hinter diesem Alias nicht mehr wiederherstellbar sein wird.

Zukünftige Entwickler müssen also diesen Account migrieren, sollte dies notwendig sein.

![Email Alias](../ressources/images/aws/email_alias.PNG){: style="width: 350px" }

## Billing Alerts

Um den AWS Account zu erstellen, wurde die Kreditkarte von Marco Kälin genutzt. Auch diese wird nach Abschluss dieses Semesters wieder entfernt, damit keine fälschliche Nutzung damit gemacht werden kann.

In der Zwischenzeit, wurde als Kostenabsicherung ein Billing Alert eingerichtet, womit Marco Kälin immer einen Überblick über die laufenden Kosten hat. Der Alert triggert sich selbst, sollte ein Datapoint (zb. EC2 als Service) mehr als 5 USD über 6 Stunden kosten.

![Billing Alert](../ressources/images/aws/billing_alert.PNG){: style="width: 500px" }

Zusätzlich wurde ein Free Tier Alert aktiviert, sollte das Projekt in einem anderen BEreich aus dem Free Tier Bereich kommen, währe Marco Kälin also informiert und könnte Gegenmassnahmen ergreifen.

![Free Tier Alert](../ressources/images/aws/free_tier_alerts.PNG){: style="width: 500px" }

## IAM User

Da Marco Kälin dieses Projekt initiert hat, ist er momentan der einzige mit einem Zugang auf den Root-Account. Für die Entwickler, welche später dazu stossen könnten, wurde die Admin Gruppe erstellt. Sie erlaubt alles in der AWS Konsole, somit kann jeder Entwickler, mit einem Account jegliche Changes unternehmen. Sollte dieses Projekt grösser werden und die Organisation der Entwicklung kann nicht mehr auf Vertrauen basieren, wird dies geändert.

![Admin Gruppe](../ressources/images/aws/admin_gruppe.PNG){: style="width: 500px" }
