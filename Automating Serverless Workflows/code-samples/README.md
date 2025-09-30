# Code Samples

This folder contains code examples, scripts, and demos used in the "Automating Serverless Workflows" presentation.

## 🎯 Main Demo Repository

For complete, deployable examples with full infrastructure and CI/CD, visit:

**[mms-basic-functions-and-containers](https://github.com/donnietaylor/mms-basic-functions-and-containers)**

This repository provides a comprehensive learning path with:
- Progressive demo series from basic to advanced
- Azure Functions examples using PowerShell
- Azure Container Apps implementations
- Complete Terraform infrastructure as code
- GitHub Actions CI/CD pipelines
- Integration patterns and microservices architecture

## Demo Series Overview

### 🟢 Demo 1: Simple HTTP Trigger Function
- Basic Azure Functions concepts
- HTTP triggers and responses
- PowerShell in the cloud
- [View Demo 1](https://github.com/donnietaylor/mms-basic-functions-and-containers/tree/main/functions/demo1-simple)

### 🟡 Demo 2: Function with Storage Integration
- Azure Storage integration
- Data persistence with Blob Storage
- PowerShell Az.Storage module
- [View Demo 2](https://github.com/donnietaylor/mms-basic-functions-and-containers/tree/main/functions/demo2-storage)

### 🟠 Demo 3: PowerShell Container App
- Container Apps basics
- Containerized PowerShell APIs
- Docker and Azure Container Registry
- [View Demo 3](https://github.com/donnietaylor/mms-basic-functions-and-containers/tree/main/containers/demo3-simple)

### 🔴 Demo 4: Integrated Solution
- Microservices architecture
- Service-to-service communication
- Shared storage patterns
- Complete serverless solution
- [View Demo 4](https://github.com/donnietaylor/mms-basic-functions-and-containers/tree/main/terraform/demo4)

## Quick Start

```bash
# Clone the demo repository
git clone https://github.com/donnietaylor/mms-basic-functions-and-containers.git
cd mms-basic-functions-and-containers

# Follow the README for prerequisites and setup
# Each demo builds on the previous one
```

## Technologies Covered

- ✅ **Azure Functions** - Event-driven serverless compute
- ✅ **Azure Container Apps** - Serverless containers with KEDA scaling
- ✅ **Azure Blob Storage** - Data persistence and integration
- ✅ **PowerShell 7.2** - Cross-platform scripting language
- ✅ **Terraform** - Infrastructure as Code
- ✅ **GitHub Actions** - CI/CD pipelines
- ✅ **Docker** - Container packaging
- ✅ **Azure Container Registry** - Private container images

## Local Development

All demos support local development:
- Test functions locally with Azure Functions Core Tools
- Build and run containers locally with Docker
- Plan infrastructure changes with Terraform

See the [main repository README](https://github.com/donnietaylor/mms-basic-functions-and-containers#-local-development) for detailed local development instructions.

## Additional Examples

This folder may contain additional code snippets and examples referenced during the presentation. For complete, working solutions, always refer to the main demo repository.