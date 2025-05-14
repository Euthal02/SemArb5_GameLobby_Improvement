---
layout: default
title: 3.4.1 External DNS
parent: 3.4 K8S Plugins
grandparent: 3. Hauptteil
nav_order: 305
---

# 3.4.1 External DNS

Zu Beginn der Arbeit wurden einige Probleme mit der DNS Auflösung festgestellt. Der DNS Eintrag in die Zone wurde gemacht, aber man konnte die Domain nicht auflösen.

```bash
mka@Tuxedo-Laptop:~$ nslookup lobby.semesterarbeit.com
;; Got SERVFAIL reply from 172.30.128.1
Server:         172.30.128.1
Address:        172.30.128.1#53

** server can't find lobby.semesterarbeit.com: SERVFAIL                                                                                      mka@Tuxedo-Laptop:~$    
```
