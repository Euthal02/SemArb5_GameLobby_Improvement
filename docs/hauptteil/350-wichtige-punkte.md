---
layout: default
title: 3.9 Wichtige Punkte
parent: 3. Hauptteil
nav_order: 350
---

# 3.9 Wichtige Punkte

![Wichtige Informationen](../ressources/icons/exchange.png){: width="250px" }

[Quelle Bild - Icons](./600-quellen.html#64-icons)

## Datenbank

In dieser Implementation wurde keine Datenbank Integration verwendet. Dies bedeutet also, dass die Spielerdaten nicht resistent gegenüber Shutdown / Reboots sind. Dieses Feature würde in einem zweiten Schritt weitergeführt, passte aber leider nicht in das 50 Stunden Limit dieser Arbeit.

## Sicherheitsaspekte

In dieser Arbeit wurden nebst dem Helm Deployment nur einen kleinen Fokus auf die Sicherheit gelegt. So sind zum Beispiel die Secret Keys der Flask Applikationen undefiniert oder besser gesagt als `secret!` definiert.

```python
def setup_game():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
```

Sollte diese Applikation weiterentwickelt werden, müssen diese Secrets In GitHub Secrets umgewandelt werden und mit Environment Variablen gearbeitet werden.
