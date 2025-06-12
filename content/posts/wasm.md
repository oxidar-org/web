+++
date = '2025-06-11T15:00:00-03:00'
draft = false
hiddenFromHomePage = false
title = 'Rust + WebAssembly en acción'
description = "El 12 de junio a las 18hs presentamos nuestro nuevo proyecto colaborativo que combina Rust, JavaScript y WebAssembly"
tags = ["rust", "webassembly", "wasm", "javascript", "wasm-pack", "presentacion"]
categories = ["Proyectos", "Eventos"]
+++

## 🎯 ¡El 12 de junio es el gran día!

**Rust Argentina** nos invita a participar de su meetup "Junio de WebAssembly!" donde presentaremos una exploración práctica del poder de **Rust** combinado con **WebAssembly (WASM)**.

---

## 🚀 ¿Qué se va a presentar?

**Tomás Kenda** presentará "Rust y WebAssembly", donde descubriremos cómo compilar Rust a WASM, los casos de uso reales, y por qué esta tecnología está cambiando la forma en que desarrollamos tanto en frontend como en backend.

Además, se presentará oficialmente **Oxidar**, un grupo latinoamericano para la divulgación y colaboración en Rust.

### 🛠️ Stack tecnológico
- **Rust** - El corazón de la lógica computacional
- **WebAssembly** - El puente hacia el navegador
- **JavaScript** - La interfaz con el DOM
- **wasm-pack** - La herramienta que hace la magia posible

---

## 🌟 ¿Por qué Rust + WebAssembly?

### Ventajas técnicas
- **Performance**: Velocidad cercana al código nativo
- **Memory Safety**: Las garantías de seguridad de Rust
- **Tamaño optimizado**: Binarios compactos para la web
- **Interoperabilidad**: Integración fluida con JavaScript

### Casos de uso perfectos
- **Procesamiento de imágenes** en tiempo real
- **Algoritmos computacionalmente intensivos**
- **Juegos web** de alta performance
- **Aplicaciones científicas** en el navegador

---

## 🔧 La arquitectura del proyecto

```
oxidar-wasm/
├── rust/               # Código fuente en Rust
├── js/                 # Proyecto JavaScript
│   └── src/
│       └── wasm/       # Paquete generado por wasm-pack
└── build.sh            # Script de compilación
```

El flujo es elegante y directo:
1. **Escribimos lógica** en Rust
2. **Compilamos a WASM** con `wasm-pack`
3. **Integramos con JavaScript** en el frontend
4. **Ejecutamos en el navegador** con performance nativa

---

## 🎓 Lo que aprenderemos juntos

### Para desarrolladores Rust
- Cómo compilar código Rust a WebAssembly
- Patrones de interoperabilidad con JavaScript
- Optimización de binarios WASM
- Debugging de aplicaciones híbridas

### Para desarrolladores web
- Integración de WebAssembly en aplicaciones JavaScript
- Cuándo usar WASM vs JavaScript puro
- Gestión de memoria entre Rust y JS
- Tooling moderno para WASM

### Para toda la comunidad
- **Colaboración práctica** en proyectos open source
- **Workflows de desarrollo** con tecnologías híbridas
- **Best practices** para proyectos Rust+WASM

---

## 🛠️ Preparación para la presentación

Si quieres seguir la presentación y probar el código, asegurate de tener:

### Requisitos básicos
```bash
# Rust
rustc --version

# wasm-pack
wasm-pack --version

# Node.js y npm
node -v && npm -v
```

### Instalación rápida
```bash
# Instalar Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Instalar wasm-pack
curl https://rustwasm.github.io/wasm-pack/installer/init.sh -sSf | sh

# Clonar el proyecto
git clone https://github.com/oxidar-org/oxidar-wasm.git
cd oxidar-wasm
```

---

## 🤝 El espíritu colaborativo

Este proyecto nació de la curiosidad colectiva de la comunidad **Oxidar** por explorar las fronteras entre **Rust** y el **desarrollo web**. Es un ejemplo perfecto de cómo el aprendizaje colaborativo acelera el crecimiento de todos.

### Áreas de exploración
- **Performance benchmarking** Rust vs JavaScript
- **Patterns de arquitectura** para aplicaciones híbridas
- **Tooling y workflows** de desarrollo
- **Casos de uso prácticos** en el mundo real

---

## 📅 Detalles del evento

**¿Cuándo?** Jueves 12 de junio a las 18:30hs (GMT-3)
**¿Dónde?** LambdaClass, A. Carranza 1441, Buenos Aires, Argentina
**¿Online?** También puedes unirte por [Google Meet](https://meet.google.com/vsd-rnqn-tyn)
**¿Qué necesitas?** Solo ganas de aprender y experimentar

*Organizado por [Rust Argentina](https://www.meetup.com/rust-argentina/events/307990465/) con bebidas, snacks y muy buena onda.*

---

## 💫 Más allá de la presentación

Esta presentación es solo el comienzo. Como comunidad, continuaremos:

- **Expandiendo el proyecto** con nuevas funcionalidades
- **Documentando patrones** y best practices
- **Creando tutoriales** paso a paso
- **Explorando casos de uso** más complejos

---

## 🔮 El futuro de Rust en la web

WebAssembly está transformando lo que es posible en el navegador, y **Rust** está en el centro de esta revolución. Proyectos como **oxidar-wasm** nos permiten:

- **Experimentar** con tecnologías emergentes
- **Compartir conocimiento** en español
- **Construir comunidad** alrededor de la innovación
- **Prepararnos** para el futuro del desarrollo web

---

## 🎉 ¡Únete a nosotros!

¿Te emociona el futuro de Rust en la web? ¿Quieres ser parte de esta exploración?

### Formas de participar:
- **Únete** a la presentación el 12 de junio a las 18hs
- **Explora** el código en [GitHub](https://github.com/oxidar-org/oxidar-wasm)
- **Comparte** tus ideas y experimentos
- **Colabora** en futuras iteraciones del proyecto

### **[📅 Regístrate en Meetup](https://www.meetup.com/rust-argentina/events/307990465/)** para confirmar tu asistencia

---

## 🦀 Construyendo el futuro juntos

En **Oxidar** creemos que las mejores ideas surgen cuando combinamos **curiosidad**, **colaboración** y **código**. El proyecto **oxidar-wasm** es una muestra perfecta de lo que podemos lograr cuando exploramos juntos las fronteras de la tecnología.

_No dejes de sumarte a Oxidar a nuestro canal de Telegram: [Telegram](https://t.me/+7PgAQVPclxIzOGQ0)._

**¡Nos vemos el 12 de junio a las 18:30hs para este emocionante evento de Rust Argentina!**

---

*¿Preguntas sobre WebAssembly? ¡Únete al evento de [Rust Argentina](https://www.meetup.com/rust-argentina/events/307990465/) y participa de la discusión!*

**🦀 Oxidar - Explorando el futuro de Rust en Latinoamérica**
