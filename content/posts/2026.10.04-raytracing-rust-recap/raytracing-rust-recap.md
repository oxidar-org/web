+++
date = '2026-10-04T10:00:00-03:00'
draft = true
hiddenFromHomePage = false
title = 'Un ray tracer en Tandil: así fue la charla en UNICEN'
description = "Gonzalo Dicosimo reescribió un ray tracer de C++ a Rust: ownership, borrowing, smart pointers, SIMD y benchmarks de las dos implementaciones."
tags = ["rust", "presentacion", "comunidad", "cpp"]
categories = ["Eventos", "Comunidad"]
translationKey = "raytracing-rust-recap"
+++

Estuvimos en la **UNICEN de Tandil** presentando esta charla: **De C++ a Rust: reescribiendo un Ray Tracer**. Gonzalo Dicosimo tomó un ray tracer que ya funcionaba, escrito en C++, y lo reescribió entero en Rust. La charla recorre ese camino: qué se traduce derecho, qué no, y qué se aprende en el intento.

{{< youtube 4HSapIeFD6o >}}

## Descargar las slides

![Un momento de la charla en el auditorio de la UNICEN](/images/posts/raytracing-rust-recap/presentacion-pantalla.jpg)

[**Descargar slides de la presentación (PDF)**](/slides/raytracing-rust.pdf)

Las slides incluyen:
- Cómo funciona un path tracer: el rayo, el viewport, el pixel grid, el antialiasing y la *Bounding Volume Hierarchy*
- Por qué Rust y no C++, comparados punto por punto en rendimiento, portabilidad, estándar, seguridad, toolchain y memoria
- El mismo código en los dos lenguajes, lado a lado: estructuras, colecciones, *new types*, polimorfismo y mutabilidad
- Los benchmarks completos sobre una Cornell box, con el perfil de release, SIMD y Rayon
- Y el cierre, que da vuelta la premisa: *¿me conviene aprender Rust?*

![El auditorio de la UNICEN durante la charla](/images/posts/raytracing-rust-recap/apertura-agenda.jpg)

El auditorio se llenó mayormente de estudiantes de la facultad. Gracias a **José M. Massa** y a la **UNICEN**, que incorporaron la charla como actividad de libre elección (ALE) y nos prestaron el auditorio, y a **Gonzalo Dicosimo**, por compartir el proyecto y la experiencia de reescribirlo. La charla se sumó además a la difusión del **FLISOL**.

## Conectá con la comunidad

![La presentación de la comunidad Oxidar ante el público, con los enlaces para sumarse](/images/posts/raytracing-rust-recap/publico-oxidar.jpg)

¿Te interesó la charla o querés seguir aprendiendo sobre Rust? ¡La comunidad **Oxidar** siempre está abierta a nuevos colaboradores!

### Formas de participar:
- **Sumate a las discusiones** en [Telegram](https://t.me/+7PgAQVPclxIzOGQ0) o en nuestro [Discord](https://discord.gg/EMpekX7en)
- **Explorá los proyectos** en nuestro [GitHub](https://github.com/oxidar-org)
- **Seguí nuestros eventos** en el [calendario público de Oxidar](https://calendar.google.com/calendar/embed?src=c_ac1102f85b1a406dd0a442876323f149a9c72aa29381a26e2af2c82cabc28661%40group.calendar.google.com&ctz=America%2FArgentina%2FBuenos_Aires) — *nuestras charlas son abiertas, siempre podés sumarte*
- **¿Querés que la próxima sea en tu facultad o en tu ciudad?** Escribinos a [admin@oxidar.org](mailto:admin@oxidar.org) 🦀
