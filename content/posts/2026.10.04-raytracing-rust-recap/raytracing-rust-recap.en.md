+++
date = '2026-10-04T10:00:00-03:00'
draft = false
hiddenFromHomePage = false
title = "A ray tracer in Tandil: how the talk at UNICEN went"
description = "Gonzalo Dicosimo rewrote a C++ ray tracer in Rust: ownership, borrowing, smart pointers, SIMD, and benchmarks of the two implementations."
tags = ["rust", "presentation", "community", "cpp"]
categories = ["Events", "Community"]
translationKey = "raytracing-rust-recap"
+++
We were at **UNICEN in Tandil** presenting this talk: **From C++ to Rust: Rewriting a Ray Tracer**. Gonzalo Dicosimo took a ray tracer that already worked, written in C++, and rewrote it entirely in Rust. The talk walks through that journey: what translates directly, what doesn't, and what you learn along the way.

{{< youtube 4HSapIeFD6o >}}

## Download the Slides

![A moment from the talk in the UNICEN auditorium](/images/posts/raytracing-rust-recap/presentacion-pantalla.jpg)

[**Download the presentation slides (PDF)**](/slides/raytracing-rust.pdf)

The slides include:
- How a path tracer works: the ray, the viewport, the pixel grid, antialiasing, and the *Bounding Volume Hierarchy*
- Why Rust and not C++, compared point by point on performance, portability, standard, safety, toolchain, and memory
- The same code in both languages, side by side: structs, collections, *new types*, polymorphism, and mutability
- The complete benchmarks on a Cornell box, with the release profile, SIMD, and Rayon
- And the closing, which flips the premise: *should I learn Rust?*

![The UNICEN auditorium during the talk](/images/posts/raytracing-rust-recap/apertura-agenda.jpg)

The auditorium was filled mostly with students from the faculty. Thanks to **José M. Massa** and **UNICEN**, who included the talk as an elective activity (ALE) and lent us the auditorium, and to **Gonzalo Dicosimo**, for sharing the project and the experience of rewriting it. The talk was also part of the **FLISOL** outreach.

## Connect with the Community

![The Oxidar community presentation in front of the audience, with links to join](/images/posts/raytracing-rust-recap/publico-oxidar.jpg)

Were you interested in the talk or do you want to keep learning about Rust? The **Oxidar** community is always open to new contributors!

### Ways to participate:
- **Join the discussions** on [Telegram](https://t.me/+7PgAQVPclxIzOGQ0) or on our [Discord](https://discord.gg/EMpekX7en)
- **Explore the projects** on our [GitHub](https://github.com/oxidar-org)
- **Follow our events** on the [public Oxidar calendar](https://calendar.google.com/calendar/embed?src=c_ac1102f85b1a406dd0a442876323f149a9c72aa29381a26e2af2c82cabc28661%40group.calendar.google.com&ctz=America%2FArgentina%2FBuenos_Aires) — *our talks are open, you can always join*
- **Want the next one to be at your school or in your city?** Write to us at [admin@oxidar.org](mailto:admin@oxidar.org) 🦀