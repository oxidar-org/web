+++
date = '2025-08-21T20:00:00-03:00'
draft = false
hiddenFromHomePage = false
title = 'gRPC en Rust'
description = "Revive la presentación del 21 de agosto sobre cómo utilizar gRPC en Rust"
tags = ["rust", "grpc", "protobuf", "protocol-buffers", "tonic", "prost", "presentacion", "video"]
categories = ["Proyectos", "Eventos"]
+++

# gRPC en Rust: Protocol Buffers y Framework de Alto Rendimiento
El pasado 21 de agosto de 2025 se llevó a cabo un nuevo encuentro de la comunidad de Rust, donde Alejandro Gonzalez, presentó una introducción práctica a gRPC en Rust. Alejandro, compartió conocimientos sobre Protocol Buffers y gRPC, enfocándose en su implementación en Rust para entornos de alto rendimiento.

---

## Presentación
En esta presentación, Alejandro Gonzalez nos guía a través de Protocol Buffers y gRPC en Rust. Exploramos qué son, sus ventajas, comparaciones, herramientas como Protoc, Prost y Tonic, ejemplos prácticos y casos de uso en la industria, incluyendo una demo de una aplicación de chat. La charla enfatiza cómo estas tecnologías permiten comunicaciones eficientes y seguras en sistemas distribuidos, aprovechando las fortalezas de Rust en seguridad y rendimiento.


{{< youtube AcZiZasZQbY >}}

---

## Descargar las slides

[**📋 Descargar slides de la presentación (PDF)**](./slides.pdf)

Las slides incluyen:

- Agenda detallada.
- Explicación de Protocol Buffers: qué es, por qué usarlo, comparaciones y herramientas.
- Detalles sobre gRPC: pros, cons, implementación en Rust y ejemplos.
- Casos de uso en microservicios, IoT y más.
- Recursos y herramientas adicionales.

---

## Protocol Buffers
Protocol Buffers, disponible en https://protobuf.dev, es un formato para el intercambio de datos que es agnóstico al lenguaje y a la plataforma, con un esquema fuertemente tipado. Desarrollado por Google, Protocol Buffers es un mecanismo neutral en cuanto a lenguaje y plataforma para serializar datos estructurados, diseñado para ser más pequeño, rápido y simple en comparación con formatos como XML o JSON. Permite definir estructuras de datos una vez y generar código fuente para leer y escribir los datos en varios flujos de datos y lenguajes de programación.

### Por qué usarlo

- Compacto (más rápido para transmitir), lo que reduce el tamaño de los payloads y acelera la transmisión.
- Rápido para serializar/deserializar, mejorando el rendimiento en aplicaciones de alto volumen.
- Evolución del esquema: puedes agregar o depreciar campos sin romper clientes o servicios existentes.


### Contras

- No legible por humanos, lo que complica el debugging manual.
- Menos flexible para datos ad-hoc, ya que requiere un esquema fijo.
- Tipos de datos incorporados limitados (ej. sin soporte nativo para fechas/timestamps).

### Codificación / Decodificación

- El nombre del campo no se codifica, lo que ahorra espacio.
- El tipo y número del campo se codifican, utilizando codificación de números de longitud variable para eficiencia.
- El orden de los campos no importa, permitiendo flexibilidad.

Protocol Buffers usa ediciones como "2023" en definiciones proto, con mensajes que definen campos numerados (e.g., string name = 1;).

#### Comparación vs JSON

- Cadenas: ~2.7 veces más rápido.

- Números: ~34 veces más rápido.

#### Decodificación:

- Cadenas: ~23 veces más rápido.
- Números: ~38 veces más rápido.

#### Tamaño de payload:

Entre 30% y 70% más pequeño, lo que lo hace ideal para entornos con restricciones de red.

> En general, Protocol Buffers es más eficiente que JSON en términos de tamaño y velocidad, aunque JSON es más legible por humanos.

## Protoc
Protoc es la herramienta oficial de línea de comandos que transforma archivos .proto en código fuente. Soporta muchos lenguajes de forma nativa, como Python, Ruby, Java, C++ y Rust (a través de plugins). Puede extenderse para soportar nuevos lenguajes vía plugins (ej. Go).

El proceso es muy simple: Ingresa un archivo .proto y genera código para el lenguaje deseado, facilitando la interoperabilidad.

## Rust: Prost
[prost](https://github.com/tokio-rs/prost) es una implementación de Protocol Buffers para Rust. Genera código Rust simple e idiomático a partir de archivos .proto, utilizando abstracciones como `bytes::{Buf, BufMut}` para serialización. Soporta `proto2` y `proto3`, retiene comentarios de .proto, permite serialización de tipos Rust existentes con atributos, y preserva valores enum desconocidos.

Ejemplo: github.com/oxidar-org/rust-proto-sample. Este repo demuestra el uso de prost-build para generar código Rust de .proto, con un ejemplo de encoding/decoding de un struct `User`. Incluye `build.rs` para compilación, y genera código en `my_package.rs`.

Comandos:
- `cargo build` para generar
- `cargo run` para ejecutar el ejemplo, que muestra bytes codificados y decodificados.


## gRPC
[gRPC](https://grpc.io/),es un framework RPC de alto rendimiento y open source. Es un framework moderno para llamadas a procedimientos remotos (RPC) que puede ejecutarse en cualquier entorno, conectando servicios eficientemente con soporte para balanceo de carga, tracing, health checking y autenticación:

- Basado en HTTP/2 para transporte eficiente.
- Usa Protocol Buffers para definiciones de servicios.
- APIs fuertemente tipadas con generación automática de stubs cliente/servidor para múltiples lenguajes.
- Ofrece streaming bidireccional, comunicación asincrónica, autenticación integrada, TLS con rustls, balanceo de carga y health checking.

## Herramientas

- `grpcurl`: Como cURL, pero para gRPC.
- `postman`: Plataforma para testing de APIs (soporta gRPC).
- `Awesome-grpc`: Lista curada de recursos útiles para gRPC.

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
