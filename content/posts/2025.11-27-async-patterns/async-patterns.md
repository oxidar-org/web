+++
date = '2025-11-27T20:00:00-03:00'
draft = false
hiddenFromHomePage = false
title = 'Async Rust: Compartiendo Memoria'
description = 'Cómo manejar memoria compartida en Async Rust, comparando distintos enfoques y resaltando la importancia de elegir el modelo adecuado según las necesidades de concurrencia y paralelismo'
tags = ["rust", "async", "await", "concurrencia", "runtimes", "presentacion", "video"]
categories = ["Proyectos", "Eventos"]
+++

# Async Rust: Compartiendo Memoria

El pasado 27 de noviembre de 2025, Gabriel Steinberg presentó una charla titulada *Async Rust: compartiendo memoria*, donde exploró distintos métodos para manejar estado mutable compartido en aplicaciones asincrónicas en Rust.


## Presentación

En esta presentación Gabriel Steinberg explica cómo manejar memoria compartida en Async Rust, comparando distintos enfoques y resaltando la importancia de elegir el modelo adecuado según las necesidades de concurrencia y paralelismo.

{{< youtube FEBSepG0Lr4 >}}

---

## Descargar las slides

[**📋 Descargar slides de la presentación (PDF)**](/slides/async-patterns.pdf)

Las slides incluyen:
- Ejemplos de servidores TCP en Rust.
- Problemas comunes con el borrow checker en contextos async.
- Uso de `Mutex`, `Arc`, y canales para sincronización.
- Modelos alternativos de concurrencia y paralelismo.

---

## De implementación ingenua a sincronización

Al intentar implementar un servidor TCP asincrónico con Tokio, surge rápidamente un problema: el borrow mutable de `self` escapa del ciclo de aceptación de conexiones. Esto ocurre porque `tokio::spawn` requiere futuros `'static`, lo que rompe las reglas del borrow checker.

**Conclusión inicial:** necesitamos mecanismos de sincronización para compartir estado mutable.

### Mutex

Una primera solución es usar `tokio::sync::Mutex`. Esto permite mantener un `HashMap` de conexiones y bloquearlo mientras se realizan operaciones `await`. Sin embargo, este enfoque puede llevar a problemas de rendimiento.

### Canales

Una alternativa más robusta es usar **canales (`mpsc`)** para comunicar tareas. En este modelo:
- Cada conexión se maneja con un `OwnedWriteHalf`.
- Los mensajes se envían a un *dispatcher central* que decide cómo distribuirlos.
- Se pueden agregar mecanismos de backpressure y manejo de errores.

Este enfoque evita bloqueos y permite mayor control sobre el flujo de mensajes. Pero tiene como tradeoff la complejidad de manejar cada interacción entre tareas, es dificil de debuggear, y el manejo de errores se torna poco natural.

### Un solo task

Finalmente, se mostró un modelo simplificado: manejar todas las conexiones en un **único task** que corre una carrera de futuros (`race`). Este diseño sacrifica paralelismo pero ofrece:
- Acceso directo y seguro a estado mutable.
- Flujo natural de errores.
- Facilidad para trazar el origen de valores.

---

## Conclusiones

- **Trade-offs:** Mutex vs Canales vs Race/Select.
- **Evaluar paralelismo:** no siempre es necesario, y puede complicar el diseño.
- **Canales:** recomendados cuando se necesita paralelismo.
- **Mutex:** útil en casos muy específicos.

---

## Referencias

- [Comparing patterns for mutable state in concurrent applications (post en el que se basa la charla)](https://taping-memory.dev/concurrency-patterns/)
- [Let futures be futures](https://without.boats/blog/let-futures-be-futures/)
- [Tree-Structured Concurrency](https://blog.yoshuawuyts.com/tree-structured-concurrency/)
- [Tree-Structured Concurrency II: Replacing Background Tasks With Actors](https://blog.yoshuawuyts.com/replacing-tasks-with-actors/)
- [sans-IO: The secret to effective Rust for network services](https://www.firezone.dev/blog/sans-io)

---

## Comunidad

La comunidad de Rust es uno de los pilares del lenguaje. Hay múltiples espacios de participación, tanto virtuales como presenciales:

### Conferencias

- [RustWeek](https://rustweek.org/)
- [RustConf](https://rustconf.com/)
- [EuroRust](https://eurorust.eu/)
- [RustNation UK](https://www.rustnationuk.com/)

### Comunidad Online

- [Rust en español - Telegram](https://t.me/rust_lang_es)
- [Foro oficial](https://users.rust-lang.org/)
- [Subreddit r/rust](https://www.reddit.com/r/rust/)
- [Canal de soporte en Zulip](https://rust-lang.zulipchat.com/)
- [Discord de la comunidad](https://discord.gg/rust-lang-community)
