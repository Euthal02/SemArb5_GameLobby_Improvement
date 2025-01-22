---
layout: default
title: 3.5 K8S Plugins
has_children: true
parent: 3. Hauptteil
nav_order: 305
---

# 3.5 K8S Plugins

![Plugins](../ressources/icons/plugin.png){: style="width: 250px"" }

[Quelle Bild - Icons](../anhang/600-quellen.html#64-icons)

Da der K8S Cluster auf AWS gehostet ist, kann man mittels Plugins, auf viele Ressourcen vpn AWS direkt zugreifen und diese bearbeiten.
Dies eröffnet uns neue Möglichkeiten, zb. eine öffentliche IP mit DNS Eintrag, welcher sich dynamisch ändert. Z.B. im Falle eines Upscaling / Downscaling eines Deployment.

Momentan haben wir zwei Use-Cases, bei welchen es mehr Sinn macht, dass ganze via AWS Ressourcen zu erledigen.

* LoadBalancing wird mit dem AWS Load Balancer gemacht. Der Vorteil dabei ist, da die Nodes bei EKS auch dynamisch skalierbar sind, kann mittels diesem LoadBalancer ganz einfach auf die einzelnen Nodes verteilt werden. Die Nodes registrieren sich in einem Service Endpunkt und werden vom ALB angesprochen.
* ExternalDNS wird genutzt um jedem Pod / Service einen Hostnamen zuzuweisen, mit öffentlicher IP, sodass der Code statsich auf den Domainnamen geschrieben werden kann, dann aber mittels dem AWS Tool dynamisch gewechselt werden kann.
* Cert Manager, in Theorie sollte dieses Plugin genutzt werden, um für jeden Ingress automatisch ein Zertifikat zu erstellen. Jedoch funktioniert dies nicht so richtig. Mehr Infos dazu im Unterartikel.

Sollten in der Zukunft noch mehr Plugins hinzukommen, werden diese hier beschrieben.
