+++
date = '2025-04-03T14:30:00-03:00'
draft = false
hiddenFromHomePage = false
title = 'Rust en AWS Lambda con Cargo Lambda'
description = "Explora nuestro proyecto colaborativo sobre cómo usar Cargo Lambda para desplegar funciones Rust en AWS Lambda de manera eficiente"
tags = ["rust", "aws", "lambda", "cargo-lambda", "serverless", "colaboracion"]
categories = ["Proyectos", "Tutoriales", "Eventos"]
+++

## 🚀 Una nueva colaboración de la comunidad

En **Oxidar** creemos en el poder del aprendizaje colaborativo. Por eso, nos complace compartir uno de nuestros proyectos más recientes: **[oxidar-lambdas](https://github.com/oxidar-org/oxidar-lambdas)**, una exploración práctica sobre cómo desplegar funciones **Rust** en **AWS Lambda** usando **Cargo Lambda**.

---

## 🤔 ¿Qué es Cargo Lambda?

**Cargo Lambda** es una herramienta que simplifica enormemente el desarrollo y despliegue de funciones Lambda escritas en Rust. Sin esta herramienta, tendrías que:

- Configurar manualmente toolchains de cross-compilation
- Manejar el empaquetado de binarios
- Escribir scripts de despliegue personalizados
- Lidiar con las complejidades del runtime de AWS Lambda

Cargo Lambda elimina toda esta fricción y nos permite enfocarnos en escribir código Rust de calidad.

---

## 🎬 Presentación

Presentamos una exposición sobre cómo utilizar Rust en la nube de la mano de AWS y Cargo Lambda en el meetup de **Rust Argentina**.

{{< youtube IfWgf2Z_rSU >}}

---

## 🚀 Lo que presentamos

**Nicolás Antinori** presentó "Creando un Lambda Authorizer en Rust con Cargo lambda", donde exploramos en detalle cómo utilizar Rust para crear funciones de AWS Lambda en un caso de uso real, qué herramientas existen y cómo utlizar Rust nos ayuda a ahorrar recursos, lo cuál se traduce en ahorro de dinero.

### 🛠️ Stack tecnológico presentado
- **Rust** - El lenguaje de programación utilizado.
- **Cargo Lambda** - Herramienta CLI para la creación de funciones AWS Lambda en Rust.
- **Amazon Web Services** - El proveedor cloud utilizado para el proyecto.

---

## 📊 Descargar las slides

[**📋 Descargar slides de la presentación (PDF)**](/slides/cargo-lambda.pdf)

Las slides incluyen:
- Qué es Cargo Lambda
- Comandos básicos de Cargo Lambda
- Performance del Authorizer creado
- Muestras del tracing obtenido con Open Telemetry
- Link al repositorio con el código



## 🛠️ Lo que construimos juntos

Nuestro repositorio **oxidar-lambdas** incluye:

### Estructura del proyecto
- **Múltiples funciones Lambda** en Rust
- **Configuración de DynamoDB** local con Docker
- **Scripts de testing** y despliegue automatizados
- **Manejo de JWT** para autenticación
- **Configuración de tracing** para observabilidad

### Herramientas y tecnologías
- **Rust** como lenguaje principal
- **Cargo Lambda** para build y deploy
- **AWS Lambda** como plataforma serverless
- **DynamoDB** para persistencia
- **Docker** para desarrollo local
- **GitHub** para colaboración

---

## 🎯 Comandos esenciales de Cargo Lambda

### Instalación
```bash
# Con pip (requiere Python 3)
pip3 install cargo-lambda

# Con Homebrew (macOS/Linux)
brew tap cargo-lambda/cargo-lambda
brew install cargo-lambda

# Con Scoop (Windows)
scoop bucket add cargo-lambda
scoop install cargo-lambda/cargo-lambda
```

### Desarrollo local
```bash
# Crear un nuevo proyecto Lambda
cargo lambda new mi-funcion

# Build para producción
cargo lambda build --release

# Build para ARM64 (Graviton2)
cargo lambda build --release --arm64

# Servidor local para testing
cargo lambda watch
```

### Testing y despliegue
```bash
# Invocar función localmente
cargo lambda invoke --data-example apigw-request

# Invocar con datos personalizados
cargo lambda invoke --data-file ./data.json

# Desplegar a AWS
cargo lambda deploy mi-funcion
```

---

## 💡 ¿Por qué Rust en Lambda?

### Ventajas de usar Rust
- **Performance**: Cold starts rápidos y ejecución eficiente
- **Memory safety**: Sin preocupaciones por memory leaks
- **Concurrencia**: Manejo excelente de operaciones asíncronas
- **Ecosistema**: Crates robustos para AWS y desarrollo web

### Casos de uso ideales
- **APIs de alta performance**
- **Procesamiento de datos en tiempo real**
- **Microservicios con baja latencia**
- **Funciones de transformación de datos**

---

## 🤝 El poder de la colaboración

Este proyecto fue posible gracias a la colaboración de varios miembros de **Oxidar**:

- **[@nicoan](https://github.com/nicoan)** - Nicolás Antinori
- **[@aleiton](https://github.com/aleiton)** - Alejandro Leiton

Juntos exploramos diferentes aspectos:
- Configuración de entornos de desarrollo
- Patrones de manejo de errores en Lambda
- Integración con servicios de AWS
- Optimización de cold starts
- Testing de funciones serverless

---

## 🎓 Aprendizajes clave

### 1. Simplificación del workflow
Cargo Lambda reduce significativamente la curva de aprendizaje para desarrollar en Lambda con Rust.

### 2. Desarrollo local eficiente
El comando `cargo lambda watch` permite un ciclo de desarrollo rápido y cómodo.

### 3. Compatibilidad con el ecosistema AWS
La integración con herramientas como AWS SAM y CDK es fluida.

### 4. Performance excepcional
Las funciones Rust en Lambda ofrecen excelente rendimiento y eficiencia de memoria.

---

## 📚 Recursos adicionales

- **[Repositorio del proyecto](https://github.com/oxidar-org/oxidar-lambdas)**
- **[Documentación oficial de Cargo Lambda](https://www.cargo-lambda.info/)**
- **[AWS Lambda Rust Runtime](https://github.com/awslabs/aws-lambda-rust-runtime)**
- **[Guía de AWS sobre Rust en Lambda](https://docs.aws.amazon.com/lambda/latest/dg/rust-package.html)**

---

## 🔮 Próximos pasos

Como comunidad, continuamos explorando:

- **Integración con otros servicios de AWS**
- **Patterns de arquitectura serverless**
- **Optimización de costos en Lambda**
- **Monitoring y observabilidad avanzada**

---

## 🙌 ¡Únete a nosotros!

¿Te interesa contribuir a proyectos como este? ¡La comunidad **Oxidar** siempre está abierta a nuevos colaboradores!

### Formas de participar:
- **Explora el código** en nuestro repositorio
- **Propón mejoras** a través de issues y PRs
- **Comparte tu experiencia** con Rust y serverless
- **Únete a nuestras discusiones** en [Telegram](https://t.me/+7PgAQVPclxIzOGQ0)

---

## 📝 Conclusión

**oxidar-lambdas** es más que un proyecto técnico; es un ejemplo de cómo el conocimiento compartido y la colaboración pueden acelerar el aprendizaje de toda una comunidad.

Rust y serverless computing son tecnologías que están transformando cómo construimos aplicaciones modernas. Con herramientas como **Cargo Lambda**, esa transformación está al alcance de cualquier desarrollador dispuesto a experimentar.

¿Tienes experiencia con Rust en Lambda? ¿Preguntas sobre serverless? ¡Nos encantaría escuchar tu perspectiva!

---

**¡Gracias por hacer crecer la comunidad Rust en Latinoamérica! 🦀**

*Para más proyectos y colaboraciones, visita nuestro [GitHub](https://github.com/oxidar-org) y únete a nuestra [comunidad](https://t.me/+7PgAQVPclxIzOGQ0).*
