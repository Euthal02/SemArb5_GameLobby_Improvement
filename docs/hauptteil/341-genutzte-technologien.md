---
layout: default
title: 3.8.1 Genutzte Technologien
parent: 3.8 GameLobby
grandparent: 3. Hauptteil
nav_order: 341
---

# 3.8.1 Genutzte Technologien

Ähnlich wie für den GameRoom, werden dieselben Technologien verwendet.

Es wird verzichtet nochmals die ganze Funktionsweise zu erläutern und stattdessen nur auf die Unterschiede fokussiert. Für mehr Informationen zur Funktionsweise, kann nochmals die GameRoom Dokumentation verwendet werden.

[GameRoom Technologien](./321-genutzte-technologien.html)

## Kommunikation zwischen der Lobby und den Rooms

Der wichtigste Unterschied zu den Rooms ist der Fakt, dass die Lobby mit mehreren Rooms kommuniziert. Um dies zu erreichen, wird die iFrame Funktionalität genutzt, mit den Sources zu kommunizieren.

Hier zum Beispiel wird von der Lobby eine Aufforderung an den "GameFrame" also das iFrame welches das Spiel enthält um die Scores aller Spieler zurückzugeben.

```javascript
gameFrame.contentWindow.postMessage({ action: 'fetch_scores'}, "*");
```

Im Gameroom wird dieser Aufruf empfangen und mit der entsprechenden Antwort zurückgesendet.

```javascript
window.addEventListener('message', (event) => {
    if (event.data.action === 'fetch_scores' && gameState) {
        scores = gameState.scores
        parent.postMessage({ action: "updateScore", scores }, '*');
    };
};
```

Somit können also Daten zwischen diesen beiden Containern gesendet werden.
