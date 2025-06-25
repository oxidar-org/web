+++
date = '2025-06-24T14:30:00-03:00'
draft = false
hiddenFromHomePage = false
title = 'Rust en AWS Lambda con Cargo Lambda - Presentacion completa'
description = "Revive la presentacion del 3 de Abril sobre cómo usar Cargo Lambda para desplegar funciones Rust en AWS Lambda de manera eficiente"
tags = ["rust", "aws", "lambda", "cargo-lambda", "serverless", "colaboracion", "video"]
categories = ["Proyectos", "Eventos"]
+++

## 🎬 Presentación

El pasado **3 de abril** presentamos una exposición sobre cómo utilizar Rust en la nube de la mano de AWS y Cargo Lambda en el meetup de **Rust Argentina**.

---

## 📹 Revive la presentación completa

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

[**📋 Descargar slides de la presentación (PDF)**](slides.pdf)

Las slides incluyen:
- Qué es Cargo Lambda
- Comandos básicos de Cargo Lambda
- Performance del Authorizer creado
- Muestras del tracing obtenido con Open Telemetry
- Link al repositorio con el código

---

## 🌟 ¿Por qué Rust + AWS Lambdas funciona tan bien?

Durante la presentación demostramos las ventajas técnicas clave:

### Performance demostrada
- **Velocidad**: En el perceltil 99 la velocidad de respuesta es de 21ms con warm start
- **Memoria**: 25 MB de uso de memoria constante
- **Procesamiento**: 40 ms de uso de CPU

### Casos de uso que exploramos
- **Autenticación de endpoints REST con JWT** en tiempo real
- **Modificación de permisos**
- **Exploración de métricas precisas** de la mano de OpenTelemetry

---

## 🎓 Lo que aprendimos juntos

### Insights para desarrolladores Rust
- Tooling para el desarrollo de AWS Lambdas con Rust
- Cómo organizar un proyecto con varios AWS Lambda relacionados

### Revelaciones para desarrolladores web
- Cómo y por qué utilizar Rust para aplicaciones serverless
- Pérformance y ahorro de recursos frente a otras alternativas más conocidas
- Integración práctica en aplicaciones existentes
- Tooling moderno que simplifica el desarrollo

---

## 🤝 El impacto en la comunidad

La presentación generó un gran interés y participación:

- **+55 asistentes** presenciales y online
- **Preguntas técnicas** durante la sesión de Q&A
- **Networking activo** entre desarrolladores Rust y web

---

## 🛠️ Recursos para continuar aprendiendo

Si quieres explorar el código presentado:

### Acceso al proyecto
```bash
# Clonar el proyecto completo
git@github.com:oxidar-org/oxidar-lambdas.git
cd oxidar-lambdas

# Seguir las instrucciones del README
```

---

## 📈 Métricas de la presentación

### Alcance del evento
- **Asistentes presenciales**: 40 personas
- **Participantes online**: 15+ conexiones simultáneas
- **Visualizaciones del video**: Creciendo diariamente

---

## 🎉 Agradecimientos

### A la comunidad Rust Argentina
Gracias por el espacio, la organización impecable y la cálida recepción de **Oxidar**.

### A LambdaClass
Por hospedar el evento y proporcionar un ambiente perfecto para el aprendizaje colaborativo.

### A todos los asistentes
Sus preguntas, comentarios y entusiasmo hicieron de esta presentación una experiencia memorable.

---

## 🦀 El futuro es colaborativo

Esta presentación demostró que cuando combinamos **curiosidad técnica**, **colaboración comunitaria** y **código de calidad**, podemos explorar las fronteras de la tecnología de manera efectiva.

---

## 📢 Mantente conectado

### Únete a la comunidad Oxidar:
- **Telegram**: [Oxidar Community](https://t.me/+7PgAQVPclxIzOGQ0)
- **GitHub**: [oxidar-org](https://github.com/oxidar-org)

---

*¿Te perdiste la presentación en vivo? No hay problema. El video completo está disponible arriba, las slides se pueden descargar, y el código está abierto para explorar. ¡La comunidad Rust en Latinoamérica está creciendo!*
