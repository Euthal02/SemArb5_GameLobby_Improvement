---
layout: default
title: 2.1 About
parent: 2. Einleitung
nav_order: 201
---

# 2.1 Um was geht es in dieser Semesterarbeit?

![Question](../ressources/icons/question.png){: style="width: 250px" }

[Quelle Bild - Icons](../anhang/600-quellen.html#64-icons)

Die Aufgabe für die Semesterarbeiten ist, ein kleines Projekt von ungefähr 50 Stunden umzusetzen.

Für die diesjährige Arbeit, wurde von Marco Kälin ein Projekt ausgewählt, welches es ermöglichen soll ein einfaches Pong Game mit mehreren "Rooms" zu versehen. Diese Rooms sind als in sich geschlossenes Spiel zu verstehen.

Falls das Spiel "Pong" dem Leser nicht bekannt ist, folgt hier eine kleine Zusammenfassung:

[Quelle Text - ChatGPT](../anhang/600-quellen.html#621-chat-gpt)

```text
"Pong" ist ein klassisches Videospiel, das 1972 von Atari veröffentlicht wurde und als eines der ersten kommerziellen Videospiele gilt. Es simuliert Tischtennis (oder Pingpong) und wird von zwei Spielern gespielt, die jeweils einen Schläger (Paddle) steuern. Die Schläger bewegen sich vertikal am linken und rechten Rand des Bildschirms, während der Ball hin und her fliegt.

Grundlegende Spielmechanik:

    Ziel des Spiels ist es, den Ball so zu schlagen, dass der Gegner ihn nicht zurückspielen kann.
    Jeder Spieler steuert einen Schläger, um den Ball abzuwehren.
    Wenn der Ball an einem Spieler vorbeigeht und den Rand des Bildschirms erreicht, bekommt der gegnerische Spieler einen Punkt.
    Das Spiel geht weiter, bis ein Spieler eine bestimmte Punktzahl erreicht oder die Spieler abbrechen.

Steuerung und Spielfeld:

    Die Steuerung beschränkt sich meist auf das Hoch- und Runterbewegen der Schläger.
    Das Spielfeld ist einfach und besteht aus einem rechteckigen Bereich mit einer Mittellinie und zwei vertikalen Wänden, die den Ball abprallen lassen.

Einfluss und Bedeutung:

    Pong gilt als eine Pionierleistung in der Videospielindustrie und ist ein Beispiel für minimalistische und zugängliche Spielmechanik.
    Trotz seiner Einfachheit ist Pong ein Klassiker und wird oft als Referenzprojekt genutzt, um grundlegende Programmierkenntnisse im Bereich Spieleentwicklung zu erlernen.

Dieses Spielprinzip ist relativ einfach, was es ideal für eine Umsetzung in Python und den Einsatz auf einem Webserver macht.
```

Die Idee dieser Arbeit, ist es nun dieses Spiel mit einer Lobby zu versehen. Dass heisst, dass mehrere Spieler sich an einem zentralen Server / Webseite versammeln können. Von diesem zentralen Sammelpunkt, sollen sich die Spieler auf einzelne Räume aufteilen können. Dies sollte mittels einer internen Weiterleitung geschehen, damit möglichst kein Spieler dies mitbekommt.

Die Aufteilung übernimmt die Lobby selbst, die Spieler sollen aber auch effektiv mit einem anderen Wunschspieler spielen können. Das ganze soll als SaaS Service aufgebaut werden, mit einem Hosting auf Kubernetes (Anforderung an die Semesterarbeit.)

Als Inspiration dienten vorallem die folgenden GitHub Projekte:

* <https://github.com/malletgaetan/transcendence>
* <https://github.com/rhuss/ping-pong/tree/1-java>
* <https://codepen.io/bbbe/pen/MWzoJQr>

[Mehr zu dem Thema Ziele findet man im Kapitel 2.2](./202-ziele.html)
