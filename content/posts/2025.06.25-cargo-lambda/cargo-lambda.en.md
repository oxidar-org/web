+++
date = '2025-04-03T14:30:00-03:00'
draft = false
hiddenFromHomePage = false
title = 'Rust on AWS Lambda with Cargo Lambda'
description = "Explore our collaborative project on how to use Cargo Lambda to efficiently deploy Rust functions on AWS Lambda"
tags = ["rust", "aws", "lambda", "cargo-lambda", "serverless", "collaboration"]
categories = ["Projects", "Tutorials", "Events"]
translationKey = "cargo-lambda"
+++

## A New Community Collaboration

At **Oxidar**, we believe in the power of collaborative learning. That's why we're pleased to share one of our most recent projects: **[oxidar-lambdas](https://github.com/oxidar-org/oxidar-lambdas)**, a hands-on exploration of how to deploy **Rust** functions on **AWS Lambda** using **Cargo Lambda**.

---

## What is Cargo Lambda?

**Cargo Lambda** is a tool that greatly simplifies the development and deployment of Lambda functions written in Rust. Without this tool, you would have to:

- Manually configure cross-compilation toolchains
- Handle binary packaging
- Write custom deployment scripts
- Deal with the complexities of the AWS Lambda runtime

Cargo Lambda eliminates all this friction and allows us to focus on writing quality Rust code.

---

## Presentation

We presented a talk on how to use Rust in the cloud with AWS and Cargo Lambda at the **Rust Argentina** meetup.

{{< youtube IfWgf2Z_rSU >}}

---

## What We Presented

**Nicolás Antinori** presented "Creating a Lambda Authorizer in Rust with Cargo Lambda," where we explored in detail how to use Rust to create AWS Lambda functions in a real use case, what tools exist, and how using Rust helps us save resources, which translates to cost savings.

### Tech Stack Presented
- **Rust** - The programming language used
- **Cargo Lambda** - CLI tool for creating AWS Lambda functions in Rust
- **Amazon Web Services** - The cloud provider used for the project

---

## Download the Slides

[**Download presentation slides (PDF)**](/slides/cargo-lambda.pdf)

The slides include:
- What is Cargo Lambda
- Basic Cargo Lambda commands
- Performance of the created Authorizer
- Samples of tracing obtained with OpenTelemetry
- Link to the repository with the code

## What We Built Together

Our **oxidar-lambdas** repository includes:

### Project Structure
- **Multiple Lambda functions** in Rust
- **Local DynamoDB configuration** with Docker
- **Automated testing and deployment scripts**
- **JWT handling** for authentication
- **Tracing configuration** for observability

### Tools and Technologies
- **Rust** as the main language
- **Cargo Lambda** for build and deploy
- **AWS Lambda** as the serverless platform
- **DynamoDB** for persistence
- **Docker** for local development
- **GitHub** for collaboration

---

## Essential Cargo Lambda Commands

### Installation
```bash
# With pip (requires Python 3)
pip3 install cargo-lambda

# With Homebrew (macOS/Linux)
brew tap cargo-lambda/cargo-lambda
brew install cargo-lambda

# With Scoop (Windows)
scoop bucket add cargo-lambda
scoop install cargo-lambda/cargo-lambda
```

### Local Development
```bash
# Create a new Lambda project
cargo lambda new my-function

# Build for production
cargo lambda build --release

# Build for ARM64 (Graviton2)
cargo lambda build --release --arm64

# Local server for testing
cargo lambda watch
```

### Testing and Deployment
```bash
# Invoke function locally
cargo lambda invoke --data-example apigw-request

# Invoke with custom data
cargo lambda invoke --data-file ./data.json

# Deploy to AWS
cargo lambda deploy my-function
```

---

## Why Rust on Lambda?

### Advantages of Using Rust
- **Performance**: Fast cold starts and efficient execution
- **Memory safety**: No worries about memory leaks
- **Concurrency**: Excellent handling of asynchronous operations
- **Ecosystem**: Robust crates for AWS and web development

### Ideal Use Cases
- **High-performance APIs**
- **Real-time data processing**
- **Low-latency microservices**
- **Data transformation functions**

---

## The Power of Collaboration

This project was possible thanks to the collaboration of several **Oxidar** members:

- **[@nicoan](https://github.com/nicoan)** - Nicolás Antinori
- **[@aleiton](https://github.com/aleiton)** - Alejandro Leiton

Together we explored different aspects:
- Development environment configuration
- Error handling patterns in Lambda
- Integration with AWS services
- Cold start optimization
- Serverless function testing

---

## Key Learnings

### 1. Workflow Simplification
Cargo Lambda significantly reduces the learning curve for developing Lambda with Rust.

### 2. Efficient Local Development
The `cargo lambda watch` command enables a fast and comfortable development cycle.

### 3. Compatibility with the AWS Ecosystem
Integration with tools like AWS SAM and CDK is seamless.

### 4. Exceptional Performance
Rust functions in Lambda offer excellent performance and memory efficiency.

---

## Additional Resources

- **[Project Repository](https://github.com/oxidar-org/oxidar-lambdas)**
- **[Official Cargo Lambda Documentation](https://www.cargo-lambda.info/)**
- **[AWS Lambda Rust Runtime](https://github.com/awslabs/aws-lambda-rust-runtime)**
- **[AWS Guide on Rust in Lambda](https://docs.aws.amazon.com/lambda/latest/dg/rust-package.html)**

---

## Next Steps

As a community, we continue exploring:

- **Integration with other AWS services**
- **Serverless architecture patterns**
- **Lambda cost optimization**
- **Advanced monitoring and observability**

---

## Join Us!

Are you interested in contributing to projects like this? The **Oxidar** community is always open to new collaborators!

### Ways to Participate:
- **Explore the code** in our repository
- **Propose improvements** through issues and PRs
- **Share your experience** with Rust and serverless
- **Join our discussions** on [Telegram](https://t.me/+7PgAQVPclxIzOGQ0)

---

## Conclusion

**oxidar-lambdas** is more than a technical project; it's an example of how shared knowledge and collaboration can accelerate the learning of an entire community.

Rust and serverless computing are technologies that are transforming how we build modern applications. With tools like **Cargo Lambda**, that transformation is within reach of any developer willing to experiment.

Do you have experience with Rust on Lambda? Questions about serverless? We'd love to hear your perspective!

---

**Thank you for helping grow the Rust community in Latin America!**

*For more projects and collaborations, visit our [GitHub](https://github.com/oxidar-org) and join our [community](https://t.me/+7PgAQVPclxIzOGQ0).*
