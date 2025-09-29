# Simple Resource Deployments

Learn Infrastructure as Code by deploying basic cloud resources with Terraform instead of clicking through web portals.

## 🎯 ClickOps vs DevOps Transformation

| Manual Approach (ClickOps) | Terraform Approach (DevOps) |
|----------------------------|------------------------------|
| Login to Azure Portal | `az login` + `terraform apply` |
| Navigate through menus | Define resources in code |
| Fill forms manually | Use variables and modules |
| Resources created inconsistently | Reproducible deployments |
| No change tracking | Git history + state files |
| Difficult to replicate | `terraform apply` anywhere |

## 📁 Examples

### [azure/](./azure/)
Azure Resource Group and Storage Account deployment
- Basic resource group creation
- Storage account with configuration
- Output values for integration

### [aws/](./aws/)
AWS S3 bucket with basic configuration
- S3 bucket creation
- Bucket policies and settings
- CloudWatch integration example

### [multi-cloud/](./multi-cloud/)
Side-by-side comparison of similar resources across providers
- Storage: Azure Storage Account vs AWS S3
- Compute: Azure VM vs AWS EC2
- Networking: Azure VNet vs AWS VPC

## 🚀 Getting Started

1. **Choose your cloud provider** (Azure or AWS)
2. **Set up authentication** (see provider-specific guides)
3. **Start with basic examples** in your chosen provider folder
4. **Compare approaches** using the multi-cloud examples

## 📋 Prerequisites

- Terraform installed (see [installation guide](../installation/))
- Cloud provider CLI installed and configured
- Basic understanding of your chosen cloud platform

## 🔑 Key Concepts Demonstrated

- **Provider Configuration**: Connecting Terraform to cloud APIs
- **Resource Blocks**: Defining infrastructure components
- **Variables**: Making configurations reusable
- **Outputs**: Extracting important values
- **State Management**: Understanding Terraform's state tracking

Each example includes:
- ✅ Complete working Terraform code
- 📖 Step-by-step instructions
- 🔍 Explanation of ClickOps vs DevOps benefits
- 🧪 Testing and validation steps