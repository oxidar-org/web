+++
date = '2026-07-31T10:00:00-03:00'
draft = false
hiddenFromHomePage = false
title = '(Por qué|Quién|Dónde) Rust en DebConf 26'
description = "Una charla sobre por qué Rust es bueno para el desarrollo de sistemas, quién lo usa en producción y cómo sumarse a la comunidad."
tags = ["rust", "presentacion", "comunidad", "seguridad"]
categories = ["Eventos"]
translationKey = "rust-in-open-source"
+++

Estuvimos en **DebConf 26** presentando esta charla: **(Por qué|Quién|Dónde) Rust**. Durante décadas, la programación de sistemas de bajo nivel ha significado elegir entre seguridad y rendimiento. A medida que estos sistemas se vuelven más complejos, el impacto de los errores de memoria y los problemas de concurrencia no para de crecer. Esta charla analiza por qué Rust es bueno para el desarrollo de sistemas.

{{< youtube HYNE8HG4AFA >}}

## Descargar las slides

[**Descargar slides de la presentación (PDF)**](/slides/405-por-quequiendonde-rust.pdf)

Las slides incluyen:
- Por qué Rust está ganando terreno frente a C/C++
- Cómo el borrow checker y el sistema de tipos previenen errores
- Quiénes usan Rust en producción
- Cómo sumarse a la comunidad Rust

## Por qué Rust está ganando terreno

![Repasando ejemplos de código y los fallos clásicos de C/C++](/images/debconf26-por-que-rust.jpeg)

**Nicolás Antinori** comienza con las razones por las cuales Rust está ganando terreno. Al examinar los fallos comunes de C/C++ (invalidación de iteradores, comportamiento indefinido, falta de seguridad de hilos), muestra cómo el borrow checker y el sistema de tipos de Rust detectan categorías enteras de errores en tiempo de compilación. También veremos cómo Rust podría haber evitado fallos del mundo real como **Heartbleed**.

## Quién lo está usando realmente

![Datos de adopción de Rust en Google presentados durante la charla](/images/debconf26-quien-usa-rust.jpeg)

**Hernán G. Gonzalez** continúa con quién lo está usando realmente. Rust ya está en el **kernel de Linux**, y organizaciones como **Google, Microsoft y Canonical** lo utilizan en producción. Estos no son experimentos: demuestran que el lenguaje está listo para el tipo de infraestructura que mantenemos todos los días.

## Cómo involucrarse

![Nicolás Antinori y Hernán G. Gonzalez durante la charla en DebConf 26](/images/debconf26-charla-apertura.jpeg)

Finalmente, hablamos sobre cómo involucrarse. La comunidad de Rust es activa y acogedora, y compartimos recursos para encontrar soporte, contribuir a proyectos de Rust de código abierto y conectar con otros Rustaceans.

## Conectate con la comunidad

¿Te interesa la charla o querés seguir aprendiendo sobre Rust? La comunidad **Oxidar** siempre está abierta a nuevos colaboradores.

### Formas de participar:
- **Únete a nuestras discusiones** en [Telegram](https://t.me/+7PgAQVPclxIzOGQ0)
- **Explora los proyectos** en nuestro [GitHub](https://github.com/oxidar-org)
- **Seguí nuestros eventos** en el [calendario público de Oxidar](https://calendar.google.com/calendar/embed?src=c_ac1102f85b1a406dd0a442876323f149a9c72aa29381a26e2af2c82cabc28661%40group.calendar.google.com&ctz=America%2FArgentina%2FBuenos_Aires) - *Nuestras charlas son abiertas, son siempre bienvenidos a participar!*
