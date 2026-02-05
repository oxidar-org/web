+++
date = '2025-07-09T14:30:00-03:00'
draft = false
hiddenFromHomePage = false
title = 'Tips for Rust in Enterprise Environments'
description = "Practical advice and strategies for adopting Rust in companies."
tags = ["rust", "community", "adoption", "collaboration"]
categories = ["Events"]
translationKey = "rust-adoption"
+++

# Rust in Industry: Correctness, Adoption, and Community

On April 3rd, a new Rust community meetup took place where **Alejandro Leiton**, software developer at **VAIRIX** and Rust enthusiast, shared an updated view of the ecosystem's state, focusing on the tool, its adoption in industry, and the community that drives it.

---

## Presentation

In this presentation, Alejandro Leiton gives us practical advice and strategies for adopting Rust in companies. We explore cases, how to train teams in the language, and the current state of the Rust community.

{{< youtube Bj-Ka26CSFk >}}

---

## Download the Slides

[**Download presentation slides (PDF)**](/slides/rust-adoption.pdf)

The slides include:
- Existing tooling in Rust
- Adoption in companies like Google and Microsoft
- Adoption in open source projects like Linux and Ubuntu
- Information about existing communities

---

## Ecosystem and Tools

Rust has a robust ecosystem and first-class tools. At its heart is [crates.io](https://crates.io), the official Rust package registry, which functions as the equivalent of `npm` (JavaScript) or `pip` (Python). Officially backed by the [Rust Foundation](https://foundation.rust-lang.org/), crates.io offers:

- Scalable and secure infrastructure
- Package security monitoring
- Coordination with other ecosystem actors

Among the most relevant crates for enterprise applications are:

- [`tokio`](https://crates.io/crates/tokio): asynchronous development, driven by the Rust Foundation
- [`axum`](https://crates.io/crates/axum): modern web framework
- [`mongodb`](https://crates.io/crates/mongodb): official MongoDB driver
- [`aws-sdk-s3`](https://crates.io/crates/aws-sdk-s3): official Amazon SDK for cloud services
- [`pingora`](https://github.com/cloudflare/pingora): Cloudflare's API gateway, developed in Rust

## Enterprise Adoption

### Google

Google has adopted Rust as a first-class language for Android and Chromium. A key fact: in internal A/B testing, it was observed that Rust code is as productive as Go and twice as productive as C++, while also having:

- Lower memory usage
- Lower error rate
- High confidence in code correctness ("If it compiles, it works")

**85%** of surveyed developers at Google stated they feel more confident about the correctness of their Rust code. In less than **4 months**, they reach productivity levels similar to their previous language.

> Google also donated **USD 1 million** to the Rust Foundation to work on C++ bridges.
> Source: [The Register](https://www.theregister.com/2024/02/05/google_rust_donation)

### Microsoft

Microsoft has also invested heavily in Rust:

- **USD 10 million** in tooling
- **USD 1 million** in donations to the Rust Foundation

They identified that **70% of their vulnerabilities** in the last decade were memory errors. In response, they began rewriting critical parts of Windows with Rust:

- **DirectWrite Core**: migrated by 2 devs in 6 months (154K lines of code)
- **Win32K GDI Region**: reimplemented in 3 months

They also use Rust in Azure services such as:

- **Caliptra**: hardware root of trust
- **Hyper-V**, **OpenVMM**, **HiperLight**: virtualization technologies
- **Azure Data Explorer** and internal HSM chips

> Source: [Microsoft Open Source Blog](https://opensource.microsoft.com/blog/2025/02/11/hyperlight-creating-a-0-0009-second-micro-vm-execution-time/)

### Linux and Ubuntu

Rust has been advancing in the Linux kernel since 2020, and some distributions are adopting it as an official option:

- **Ubuntu 25.10** plans to replace GNU `coreutils` with tools written in Rust

> Source: [The Register](https://www.theregister.com/2025/03/19/ubuntu_2510_rust/)

### Other Companies

- **Amazon (AWS)**: uses Rust in [Firecracker](https://firecracker-microvm.github.io/) and Bottlerocket
- **Meta (Facebook)**: backend services and cryptography
- **Cloudflare & Discord**: low-latency and high-concurrency systems
- **Figma**: parts of the backend were rewritten in Rust to improve real-time performance

> [Why Discord is switching from Go to Rust](https://discord.com/blog/why-discord-is-switching-from-go-to-rust)

> [Rust in production at Figma](https://www.figma.com/blog/rust-in-production-at-figma/)

## Community

The Rust community is one of the pillars of the language. There are multiple spaces for participation, both virtual and in-person:

### Conferences

- [RustWeek](https://rustweek.org/)
- [RustConf](https://rustconf.com/)
- [EuroRust](https://eurorust.eu/)
- [RustNation UK](https://www.rustnationuk.com/)

### Online Community

- [Official Forum](https://users.rust-lang.org/)
- [Subreddit r/rust](https://www.reddit.com/r/rust/)
- [Zulip Support Channel](https://rust-lang.zulipchat.com/)
- [Community Discord](https://discord.gg/rust-lang-community)
