+++
date = '2025-08-06T08:30:58-03:00'
draft = true
title = 'Snakear 🦀🐍'
+++

## ¡El hackathon de Oxidar, La Viborita!

Empecemos a construir nuestra serpiente.

## Endpoints

| Endpoint           | Channel  | Description          |
| ------------------ | -------- | -------------------- |
| `/login`           | TCP      | Conectarse al juego. |
| `/move`            | UDP      | Conectarse al juego. |
| `/board`           | UDP      | Socket de estado del juego. |

### /login
Deberás enviar un mensaje HTTP:POST usando un nombre de usuario, con el que te identificarás en el juego. Aquí obtendras un token de sesión que te permitirá interactuar con el resto de los endpoints. Si el nombre de usuario ya existe, resiviras siempre el mismo token.

Requerimientos:
- El nombre de usuario debe tener entre 3 y 20 caracteres.
- El nombre de usuario debe contener solo letras y números.

*Request*
```
{
    "username": "string"
}
```

*Response*
```
{
    "token": "string"
}
```

*Example*
```
curl -X POST -H "Content-Type: application/json" -d '{"username": "user123"}' http://localhost:8080/login
```

## /move
Socket UDP bidireccional para actulizar tu posición y recibir la comida si llegas primero.

Requerimientos:
- Debes estar autenticado con un token válido.

*Request*
```
{
    "token": "string"
}
```

Puedes enviar mensajes del tipo `Move` para actualizar tu posición, y recibirás mensajes del tipo `Grow` si llegas primero.

## /board
Socket UDP unidireccional para obtener el estado del juego

Una vez conectado a nuestro _status socket_ vas a recibir un stream de datos binarios que representan el estado del juego para vos y todos los jugadores.

Los mensajes son del tipo `Board` que contiene información sobre el tablero y los jugadores.

## Data Types

### Board
| Content            | Type                 | Description          |
| ------------------ | -------------------- | -------------------- |
| ID                 | MessageID            | Identificador del tipo de mensaje. |
| Food               | Cell                 | Posición del alimento en el tablero. |
| Snakes             | [Snake; u8]          | Lista de serpientes y su posición en el tablero. |

### Snake
| Content            | Type                 | Description          |
| ------------------ | -------------------- | -------------------- |
| name               | [u8; 16]             | Nombre del jugador. (ASCII) |
| body               | [Cell; u8]           | Posiciones de la serpiente. |

### Cell
| Content            | Type                 | Description          |
| ------------------ | -------------------- | -------------------- |
| x                  | u8                   | Posición en el eje X. |
| y                  | u8                   | Posición en el eje Y. |

### MessageID
| ID             | Value  | Description |
| -------------- | ------ | ----------- |
| Move           | 0x10   | Movimiento  de un jugador |
| Grow           | 0x11   | Llegaste primero a la comida, tu snake crece 1 unidad. |
| Board          | 0x12   | Estado del tablero. |
