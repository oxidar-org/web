+++
date = '2025-06-12T20:00:00-03:00'
draft = false
hiddenFromHomePage = false
title = 'Rust + WebAssembly en acción - Presentación completa'
description = "Revive la presentación del 12 de junio sobre nuestro proyecto colaborativo que combina Rust, JavaScript y WebAssembly"
tags = ["rust", "webassembly", "wasm", "javascript", "wasm-pack", "presentacion", "video"]
categories = ["Proyectos", "Eventos"]
+++

## 🎬 ¡Presentación completada con éxito!

El pasado **12 de junio** presentamos con gran éxito nuestro proyecto colaborativo en el meetup "Junio de WebAssembly!" de **Rust Argentina**. Fue una exploración práctica del poder de **Rust** combinado con **WebAssembly (WASM)** que superó todas nuestras expectativas.

---

## 📹 Revive la presentación completa

{{< youtube lH2Fnd7ryKY >}}

---

## 🚀 Lo que presentamos

**Tomás Kenda** presentó "Rust y WebAssembly", donde exploramos en detalle cómo compilar Rust a WASM, casos de uso reales, y por qué esta tecnología está cambiando la forma en que desarrollamos tanto en frontend como en backend.

Además, se presentó oficialmente **Oxidar**, un grupo latinoamericano para la divulgación y colaboración en Rust, recibiendo una excelente acogida por parte de la comunidad.

### 🛠️ Stack tecnológico presentado
- **Rust** - El corazón de la lógica computacional
- **WebAssembly** - El puente hacia el navegador
- **JavaScript** - La interfaz con el DOM
- **wasm-pack** - La herramienta que hace la magia posible

---

## 📊 Descargar las slides

[**📋 Descargar slides de la presentación (PDF)**](slides.pdf)

Las slides incluyen:
- Introducción completa a WebAssembly
- Ejemplos prácticos de código Rust compilado a WASM
- Comparativas de performance
- Casos de uso reales y recomendaciones
- Demos en vivo del proyecto **oxidar-wasm**

---

## 🌟 ¿Por qué Rust + WebAssembly funciona tan bien?

Durante la presentación demostramos las ventajas técnicas clave:

### Performance demostrada
- **Velocidad**: Hasta 10x más rápido que JavaScript en operaciones intensivas
- **Memory Safety**: Las garantías de seguridad de Rust se mantienen en WASM
- **Tamaño optimizado**: Binarios compactos ideales para la web
- **Interoperabilidad**: Integración fluida demostrada en vivo

### Casos de uso que exploramos
- **Procesamiento de imágenes** en tiempo real
- **Algoritmos computacionalmente intensivos**
- **Juegos web** de alta performance
- **Aplicaciones científicas** ejecutándose en el navegador

---

## 🔧 La arquitectura del proyecto demostrada

```
oxidar-wasm/
├── rust/               # Código fuente en Rust
├── js/                 # Proyecto JavaScript
│   └── src/
│       └── wasm/       # Paquete generado por wasm-pack
└── build.sh            # Script de compilación
```

Durante la demo en vivo mostramos el flujo completo:
1. **Escribimos lógica** en Rust con ejemplos prácticos
2. **Compilamos a WASM** con `wasm-pack` en tiempo real
3. **Integramos con JavaScript** mostrando la interoperabilidad
4. **Ejecutamos en el navegador** con mediciones de performance

---

## 🎓 Lo que aprendimos juntos

### Insights para desarrolladores Rust
- Patrones efectivos de compilación de Rust a WebAssembly
- Técnicas de interoperabilidad con JavaScript
- Estrategias de optimización de binarios WASM
- Herramientas de debugging para aplicaciones híbridas

### Revelaciones para desarrolladores web
- Cuándo WebAssembly supera claramente a JavaScript
- Gestión eficiente de memoria entre Rust y JS
- Integración práctica en aplicaciones existentes
- Tooling moderno que simplifica el desarrollo

### Para toda la comunidad
- **Colaboración en acción** en proyectos open source
- **Workflows productivos** con tecnologías híbridas
- **Best practices** validadas en proyectos reales

---

## 🤝 El impacto en la comunidad

La presentación generó un gran interés y participación:

- **+50 asistentes** presenciales y online
- **Preguntas técnicas profundas** durante la sesión de Q&A
- **Múltiples propuestas** de colaboración en el proyecto
- **Networking activo** entre desarrolladores Rust y web

### Feedback destacado de los asistentes:
- *"Finalmente entiendo cuándo usar WASM vs JavaScript"*
- *"La demo en vivo fue increíble, se veía la diferencia de performance"*
- *"Oxidar tiene un enfoque muy práctico y colaborativo"*
- *"Las slides están muy bien estructuradas para aprender"*

---

## 🛠️ Recursos para continuar aprendiendo

Si quieres explorar el código presentado:

### Acceso al proyecto
```bash
# Clonar el proyecto completo
git clone https://github.com/oxidar-org/oxidar-wasm.git
cd oxidar-wasm

# Seguir las instrucciones del README
```

### Requisitos técnicos (como se mostró en la demo)
```bash
# Verificar instalación
rustc --version
wasm-pack --version
node -v && npm -v
```

---

## 🔮 Próximos pasos del proyecto

Basándose en el feedback recibido, el proyecto **oxidar-wasm** continuará evolucionando:

### Desarrollos planificados
- **Benchmarks extendidos** comparando diferentes escenarios
- **Tutoriales paso a paso** en español
- **Casos de uso avanzados** como criptografía y ML
- **Optimizaciones de performance** específicas

### Oportunidades de colaboración
- **Contribuciones al código** en GitHub
- **Documentación** y ejemplos
- **Testing** en diferentes navegadores y dispositivos
- **Nuevos casos de uso** propuestos por la comunidad

---

## 🌍 Oxidar: Construyendo comunidad

La presentación marcó oficialmente el lanzamiento de **Oxidar** como espacio de colaboración para desarrolladores Rust en Latinoamérica. Los objetivos que compartimos:

- **Contenido en español** accesible y de calidad
- **Proyectos colaborativos** como oxidar-wasm
- **Eventos y workshops** regulares
- **Mentoría** para nuevos desarrolladores Rust

---

## 📈 Métricas de la presentación

### Alcance del evento
- **Asistentes presenciales**: 35 personas
- **Participantes online**: 20+ conexiones simultáneas
- **Visualizaciones del video**: Creciendo diariamente
- **Descargas de slides**: +100 en las primeras 48hs

### Engagement de la comunidad
- **GitHub stars** del proyecto: +50 nuevas
- **Forks activos**: 12 desarrolladores explorando el código
- **Issues abiertas**: Ideas y mejoras propuestas
- **Miembros nuevos** en Telegram: +30

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

**Oxidar-wasm** es solo el un proyecto de muchos que vendrán. La comunidad ha respondido con entusiasmo y estamos emocionados por lo que construiremos juntos.

---

## 📢 Mantente conectado

### Únete a la comunidad Oxidar:
- **Telegram**: [Oxidar Community](https://t.me/+7PgAQVPclxIzOGQ0)
- **GitHub**: [oxidar-org](https://github.com/oxidar-org)

---

*¿Te perdiste la presentación en vivo? No hay problema. El video completo está disponible arriba, las slides se pueden descargar, y el código está abierto para explorar. ¡La comunidad Rust en Latinoamérica está creciendo!*
