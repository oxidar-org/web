+++
date = '2026-04-19T12:00:00-03:00'
draft = true
hiddenFromHomePage = false
title = '¡Lo logramos! El Hackathon Snakear fue un éxito'
description = "Crónica del Distributed Snake Challenge: más de 40 rustáceos se juntaron en Buenos Aires para hackear, competir, y poner a prueba un servidor que no cayó ni una sola vez."
tags = ["rust", "hackathon", "juegos", "comunidad", "eventos"]
categories = ["Eventos", "Comunidad", "Hackathons"]
translationKey = "snakear-recap"
+++

<img src="/images/posts/snakear-recap/grupo.jpg" alt="La comunidad Oxidar reunida en el Hackathon Snakear" style="width:100%; margin: 20px auto; display: block;">

El 11 de abril, más de **40 rustáceos** nos encontramos en Torres Catalinas, en el corazón de Retiro, para vivir una jornada que todavía nos genera sonrisas. Con 113 registrados, el **Distributed Snake Challenge** se convirtió en el evento más grande de Oxidar.org hasta el momento — 30 presenciales, 10 conectados en línea, y cero panics en producción.

## El desafío: tu serpiente contra el mundo

La premisa era simple y despiadada: conectarse a nuestro servidor compartido y construir el cliente de Snake más competitivo posible usando Rust. El tablero era el mismo para todos. Los ticks, el estado global, y la latencia eran el enemigo.

La libertad era total — Bevy, SDL2, Ratatui, o una terminal cruda. Lo que importaba era cómo tu serpiente sobrevivía en un entorno donde todos querían comer la misma manzana.

<img src="/images/posts/snakear-recap/juego-accion.jpg" alt="El tablero compartido en acción durante el hackathon" style="width:100%; margin: 20px auto; display: block;">

## El caos (controlado) que no esperábamos

Lo mejor del evento no fue lo que planeamos — fue lo que la gente inventó sobre la marcha.

Los participantes no solo compitieron: **intentaron hackear el servidor**. Mandaron requests malformados, buscaron exploits en el protocolo, probaron condiciones de borde que nosotros ni habíamos imaginado. El ambiente competitivo derivó naturalmente en algo mucho más interesante: una red de adversarios creativos tratando de romper las reglas del sistema.

<img src="/images/posts/snakear-recap/hackeando.jpg" alt="Participantes en pleno modo hackeo" style="width:100%; margin: 20px auto; display: block;">

Nosotros, del otro lado, nos encontramos **mejorando el servidor en tiempo real** para responder a sus ataques. Un loop de ataque y defensa que mantuvo al equipo de Oxidar corriendo todo el día. El resultado: el servidor aguantó todo. No hubo downtime. Ni uno solo.

<img src="/images/posts/snakear-recap/juego-accion.jpg" alt="El Snake game con el leaderboard en pantalla" style="width:100%; margin: 20px auto; display: block;">

## Los ganadores

### 🧠 Quiz de Rust

<!-- TODO: completar con nombre del ganador del quiz -->
El quiz de Rust del mediodía tuvo su propio campeón: **Gaby**, que demostró que el *Book* no alcanza — hay que haber sufrido el borrow checker de verdad.

<img src="/images/posts/snakear-recap/quiz.jpg" alt="Los ganadores del Quiz de Oxidar" style="width:100%; margin: 20px auto; display: block;">

### 🏆 Hackathon

<!-- TODO: completar con nombre/equipo ganador del hackathon -->
**ClaudIA** se llevó el primer puesto del hackathon con una implementación que se destacó por analizar la estrategia de los demás competidoes y usarlo a su favor.

<img src="/images/posts/snakear-recap/ganadores-hackathon.jpg" alt="Los ganadores del hackathon con los premios de Input Output" style="width:100%; margin: 20px auto; display: block;">

<img src="/images/posts/snakear-recap/premios.jpg" alt="Premios entregados por TxPipe e Input Output Global" style="width:100%; margin: 20px auto; display: block;">

<img src="/images/posts/snakear-recap/remera.jpg" alt="Una de las remeras Oxidar.org que se llevaron los ganadores" style="width:100%; margin: 20px auto; display: block;">

## El equipo que lo hizo posible

Nada de esto hubiera pasado sin el esfuerzo de las personas detrás de Oxidar.org, y el apoyo fundamental de nuestros sponsors.

<img src="/images/posts/snakear-recap/equipo-oxidar.jpg" alt="El equipo de Oxidar.org" style="width:100%; margin: 20px auto; display: block;">

<img src="/images/posts/snakear-recap/hernan.jpg" alt="Hernan de Oxidar.org durante el evento" style="width:100%; margin: 20px auto; display: block;">

<img src="/images/posts/snakear-recap/organizadores.jpg" alt="Los organizadores presentando el desafío" style="width:100%; margin: 20px auto; display: block;">

Gracias a **TxPipe** e **Input Output Global** por los premios, el espacio, y creer en la comunidad Rust de Latinoamérica. Sin su apoyo esto no existiría.

<img src="/images/posts/snakear-recap/presentacion.jpg" alt="Presentación del hackathon ante los participantes" style="width:100%; margin: 20px auto; display: block;">

## Lo que nos quedó

Más allá de los ganadores y el código, lo que nos llevamos es esto: una comunidad que crece, que aprende junta, y que se divierte rompiendo cosas en Rust.

Fue el evento más ambicioso que organizamos, y salió bien. Eso nos da energía para seguir.

Distruta de todas las [fotos](https://iog.pixieset.com/iog/) del evento, gracias a nuestros hosts!

---

**¿Estuviste ahí? Contanos tu experiencia en nuestro [Telegram](https://t.me/+7PgAQVPclxIzOGQ0) o escribinos a [admin@oxidar.org](mailto:admin@oxidar.org).**

**¡Hasta el próximo hackathon!** 🦀
