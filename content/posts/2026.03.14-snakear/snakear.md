+++
date = '2026-03-14T00:00:00-03:00'
draft = false
hiddenFromHomePage = false
title = 'Distributed Snake Challenge: El próximo Hackathon de Oxidar.org'
description = "Hackathon para construir una versión multijugador del clásico Snake, donde el tablero es compartido y la competencia ocurre en tiempo real."
tags = ["rust", "hackathon", "juegos"]
categories = ["Eventos", "Comunidad", "Hackathons"]
translationKey = "snakear"
+++

# Distributed Snake Challenge!: El próximo Hackathon de Oxidar.org

¡Es hora de volver a ensuciarnos las manos con código! Desde la comunidad de **Oxidar.org**, nos emociona anunciar nuestro próximo gran evento: un Hackathon dedicado a la experimentación, el networking y, por supuesto, la potencia de Rust.

En esta edición, el desafío escala a otro nivel. No vamos a construir un simple juego; vamos a enfrentarnos a los problemas reales de los **sistemas distribuidos y la comunicación en tiempo real**.

<a href="https://luma.com/5f51ey45" target="_blank">
    <img src="/images/posts/snakear/snakear.png" alt="Distributed Snake Challenge" style="width:100%; max-width:300px; margin: 20px auto; display: block;">
</a>

## El Desafío: Distributed Snake

El objetivo es simple pero ambicioso: construir una versión multijugador del clásico **Snake**, donde el tablero es compartido y la competencia ocurre en tiempo real.

¿Cuál es el truco? El foco estará en la **perspectiva del cliente**. Deberás implementar la lógica de red necesaria para que tu serpiente sobreviva en un entorno donde la sincronización de ticks y el manejo del estado global son la clave entre el éxito o un *panic!*.

### ¿Qué vas a explorar?
* **Networking en Rust:** Manejo de sockets, protocolos de comunicación y serialización eficiente.
* **Estado Global:** Cómo sincronizar lo que pasa en el servidor con lo que ve el usuario.
* **Libertad Total de Frontend:** ¡La visualización queda a tu criterio! Podés usar:
    * **Bevy** para los amantes de los Game Engines.
    * **SDL2** para algo más clásico.
    * **Ratatui** o una simple terminal si sos un purista del CLI.

## ¿Por qué participar?

Este hackathon no es solo una competencia; es un espacio para poner a prueba tus conocimientos de Rust en un entorno de **concurrencia y sistemas distribuidos**. Es la oportunidad perfecta para ver cómo estructurar un proyecto que debe responder en milisegundos y cómo manejar la comunicación asíncrona de manera segura.

Además, es el lugar ideal para conocer a otros "Rustáceos" de la escena local, intercambiar patrones de diseño y, por qué no, encontrar a tu próximo equipo de desarrollo.

---

### 📋 Detalles del Evento

* **Organiza:** Equipo de [Oxidar.org](https://oxidar.org)
* **Colaboran:** TxPipe e Input Output Global.
* **Requisitos:** Traer tu laptop con el toolchain de Rust instalado y muchas ganas de debugear.
* **Fecha:** 11/04/2026
* **Lugar:** Torres Catalina - Retiro, Buenos Aires

**Inscribite aca** https://luma.com/5f51ey45

> **Nota:** No importa si sos experto en compiladores o si recién terminaste el *Book*; el hackathon está pensado para que todos aprendamos algo nuevo en el proceso.

---

### ¡Inscribite y participá!

No te quedes afuera de esta jornada de pura programación. Vení a compilar código, resolver problemas de red y, por supuesto, a comer algunas **manzanas (virtuales)** con nosotros.

**¡Los esperamos para hacer crecer la comunidad de Rust en Latinoamérica!**
