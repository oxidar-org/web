+++
date = '2026-05-27T00:00:00-03:00'
draft = true
hiddenFromHomePage = false
title = 'RustWeek 2026: lo que nos trajimos de Utrecht'
description = "Crónica de RustWeek 2026 en Utrecht: más de 900 asistentes, 50 charlas, workshops y el Rust All-Hands."
tags = ["rust", "comunidad", "conferencia", "eventos"]
categories = ["Eventos", "Comunidad"]
translationKey = "rust-week-2026"
+++

La semana pasada viajamos a **Utrecht, Países Bajos**, para asistir a **RustWeek 2026**, y volver a casa con la cabeza llena de ideas y la energía renovada para seguir construyendo con Rust.

![RustWeek 2026 — apertura en el Kinepolis de Utrecht](/images/rustweek26-apertura.jpeg)

## Qué es RustWeek

RustWeek 2026 se presentó como **la conferencia de Rust más grande del mundo**, y los números lo respaldan: más de **900 asistentes**, 50 charlas distribuidas en 3 tracks, 8 workshops, un hackathon y el segundo **Rust Project All-Hands**. Todo esto a lo largo de una semana completa (18 al 23 de mayo) en tres sedes distintas de Utrecht.

La elección de Utrecht no es casual. La ciudad está en el corazón de los Países Bajos, con conexiones de tren directas desde el aeropuerto de Ámsterdam, lo que la hace accesible para quienes viajamos desde cualquier rincón del mundo.

## Los días de conferencia

### Martes y miércoles: la conferencia

Los dos días centrales se desarrollaron en el **Kinepolis** con capacidad para 800 asistentes por día. Tres tracks simultáneos significaron que siempre había decisiones difíciles sobre qué sesión priorizar.

Estas son las charlas que más nos marcaron:

---

#### Lessons Learnt from using Rust as the Intro to Programming

Una de las más refrescantes del evento. La charla exploró la experiencia de enseñar Rust como **primer lenguaje de programación** — algo que suena contraintuitivo dado que Rust tiene fama de difícil. La conclusión fue interesante: el compilador, que suele frustrarnos a los adultos que venimos de otros lenguajes, resulta ser un excelente maestro para alguien que aprende desde cero. Los mensajes de error son descriptivos, el sistema de tipos obliga a pensar con precisión, y los "momentos de '¿por qué?' del compilador" se convierten en oportunidades de aprendizaje genuino.

![Why Rust — ponencia sobre enseñanza de Rust como primer lenguaje](/images/rustweek26-why-rust-teaching.jpeg)

> *"I really believe anyone can learn anything. We just need to change the world a little bit. I believe Rust can be part of that."*

![](/images/rustweek26-believe-rust.jpeg)

{{< youtube 8iy37I0WE_s >}}

---

#### Completion-based IO

Una charla técnica profunda sobre el modelo de I/O basado en **completions** (como io_uring en Linux), en contraste con el modelo tradicional basado en readiness que usan los runtimes async de Rust hoy. Alice exploró los desafíos de integrar este modelo con el ecosistema async existente: las diferencias en cómo se manejan los buffers, la cancelación, y por qué la transición no es trivial. Para quienes trabajamos con sistemas donde la performance de I/O importa, fue una de las más relevantes de la semana.

{{< youtube CmLAHUuUsAQ >}}

---

#### Untrusted data in Linux — How Rust is going to save us

**Greg Kroah-Hartman** de la Linux Foundation presentó uno de los keynotes más aplaudidos. El mensaje fue claro: Rust en el kernel Linux no es un experimento — es una necesidad. La charla detalló el trabajo de manejar **datos no confiables** que llegan del userspace, un área donde los bugs de memoria han causado vulnerabilidades críticas históricamente. Rust permite expresar esas invariantes directamente en el sistema de tipos.

![Greg Kroah-Hartman: "We need more Rust Linux developers!"](/images/rustweek26-linux-keynote.jpeg)

También presentó datos concretos del descenso de vulnerabilidades de memoria en proyectos que adoptaron Rust.

![Datos sobre el descenso de vulnerabilidades de memoria](/images/rustweek26-memory-safety.jpeg)

{{< youtube Nzmj7K0FNRY >}}

---

#### Obsessive Optimization with String Interning

**Arya Dradjica** presentó una de las charlas más entretenidas del track de performance. Arrancó con un problema aparentemente simple — strings repetidos que se comparan frecuentemente — y fue construyendo capas de optimización, midiendo a cada paso con benchmarks reales. La metodología fue ejemplar: usar `perf`, analizar accesos a cache L1, medir ciclos por iteración. Una clase magistral de cómo se hace performance engineering en Rust sin adivinar.

![Obsessive Optimization with String Interning — Arya Dradjica](/images/rustweek26-string-interning.jpeg)

{{< youtube SWRL4JpaR2I >}}

---

#### Interop is the New Rewrite: Design Axioms for Rust's Next Frontier

**Taylor Cramer (Google)** cerró con una charla estratégica sobre el futuro de Rust. El argumento central: el próximo gran desafío de Rust no es reescribir sistemas en Rust, sino **interoperar con el mundo existente** — especialmente con C++, que domina las interfaces de bajo nivel (system libraries, ABIs, linkers). Pero C++ no puede expresar ownership, lifetimes ni destructores, lo que crea una brecha semántica al cruzar el boundary.

![The Trouble with C Interop — Taylor Cramer](/images/rustweek26-c-interop.jpeg)

La charla propuso axiomas de diseño concretos para guiar el trabajo futuro en este espacio. Un mapa de ruta para quienes trabajan en FFI o en integración de Rust en proyectos C/C++ existentes.

{{< youtube 1NnCJTVYPA4 >}}

## Qué nos llevamos

Más allá de las charlas y los slides que se van a publicar, lo que más valoramos de este tipo de eventos es la **gente**. Hablar con personas que usan Rust en contextos completamente distintos — sistemas embebidos, kernel, backend web, compiladores — y ver cómo se articulan las mismas herramientas para resolver problemas tan distintos es recordar por qué esta comunidad es especial.

![Estrategias para Rust: "Design holistically. Ship incrementally."](/images/rustweek26-strategies.jpeg)

![Representando a Oxidar en RustWeek 2026](/images/rustweek26-oxidar-tshirt.jpeg)

También es motivador ver cuánto espacio hay para que **comunidades regionales como Oxidar** contribuyan. Rust en Latinoamérica todavía tiene mucho terreno por cubrir, y eventos como RustWeek son un buen lugar para traer esa energía de vuelta a casa.

![Foto grupal al cierre de RustWeek 2026](/images/rustweek26-grupo.jpeg)

Y para terminar, un detalle que resume bien el espíritu de la conferencia: entre los afiches del cine Kinepolis, el equipo de RustWeek colocó sus propias versiones parodiadas de películas clásicas. "Box to the Future - 1.21 Gigabytes", con un DeLorean cuya matrícula decía **ENOMEN**. El humor de la comunidad Rust en su máxima expresión.

![Box to the Future — 1.21 Gigabytes](/images/rustweek26-back-to-future.jpeg)

## Las charlas ya están disponibles

Las grabaciones ya están publicadas en el [canal de YouTube de RustNL](https://www.youtube.com/@RustNL). También podés revisar el programa completo en [2026.rustweek.org](https://2026.rustweek.org).

---

¿Estuviste en RustWeek 2026? ¿Qué charla te pareció la más interesante? Contanos en el [grupo de Telegram](https://t.me/+7PgAQVPclxIzOGQ0) o en nuestro [Discord](https://discord.gg/EMpekX7en). 🦀
