+++
date = '2025-11-27T20:00:00-03:00'
draft = false
hiddenFromHomePage = false
title = 'Async Rust: Sharing Memory'
description = 'How to handle shared memory in Async Rust, comparing different approaches and highlighting the importance of choosing the right model based on concurrency and parallelism needs'
tags = ["rust", "async", "await", "concurrency", "runtimes", "presentation", "video"]
categories = ["Projects", "Events"]
translationKey = "async-patterns"
+++

# Async Rust: Sharing Memory

On November 27th, 2025, Gabriel Steinberg presented a talk titled *Async Rust: Sharing Memory*, where he explored different methods for handling shared mutable state in asynchronous Rust applications.

## Presentation

In this presentation, Gabriel Steinberg explains how to handle shared memory in Async Rust, comparing different approaches and highlighting the importance of choosing the right model based on concurrency and parallelism needs.

{{< youtube FEBSepG0Lr4 >}}

---

## Download the Slides

[**Download presentation slides (PDF)**](/slides/async-patterns.pdf)

The slides include:
- Examples of TCP servers in Rust
- Common problems with the borrow checker in async contexts
- Usage of `Mutex`, `Arc`, and channels for synchronization
- Alternative models for concurrency and parallelism

---

## From Naive Implementation to Synchronization

When trying to implement an asynchronous TCP server with Tokio, a problem quickly arises: the mutable borrow of `self` escapes the connection acceptance loop. This happens because `tokio::spawn` requires `'static` futures, which breaks the borrow checker rules.

**Initial conclusion:** we need synchronization mechanisms to share mutable state.

### Mutex

A first solution is to use `tokio::sync::Mutex`. This allows maintaining a `HashMap` of connections and locking it while performing `await` operations. However, this approach can lead to performance issues.

### Channels

A more robust alternative is to use **channels (`mpsc`)** to communicate between tasks. In this model:
- Each connection is handled with an `OwnedWriteHalf`
- Messages are sent to a *central dispatcher* that decides how to distribute them
- Backpressure and error handling mechanisms can be added

This approach avoids locks and allows greater control over message flow. But it has the tradeoff of complexity in handling each interaction between tasks, is difficult to debug, and error handling becomes unnatural.

### Single Task

Finally, a simplified model was shown: handling all connections in a **single task** that runs a race of futures (`race`). This design sacrifices parallelism but offers:
- Direct and safe access to mutable state
- Natural error flow
- Ease of tracing the origin of values

---

## Conclusions

- **Trade-offs:** Mutex vs Channels vs Race/Select
- **Evaluate parallelism:** it's not always necessary, and can complicate the design
- **Channels:** recommended when parallelism is needed
- **Mutex:** useful in very specific cases

---

## References

- [Comparing patterns for mutable state in concurrent applications (post the talk is based on)](https://taping-memory.dev/concurrency-patterns/)
- [Let futures be futures](https://without.boats/blog/let-futures-be-futures/)
- [Tree-Structured Concurrency](https://blog.yoshuawuyts.com/tree-structured-concurrency/)
- [Tree-Structured Concurrency II: Replacing Background Tasks With Actors](https://blog.yoshuawuyts.com/replacing-tasks-with-actors/)
- [sans-IO: The secret to effective Rust for network services](https://www.firezone.dev/blog/sans-io)

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
