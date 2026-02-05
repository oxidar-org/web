+++
date = '2025-10-08T20:00:00-03:00'
draft = false
hiddenFromHomePage = false
title = 'Deep Dive into Async/Await'
description = 'A practical guide to understanding what the Rust compiler does when we use async/await, and how to write an async runtime from scratch.'
tags = ["rust", "async", "await", "concurrency", "runtimes", "presentation", "video"]
categories = ["Projects", "Events"]
translationKey = "async"
+++

# Deep Dive into Async: How async/await Works in Rust from Scratch

On October 8th, 2025, a new Rust community meetup took place, where Jorge Prendes presented what `async fn` really does, how the `Future` trait is implemented, and how a runtime like Tokio executes our concurrent tasks.

---

## Presentation

In this presentation, Jorge Prendes shows us how to build an async runtime from scratch, stopping and explaining each detail so we can deeply understand what happens when we execute asynchronous functions.

{{< youtube fbM_IP0VFiA >}}

---

## Download the Slides

[**Download presentation slides (PDF)**](/slides/async-await.pdf)

The slides include:

- Why build an async runtime from scratch
- Explanation of the anatomy of an async function
- Explanation of the `Future` trait and wakers
- What professional runtimes do

---

## From `fn` to `async fn`

At first glance, using `async fn` seems magical: we mark a function with `async`, add `.await`, and the code "works."
However, an `async fn` doesn't return the value directly, but rather a structure that implements the [`Future`](https://doc.rust-lang.org/std/future/trait.Future.html) trait.

The compiler automatically transforms the function into an anonymous type that implements `Future`, with a `poll` method that controls its progress.
This means that *`async fn` is syntactic sugar for a state machine that the compiler generates automatically.*
Each suspension point (`await`) internally becomes a state transition within that machine.

---

## The `Future` Trait

The heart of Rust's asynchronous model is the `Future` trait, which defines how a task progresses toward its final result.
Its `poll` method returns:
- `Poll::Ready(val)` when the future has completed its work, or
- `Poll::Pending` if it still cannot continue and needs to be retried later.

Each `Future` must guarantee that, if it returns `Pending`, it will notify the *runtime* when it's ready to proceed.
That notification is performed through a `Waker` object that is part of the execution context (`Context`).

In conceptual terms, a `Future` is a cooperative process: it doesn't execute by itself, but the runtime invokes it repeatedly until it returns a final value.

---

## Building a Minimal Runtime

Rust doesn't execute `async fn` functions automatically: it requires a *runtime* that manages the execution of futures.
A runtime is essentially a *scheduler* that maintains a task queue and calls `poll` on each one when progress is available.

A basic runtime can be implemented in a few lines: a loop that invokes `poll`, and waits for external events (for example, through a channel or an operating system selector).
When a `Future` returns `Pending`, the runtime suspends its execution and blocks until some `Waker` wakes it up.

This way, concurrency is achieved without the need for multiple threads, leveraging a single cooperative thread that manages multiple tasks efficiently.

---

## The Role of the `Waker`

The `Waker` is the mechanism through which futures notify the runtime that they're ready to continue.
When a `Future` returns `Poll::Pending`, it registers a `Waker` so that, when new work is available, it can invoke `wake_by_ref` and alert the runtime.

Runtimes like Tokio, Smol, or Embassy implement this concept with different strategies:
- **Tokio** uses operating system mechanisms like `epoll` or `kqueue` to manage thousands of I/O operations on a single thread.
- **Smol** employs a lightweight *thread pool* that leverages standard library primitives.
- **Embassy** is designed for environments without an operating system (bare metal), and uses a *Hardware Abstraction Layer (HAL)* to interact directly with the hardware.

In all cases, the principle is the same: the `Waker` connects futures with the scheduler that controls them.

---

## Interactive Demo

You can explore a practical implementation of the explained model in Rust Playground:

- [Basic version](https://play.rust-lang.org/?version=stable&mode=debug&edition=2024&gist=b51f63e714ab80cf109a443bfcbc9c46)
- [Advanced version](https://play.rust-lang.org/?version=stable&mode=debug&edition=2024&gist=c244fef8ad8aa124058234f63c7d096e)

The basic version executes sequential tasks, while the advanced one creates multiple futures that run in parallel on the same runtime.

---

## Conclusions

- An `async fn` is a syntactic transformation that generates a state machine implementing `Future`.
- Asynchronous runtimes like Tokio or Smol are *schedulers* that execute and reactivate futures based on system events.
- Implementing a simple runtime helps understand the fundamentals of Rust's asynchronous model.
- Understanding `poll`, `Context`, and `Waker` allows writing more efficient, predictable, and compatible code with existing runtimes.

Behind `async/await` there's no magic: just **deterministic transformations and an explicit concurrency model**.
Understanding these concepts is key to mastering asynchronous programming in Rust.

---

## References

- [Official `Future` Documentation](https://doc.rust-lang.org/std/future/trait.Future.html)
- [Official Tokio Tutorial](https://tokio.rs/tokio/tutorial/async#)
- [Smol Runtime](https://github.com/smol-rs/smol)
- [Embassy for Embedded Environments](https://github.com/embassy-rs/embassy)
- [Hyperlight Project](https://github.com/hyperlight-dev/hyperlight)

---

## Community

The Rust community is one of the pillars of the language. There are multiple spaces for participation, both virtual and in-person:

### Conferences

- [RustWeek](https://rustweek.org/)
- [RustConf](https://rustconf.com/)
- [EuroRust](https://eurorust.eu/)
- [RustNation UK](https://www.rustnationuk.com/)

### Online Community

- [Rust in Spanish - Telegram](https://t.me/rust_lang_es)
- [Official Forum](https://users.rust-lang.org/)
- [Subreddit r/rust](https://www.reddit.com/r/rust/)
- [Zulip Support Channel](https://rust-lang.zulipchat.com/)
- [Community Discord](https://discord.gg/rust-lang-community)
