+++
date = '2025-10-08T20:00:00-03:00'
draft = false
hiddenFromHomePage = false
title = 'Async/Await a fondo'
description = 'Una guía práctica para entender qué hace el compilador de Rust cuando usamos async/await, y cómo escribir un runtime asincrónico desde cero.'
tags = ["rust", "async", "await", "concurrencia", "runtimes", "presentacion", "video"]
categories = ["Proyectos", "Eventos"]
+++

# Async a fondo: Cómo funciona async/await en Rust desde cero

El pasado 08 de octubre de 2025 se llevó a cabo un nuevo encuentro de la comunidad de Rust, donde Jorge Prendes, presentó qué hace realmente `async fn`, cómo se implementa el trait `Future`, y cómo un runtime como Tokio ejecuta nuestras tareas concurrentes.

---

## Presentación

En esta presentación, Jorge Prendes nos va mostrando cómo se construye un async runtime desde cero, deteniéndose y explicando cada detalle para que podamos entender a fondo qué sucede cuando ejecutamos funciones asincrónas.

{{< youtube fbM_IP0VFiA >}}

---

## Descargar las slides

[**📋 Descargar slides de la presentación (PDF)**](/slides/async-await.pdf)

Las slides incluyen:

- Por qué construir un async runtime desde cero.
- Explicación de cómo es la anatomia de una función async.
- Explicación del trait `Future` y los wakers.
- Qué hacen los runtimes profesionales.

---

## De `fn` a `async fn`

A primera vista, usar `async fn` parece mágico: marcamos una función con `async`, agregamos `.await` y el código “funciona”.
Sin embargo, un `async fn` no devuelve el valor directamente, sino una estructura que implementa el trait [`Future`](https://doc.rust-lang.org/std/future/trait.Future.html).

El compilador transforma automáticamente la función en un tipo anónimo que implementa `Future`, con un método `poll` que controla su avance.
Esto significa que *`async fn` es azúcar sintáctica para una máquina de estados que el compilador genera automáticamente.*
Cada punto de suspensión (`await`) se convierte internamente en una transición de estado dentro de esa máquina.

---

## El trait `Future`

El corazón del modelo asincrónico de Rust es el trait `Future`, que define cómo una tarea avanza hacia su resultado final.
Su método `poll` devuelve:
- `Poll::Ready(val)` cuando el futuro ha completado su trabajo, o
- `Poll::Pending` si todavía no puede continuar y necesita ser reintentado más adelante.

Cada `Future` debe garantizar que, si devuelve `Pending`, notificará al *runtime* cuando esté listo para avanzar.
Esa notificación se realiza mediante un objeto `Waker` que forma parte del contexto (`Context`) de ejecución.

En términos conceptuales, un `Future` es un proceso cooperativo: no se ejecuta por sí mismo, sino que el runtime lo invoca repetidamente hasta que devuelve un valor final.

---

## Construyendo un runtime mínimo

Rust no ejecuta funciones `async fn` automáticamente: requiere un *runtime* que gestione la ejecución de los futuros.
Un runtime es, esencialmente, un *scheduler* que mantiene una cola de tareas y llama a `poll` sobre cada una cuando hay progreso disponible.

Un runtime básico puede implementarse en pocas líneas: un bucle que invoca `poll`, y que espera eventos externos (por ejemplo, mediante un canal o un selector del sistema operativo).
Cuando un `Future` devuelve `Pending`, el runtime suspende su ejecución y se bloquea hasta que algún `Waker` lo despierte.

De esta forma, se logra concurrencia sin necesidad de hilos múltiples, aprovechando un único hilo cooperativo que gestiona múltiples tareas de manera eficiente.

---

## El papel del `Waker`

El `Waker` es el mecanismo mediante el cual los futuros notifican al runtime que están listos para continuar.
Cuando un `Future` devuelve `Poll::Pending`, registra un `Waker` para que, cuando haya nuevo trabajo disponible, pueda invocar `wake_by_ref` y alertar al runtime.

Runtimes como Tokio, Smol o Embassy implementan este concepto con diferentes estrategias:
- **Tokio** utiliza mecanismos del sistema operativo como `epoll` o `kqueue` para gestionar miles de operaciones I/O en un solo hilo.
- **Smol** emplea un *thread pool* ligero que aprovecha primitivas de la biblioteca estándar.
- **Embassy** está diseñado para entornos sin sistema operativo (bare metal), y usa un *Hardware Abstraction Layer (HAL)* para interactuar directamente con el hardware.

En todos los casos, el principio es el mismo: el `Waker` conecta los futuros con el scheduler que los controla.

---

## Demo interactiva

Puedes explorar una implementación práctica del modelo explicado en Rust Playground:

- [Versión básica](https://play.rust-lang.org/?version=stable&mode=debug&edition=2024&gist=b51f63e714ab80cf109a443bfcbc9c46)
- [Versión avanzada](https://play.rust-lang.org/?version=stable&mode=debug&edition=2024&gist=c244fef8ad8aa124058234f63c7d096e)

La versión básica ejecuta tareas secuenciales, mientras que la avanzada crea múltiples futuros que se ejecutan en paralelo sobre el mismo runtime.

---

## Conclusiones

- Un `async fn` es una transformación sintáctica que genera una máquina de estados que implementa `Future`.
- Los runtimes asincrónicos como Tokio o Smol son *schedulers* que ejecutan y reactivan futuros basados en eventos del sistema.
- Implementar un runtime simple ayuda a comprender los fundamentos del modelo asincrónico de Rust.
- Comprender `poll`, `Context` y `Waker` permite escribir código más eficiente, predecible y compatible con runtimes existentes.

Detrás de `async/await` no hay magia: solo **transformaciones deterministas y un modelo explícito de concurrencia**.
Entender estos conceptos es clave para dominar la programación asincrónica en Rust.

---

## Referencias

- [Documentación oficial de `Future`](https://doc.rust-lang.org/std/future/trait.Future.html)
- [Tutorial oficial de Tokio](https://tokio.rs/tokio/tutorial/async#)
- [Smol runtime](https://github.com/smol-rs/smol)
- [Embassy para entornos embebidos](https://github.com/embassy-rs/embassy)
- [Proyecto Hyperlight](https://github.com/hyperlight-dev/hyperlight)

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
