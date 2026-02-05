+++
date = '2025-08-21T20:00:00-03:00'
draft = false
hiddenFromHomePage = false
title = 'gRPC in Rust'
description = "Relive the August 21st presentation on how to use gRPC in Rust"
tags = ["rust", "grpc", "protobuf", "protocol-buffers", "tonic", "prost", "presentation", "video"]
categories = ["Projects", "Events"]
translationKey = "grpc"
+++

# gRPC in Rust: Protocol Buffers and High-Performance Framework

On August 21st, 2025, a new Rust community meetup took place, where Alejandro Gonzalez presented a practical introduction to gRPC in Rust. Alejandro shared knowledge about Protocol Buffers and gRPC, focusing on their implementation in Rust for high-performance environments.

---

## Presentation

In this presentation, Alejandro Gonzalez guides us through Protocol Buffers and gRPC in Rust. We explore what they are, their advantages, comparisons, tools like Protoc, Prost and Tonic, practical examples, and industry use cases, including a demo of a chat application. The talk emphasizes how these technologies enable efficient and secure communications in distributed systems, leveraging Rust's strengths in safety and performance.

{{< youtube AcZiZasZQbY >}}

---

## Download the Slides

[**Download presentation slides (PDF)**](/slides/grpc.pdf)

The slides include:

- Detailed agenda
- Protocol Buffers explanation: what it is, why use it, comparisons, and tools
- gRPC details: pros, cons, Rust implementation, and examples
- Use cases in microservices, IoT, and more
- Additional resources and tools

---

## Protocol Buffers

Protocol Buffers, available at https://protobuf.dev, is a data interchange format that is language and platform agnostic, with a strongly typed schema. Developed by Google, Protocol Buffers is a language-neutral and platform-neutral mechanism for serializing structured data, designed to be smaller, faster, and simpler compared to formats like XML or JSON. It allows you to define data structures once and generate source code to read and write the data in various data streams and programming languages.

### Why Use It

- Compact (faster to transmit), which reduces payload size and speeds up transmission
- Fast to serialize/deserialize, improving performance in high-volume applications
- Schema evolution: you can add or deprecate fields without breaking existing clients or services

### Cons

- Not human-readable, which complicates manual debugging
- Less flexible for ad-hoc data, as it requires a fixed schema
- Limited built-in data types (e.g., no native support for dates/timestamps)

### Encoding / Decoding

- Field name is not encoded, which saves space
- Field type and number are encoded, using variable-length number encoding for efficiency
- Field order doesn't matter, allowing flexibility

Protocol Buffers uses editions like "2023" in proto definitions, with messages defining numbered fields (e.g., string name = 1;).

#### Comparison vs JSON

- Strings: ~2.7 times faster
- Numbers: ~34 times faster

#### Decoding:

- Strings: ~23 times faster
- Numbers: ~38 times faster

#### Payload Size:

Between 30% and 70% smaller, making it ideal for network-constrained environments.

> In general, Protocol Buffers is more efficient than JSON in terms of size and speed, although JSON is more human-readable.

## Protoc

Protoc is the official command-line tool that transforms .proto files into source code. It supports many languages natively, such as Python, Ruby, Java, C++, and Rust (through plugins). It can be extended to support new languages via plugins (e.g., Go).

The process is very simple: Input a .proto file and generate code for the desired language, facilitating interoperability.

## Rust: Prost

[prost](https://github.com/tokio-rs/prost) is a Protocol Buffers implementation for Rust. It generates simple and idiomatic Rust code from .proto files, using abstractions like `bytes::{Buf, BufMut}` for serialization. It supports `proto2` and `proto3`, retains .proto comments, allows serialization of existing Rust types with attributes, and preserves unknown enum values.

Example: github.com/oxidar-org/rust-proto-sample. This repo demonstrates the use of prost-build to generate Rust code from .proto, with an example of encoding/decoding a `User` struct. It includes `build.rs` for compilation and generates code in `my_package.rs`.

Commands:
- `cargo build` to generate
- `cargo run` to execute the example, which shows encoded and decoded bytes

## gRPC

[gRPC](https://grpc.io/) is a high-performance, open-source RPC framework. It's a modern framework for remote procedure calls (RPC) that can run in any environment, efficiently connecting services with support for load balancing, tracing, health checking, and authentication:

- Based on HTTP/2 for efficient transport
- Uses Protocol Buffers for service definitions
- Strongly typed APIs with automatic client/server stub generation for multiple languages
- Offers bidirectional streaming, asynchronous communication, built-in authentication, TLS with rustls, load balancing, and health checking

## Tools

- `grpcurl`: Like cURL, but for gRPC
- `postman`: Platform for API testing (supports gRPC)
- `Awesome-grpc`: Curated list of useful resources for gRPC

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
