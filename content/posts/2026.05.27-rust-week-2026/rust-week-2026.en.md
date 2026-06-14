+++
date = '2026-05-27T00:00:00-03:00'
draft = false
hiddenFromHomePage = false
title = "RustWeek 2026: What We Brought Back from Utrecht"
description = "RustWeek 2026 Chronicle in Utrecht: Over 900 Attendees, 50 Talks, Workshops, and the Rust All-Hands."
tags = ["rust", "community", "conference", "events"]
categories = ["Events", "Community"]
translationKey = "rust-week-2026"
+++
Last week we traveled to **Utrecht, Netherlands** to attend **RustWeek 2026**, returning home with our heads full of ideas and renewed energy to keep building with Rust.

![RustWeek 2026 — opening at Kinepolis Utrecht](/images/rustweek26-apertura.jpeg)

## What is RustWeek

RustWeek 2026 was presented as **the largest Rust conference in the world**, and the numbers back it up: more than **900 attendees**, 50 talks across 3 tracks, 8 workshops, a hackathon, and the second **Rust Project All-Hands**. All of this took place over a full week (May 18th to 23rd) at three different venues in Utrecht.

The choice of Utrecht was no coincidence. The city is in the heart of the Netherlands, with direct train connections from Amsterdam airport, making it accessible for those of us traveling from anywhere in the world.

## Conference Days

### Tuesday and Wednesday: The Conference

The two main days were held at **Kinepolis**, with a capacity of 800 attendees per day. Three simultaneous tracks meant there were always tough decisions about which session to prioritize.

Here are the talks that left the biggest impression on us:

---

#### Lessons Learnt from using Rust as the Intro to Programming

One of the most refreshing talks of the event. It explored the experience of teaching Rust as a **first programming language** — something that sounds counterintuitive given Rust’s reputation for difficulty. The takeaway was interesting: the compiler, which often frustrates us adults coming from other languages, turns out to be an excellent teacher for someone learning from scratch. The error messages are descriptive, the type system forces precise thinking, and the compiler's "why?" moments become genuine learning opportunities.

![Why Rust — talk about teaching Rust as a first language](/images/rustweek26-why-rust-teaching.jpeg)

> *"I really believe anyone can learn anything. We just need to change the world a little bit. I believe Rust can be part of that."*

![](/images/rustweek26-believe-rust.jpeg)

{{< youtube 8iy37I0WE_s >}}

---

#### Completion-based IO

A deep technical talk on the I/O model based on **completions** (like io_uring on Linux), compared to the traditional readiness-based model used by Rust’s async runtimes today. Alice explored the challenges of integrating this model with the existing async ecosystem: differences in buffer handling, cancellation, and why the transition is not trivial. For anyone working with systems where I/O performance matters, this was one of the most relevant talks of the week.

{{< youtube CmLAHUuUsAQ >}}

---

#### Untrusted data in Linux — How Rust is going to save us

**Greg Kroah-Hartman** from the Linux Foundation delivered one of the most applauded keynotes. The message was clear: Rust in the Linux kernel is not an experiment — it is a necessity. The talk detailed the work of handling **untrusted data** coming from userspace, an area where memory bugs have historically caused critical vulnerabilities. Rust allows expressing these invariants directly in the type system.

![Greg Kroah-Hartman: "We need more Rust Linux developers!"](/images/rustweek26-linux-keynote.jpeg)

He also presented concrete data about the decrease in memory vulnerabilities in projects that adopted Rust.

![Data on the decrease of memory vulnerabilities](/images/rustweek26-memory-safety.jpeg)

{{< youtube Nzmj7K0FNRY >}}

---

#### Obsessive Optimization with String Interning

**Arya Dradjica** gave one of the most entertaining talks on the performance track. She started with a seemingly simple problem — repeated strings frequently compared — and built layers of optimization, measuring at each step with real benchmarks. The methodology was exemplary: using `perf`, analyzing L1 cache accesses, measuring cycles per iteration. A masterclass on how to do performance engineering in Rust without guessing.

![Obsessive Optimization with String Interning — Arya Dradjica](/images/rustweek26-string-interning.jpeg)

{{< youtube SWRL4JpaR2I >}}

---

#### Interop is the New Rewrite: Design Axioms for Rust's Next Frontier

**Taylor Cramer (Google)** closed with a strategic talk about Rust’s future. The central argument: Rust’s next big challenge is not rewriting systems in Rust, but **interoperating with the existing world** — especially C++, which dominates low-level interfaces (system libraries, ABIs, linkers). But C++ cannot express ownership, lifetimes, nor destructors, creating a semantic gap when crossing the boundary.

![The Trouble with C Interop — Taylor Cramer](/images/rustweek26-c-interop.jpeg)

The talk proposed concrete design axioms to guide future work in this space. A roadmap for those working on FFI or integrating Rust into existing C/C++ projects.

{{< youtube 1NnCJTVYPA4 >}}

## What We Took Away

Beyond the talks and the slides that will be published, what we valued most at events like this is the **people**. Talking with folks using Rust in completely different contexts — embedded systems, kernel, web backend, compilers — and seeing how the same tools solve such different problems is a reminder of why this community is special.

![Strategies for Rust: "Design holistically. Ship incrementally."](/images/rustweek26-strategies.jpeg)

![Representing Oxidar at RustWeek 2026](/images/rustweek26-oxidar-tshirt.jpeg)

It’s also motivating to see how much space there is for **regional communities like Oxidar** to contribute. Rust in Latin America still has a lot of ground to cover, and events like RustWeek are a great place to bring that energy back home.

![Group photo closing RustWeek 2026](/images/rustweek26-grupo.jpeg)

And to finish, a detail that sums up the spirit of the conference: among the posters at the Kinepolis cinema, the RustWeek team put up their own parodied versions of classic movies. “Box to the Future – 1.21 Gigabytes,” featuring a DeLorean with a license plate that said **ENOMEN**. Rust community humor at its finest.

![Box to the Future — 1.21 Gigabytes](/images/rustweek26-back-to-future.jpeg)

## The Talks Are Now Available

Recordings are already published on the [RustNL YouTube channel](https://www.youtube.com/@RustNL). You can also check out the full program at [2026.rustweek.org](https://2026.rustweek.org).

---

Did you attend RustWeek 2026? Which talk did you find most interesting? Tell us in the [Telegram group](https://t.me/+7PgAQVPclxIzOGQ0) or on our [Discord](https://discord.gg/EMpekX7en). 🦀