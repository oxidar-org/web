+++
date = '2025-07-09T14:30:00-03:00'
draft = false
hiddenFromHomePage = false
title = 'Tips para Rust en entornos empresariales'
description = "Consejos prácticos y estrategias para adoptar Rust en empresas."
tags = ["rust", "comunidad", "adopcion", "colaboracion"]
categories = ["Eventos"]
+++

# Rust en la industria: Correctitud, Adopción y Comunidad

El pasado 3 de abril se llevó a cabo un nuevo encuentro de la comunidad de Rust en el que **Alejandro Leiton**, desarrollador de software en **VAIRIX** y entusiasta de Rust, compartió una visión actualizada del estado del ecosistema, con foco en la herramienta, su adopción en la industria y la comunidad que lo impulsa.

---

## Presentación

En esta presentación, Alejandro Leiton nos da consejos prácticos y estrategias para adoptar Rust en empresas. Exploramos casos, cómo entrenar equipos en el lenguaje y el estado actual de la comunidad de Rust.

{{< youtube Bj-Ka26CSFk >}}

---


## Descargar las slides

[**📋 Descargar slides de la presentación (PDF)**](slides.pdf)

Las slides incluyen:
- Tooling existente en Rust.
- Adopción en empresas como Google y Microsoft.
- Adopción en proyectos de software libre como Linux y Ubuntu.
- Información sobre comunidades existentes.

---

## Ecosistema y Herramientas

Rust cuenta con un ecosistema robusto y herramientas de primera clase. En el corazón del mismo se encuentra [crates.io](https://crates.io), el registro oficial de paquetes de Rust, que funciona como el equivalente a `npm` (JavaScript) o `pip` (Python). Respaldado oficialmente por la [Rust Foundation](https://foundation.rust-lang.org/), crates.io ofrece:

- Infraestructura escalable y segura.
- Monitoreo de seguridad de paquetes.
- Coordinación con otros actores del ecosistema.

Entre los crates más relevantes para aplicaciones empresariales se encuentran:

- [`tokio`](https://crates.io/crates/tokio): desarrollo asincrónico, impulsado por la Rust Foundation.
- [`axum`](https://crates.io/crates/axum): framework web moderno.
- [`mongodb`](https://crates.io/crates/mongodb): driver oficial para MongoDB.
- [`aws-sdk-s3`](https://crates.io/crates/aws-sdk-s3): SDK oficial de Amazon para servicios en la nube.
- [`pingora`](https://github.com/cloudflare/pingora): gateway API de Cloudflare, desarrollado en Rust.

## Adopción Empresarial

### Google

Google ha adoptado Rust como lenguaje de primera clase para Android y Chromium. Un dato clave: en pruebas A/B internas, se observó que el código Rust es tan productivo como Go y el doble que C++, además de tener:

- Menor uso de memoria.
- Menor tasa de errores.
- Alta confianza en la corrección del código (“If it compiles, it works”).

Un **85%** de los desarrolladores encuestados en Google afirmaron sentirse más seguros de la corrección de su código en Rust. En menos de **4 meses**, alcanzan niveles de productividad similares a los de su lenguaje anterior.

> Google también donó **USD 1 millón** a la Rust Foundation para trabajar en puentes con C++.
> Fuente: [The Register](https://www.theregister.com/2024/02/05/google_rust_donation)

### Microsoft

Microsoft también ha invertido fuertemente en Rust:

- **USD 10 millones** en herramientas.
- **USD 1 millón** en donaciones a la Rust Foundation.

Identificaron que **el 70% de sus vulnerabilidades** en la última década fueron errores de memoria. Como respuesta, comenzaron a reescribir partes críticas de Windows con Rust:

- **DirectWrite Core**: migrado por 2 devs en 6 meses (154K líneas de código).
- **Win32K GDI Region**: reimplementado en 3 meses.

También usan Rust en servicios de Azure como:

- **Caliptra**: root of trust en hardware.
- **Hyper-V**, **OpenVMM**, **HiperLight**: tecnologías de virtualización.
- **Azure Data Explorer** y chips HSM internos.

> Fuente: [Microsoft Open Source Blog](https://opensource.microsoft.com/blog/2025/02/11/hyperlight-creating-a-0-0009-second-micro-vm-execution-time/)

### Linux y Ubuntu

Rust avanza en el kernel de Linux desde 2020, y algunas distribuciones lo adoptan como opción oficial:

- **Ubuntu 25.10** planea reemplazar `coreutils` de GNU por herramientas escritas en Rust.

> Fuente: [The Register](https://www.theregister.com/2025/03/19/ubuntu_2510_rust/)

### Otras empresas

- **Amazon (AWS)**: usa Rust en [Firecracker](https://firecracker-microvm.github.io/) y Bottlerocket.
- **Meta (Facebook)**: servicios de backend y criptografía.
- **Cloudflare & Discord**: sistemas de baja latencia y alta concurrencia.
- **Figma**: partes del backend fueron reescritas en Rust para mejorar el rendimiento en tiempo real.

> [Why Discord is switching from Go to Rust](https://discord.com/blog/why-discord-is-switching-from-go-to-rust)

> [Rust in production at Figma](https://www.figma.com/blog/rust-in-production-at-figma/)

## Comunidad

La comunidad de Rust es uno de los pilares del lenguaje. Hay múltiples espacios de participación, tanto virtuales como presenciales:

### Conferencias

- [RustWeek](https://rustweek.org/)
- [RustConf](https://rustconf.com/)
- [EuroRust](https://eurorust.eu/)
- [RustNation UK](https://www.rustnationuk.com/)

### Comunidad Online

- [Foro oficial](https://users.rust-lang.org/)
- [Subreddit r/rust](https://www.reddit.com/r/rust/)
- [Canal de soporte en Zulip](https://rust-lang.zulipchat.com/)
- [Discord de la comunidad](https://discord.gg/rust-lang-community)



