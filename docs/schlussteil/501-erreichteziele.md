---
layout: default
title: 5.1 Erreichte Ziele
parent: 5. Schlussteil
nav_order: 501
---

# 5.1 Erreichte Ziele

Ich habe mir vor Beginn dieser Arbeit einige Ziele gesetzt. Wie sieht es nun mit diesen aus?

![Erreichte Ziele](../ressources/icons/achievement.png){: style="width: 250px" }

[Quelle Bild - Icons](../anhang/600-quellen.html#64-icons)

## Vergleich

Ich erläutere zu jedem Ziel inwiefern dies erreicht wurde oder nicht.

### 1. Die Game Lobby funktioniert Browser basiert

100% erreicht.

Dies funktioniert wie erwartet. Die Lobby kann mit jedem Browser geöffnet werden, die technische Implementation wurde mit dem Mauszeiger gemacht. Das heisst, wenn sich der Mauszeiger des Spielers bewegt, bewegt sich auch das "Paddle". Diese Variante sollte mit jeglichen Brwoser verfügbar sein und wurde auch so getestet.

### 2. Die Game Lobby und der Game Room werden automatisiert von einer CI/CD Pipeline deployt

100% erreicht.

Sobald ein neuer Commit auf dem Main Branch stattfindet, werden die beiden Pipelines für die GameLobby und den GameRoom deployed. Jedoch muss dafür ein Change innerhalb den Unterordnern `gameroom/` oder `gamelobby/` gemacht werden. Das bedeutet also, das Features auf einem eigenständigen Branch entwickelt werden können und sobald der Branch gemerged wird, wird die entsprechende Pipeline ausgeführt.

### 3. Neue Versionen werden automatisch getestet

100% erreicht.

Das Testing ist in der Pipeline erledigt. Zugegebenermassen ist das Testing ziemlich einfach erledigt und basiert auf einem internen Health Check. Da die beiden Programme / Container jedoch einen kleinen Umfang haben, erachte ich dies als ausreichend.

### 4. Das ganze soll auf Kubernetes gehostet werden. (Grundanforderung der Semesterarbeit)

100% erreicht.

Die Container werden auf EKS gehostet, was die Kubernetes Version von AWS ist. Aws übernimmt dabei das Management des Clusters und man bekommt dabei die bessere Cloud Redundanz von AWS, statt wenn man das ganze selbst hosten würde.

### 5. Die Lobby skaliert automatisch anhand der Anzahl Spieler und erstellt neue "Rooms"

Nicht erreicht.

Aufgrund von Zeitrestriktionen, habe ich dieses Ziel nicht bis zum Ende verfolgt. Es wurde einige Zeit darin investiert, jedoch konnte ich keine gute Endlösung erreichen und habe daher das ganze sein lassen.

### 6. Bereits vorhandene "Pong" Spiele für die Rooms einsetzen

Nicht erreicht.

Leider waren die Projekte, welche mich zu diesem Projekt inspiriert haben, nicht wirklich kompatibel mit meiner Vision. Der Aufwand, welcher notwendig gewesen wäre um diese Projekte zu migrieren, wäre noch grösser gewesen, anstatt das ganze selbst zu schreiben. Daher habe ich den Entschluss gefasst, das ganze selbst zu schreiben.
