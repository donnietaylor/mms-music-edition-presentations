# Terraform Examples - ClickOps to DevOps

This directory contains practical Terraform examples demonstrating the transformation from manual infrastructure operations to Infrastructure as Code (IaC).

## 🚀 Quick Start

1. **Install Terraform** - See [installation guide](./installation/)
2. **Try Simple Resources** - Start with [basic deployments](./simple-resources/)
3. **Learn State Management** - Understand [Terraform state](./state-management/)
4. **Handle Drift** - Master [drift detection and correction](./drift-detection/)

## 📁 Directory Structure

### [installation/](./installation/)
Local Terraform setup guides for different platforms, version management, and initial configuration.

### [simple-resources/](./simple-resources/)
Basic resource deployment examples including:
- Azure Resource Groups and Storage Accounts
- AWS S3 buckets and basic infrastructure
- Multi-cloud comparison examples

### [state-management/](./state-management/)
Terraform state file examples covering:
- Local vs. remote state backends
- State inspection and manipulation
- Import/export workflows

### [drift-detection/](./drift-detection/)
Drift management scenarios including:
- Detecting configuration drift
- Manual resource modification scenarios
- Correction workflows and best practices

## 🎯 Learning Path

**Beginner**: Start with `installation/` → `simple-resources/`  
**Intermediate**: Focus on `state-management/` → `drift-detection/`  
**Advanced**: Combine all concepts for real-world scenarios

## 💡 ClickOps vs DevOps Comparison

| Manual (ClickOps) | Automated (DevOps) |
|------------------|-------------------|
| Azure Portal clicking | `terraform apply` |
| Inconsistent deployments | Reproducible infrastructure |
| Manual state tracking | Automated state management |
| Drift goes unnoticed | Continuous drift detection |
| Knowledge in heads | Code-documented infrastructure |

Each example includes both the "before" (manual) and "after" (Terraform) approaches to highlight the transformation benefits.