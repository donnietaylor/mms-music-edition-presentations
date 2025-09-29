# Remote State Management Examples

Learn how to configure and use remote state backends for team collaboration and state security.

## 🎯 Remote State: ClickOps vs DevOps

| Local State (ClickOps-ish) | Remote State (DevOps) |
|----------------------------|------------------------|
| State file on developer's laptop | Centralized state in cloud storage |
| No collaboration possible | Multiple team members can work together |
| No state locking | Automatic state locking prevents conflicts |
| State file can be lost | Durable, backed up storage |
| No audit trail | Complete history of state changes |
| Sensitive data in local files | Encrypted storage with access controls |

## 📋 Prerequisites

- Terraform installed and configured
- Azure CLI installed and authenticated
- Appropriate permissions to create storage accounts
- Understanding of basic Terraform concepts

## 🚀 Quick Start

### Step 1: Set Up the Remote State Backend

Run the setup script to create Azure Storage resources:

```bash
# Make the script executable (if not already)
chmod +x setup-azure-backend.sh

# Run the setup script
./setup-azure-backend.sh
```

This script will:
- Create a resource group for Terraform state
- Create a storage account with encryption
- Create a blob container for state files
- Generate configuration snippets for you to use

### Step 2: Configure Your Terraform Backend

The setup script provides multiple ways to configure your backend:

#### Option A: Update terraform block directly
```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "terraformstateXXXXXXXX"
    container_name       = "terraform-state"
    key                 = "terraform.tfstate"
  }
}
```

#### Option B: Use command line parameters
```bash
terraform init \
  -backend-config="resource_group_name=rg-terraform-state" \
  -backend-config="storage_account_name=terraformstateXXXXXXXX" \
  -backend-config="container_name=terraform-state" \
  -backend-config="key=terraform.tfstate"
```

#### Option C: Use backend configuration file
```bash
# The setup script creates backend.hcl for you
terraform init -backend-config=backend.hcl
```

### Step 3: Initialize with Remote State

```bash
# Initialize Terraform with remote state
terraform init

# You should see output like:
# Successfully configured the backend "azurerm"!
```

### Step 4: Deploy Resources

```bash
# Plan and apply as usual
terraform plan
terraform apply
```

## 🔒 State Security Features

### Encryption at Rest
The Azure Storage backend provides:
- AES-256 encryption for data at rest
- TLS 1.2 minimum for data in transit
- Access keys and SAS tokens for authentication

### Access Control
```bash
# Limit access to the storage account
az storage account update \
  --name YOUR_STORAGE_ACCOUNT \
  --resource-group rg-terraform-state \
  --default-action Deny

# Add your IP to allowed list
az storage account network-rule add \
  --account-name YOUR_STORAGE_ACCOUNT \
  --resource-group rg-terraform-state \
  --ip-address YOUR_IP_ADDRESS
```

### State Locking
Azure Storage provides native state locking:
- Prevents concurrent `terraform apply` operations
- Automatically locks during state-modifying operations
- Releases lock when operation completes

## 👥 Team Collaboration Workflow

### Setup for New Team Member

1. **Get access to Azure subscription**
2. **Authenticate with Azure CLI**: `az login`
3. **Clone the repository**: `git clone <repo-url>`
4. **Initialize Terraform**: `terraform init`
5. **Verify access**: `terraform plan`

### Best Practices for Teams

#### 1. Environment Separation
```hcl
# Development environment
terraform {
  backend "azurerm" {
    key = "dev/terraform.tfstate"
  }
}

# Production environment
terraform {
  backend "azurerm" {
    key = "prod/terraform.tfstate"
  }
}
```

#### 2. State File Naming Convention
```
environments/
├── dev/
│   ├── networking/terraform.tfstate
│   ├── compute/terraform.tfstate
│   └── databases/terraform.tfstate
├── staging/
│   └── ...
└── prod/
    └── ...
```

#### 3. Access Control by Environment
```bash
# Create separate resource groups for different environments
az group create --name rg-terraform-state-dev --location "East US"
az group create --name rg-terraform-state-prod --location "East US"

# Assign different permissions to different teams
az role assignment create \
  --assignee dev-team@company.com \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/.../resourceGroups/rg-terraform-state-dev"
```

## 🔧 State Operations with Remote Backend

### View State Information
```bash
# Show current state
terraform show

# List resources in state
terraform state list

# Show specific resource
terraform state show azurerm_resource_group.example
```

### Import Existing Resources
```bash
# Import existing Azure resource into state
terraform import azurerm_resource_group.existing /subscriptions/.../resourceGroups/existing-rg

# Verify import
terraform plan
```

### Move Resources Between States
```bash
# Move resource to different Terraform configuration
terraform state mv azurerm_storage_account.old azurerm_storage_account.new

# Move resource to different state file (different backend key)
terraform state mv -state-out=other.tfstate azurerm_resource_group.example azurerm_resource_group.example
```

## 🚨 Troubleshooting Remote State

### Common Issues

#### State Lock Conflicts
```bash
# If terraform apply fails with lock error
terraform force-unlock LOCK_ID

# Check who has the lock (if supported by backend)
terraform state list
```

#### Authentication Issues
```bash
# Refresh Azure authentication
az login

# Check current subscription
az account show

# Set correct subscription
az account set --subscription "Your Subscription Name"
```

#### Backend Configuration Errors
```bash
# Reconfigure backend
terraform init -reconfigure

# Migrate from local to remote state
terraform init -migrate-state
```

#### State File Corruption
```bash
# Validate state file
terraform validate

# Pull latest state from backend
terraform refresh

# In emergency, restore from backup
# Azure Storage automatically maintains versions
```

## 🧹 Cleanup

### Remove Demo Resources
```bash
# Destroy resources created by Terraform
terraform destroy

# Remove the backend storage account (CAREFUL!)
az group delete --name rg-terraform-state --yes
```

### Migration Back to Local State
```bash
# Remove backend configuration from terraform block
terraform init -migrate-state

# Confirm state is now local
ls -la terraform.tfstate
```

## 📊 Monitoring and Auditing

### Azure Storage Metrics
```bash
# View storage account metrics
az monitor metrics list \
  --resource "/subscriptions/.../resourceGroups/rg-terraform-state/providers/Microsoft.Storage/storageAccounts/terraformstateXXXX" \
  --metric "Transactions"
```

### Access Logging
```bash
# Enable storage analytics logging
az storage logging update \
  --account-name terraformstateXXXX \
  --account-key YOUR_ACCOUNT_KEY \
  --services b \
  --log rwd \
  --retention 30
```

### Cost Monitoring
```bash
# View storage costs
az consumption usage list \
  --start-date 2024-01-01 \
  --end-date 2024-01-31 \
  --query "[?contains(instanceName, 'terraformstate')]"
```

## 🔗 Integration with CI/CD

### GitHub Actions Example
```yaml
name: Terraform
on: [push, pull_request]

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: hashicorp/setup-terraform@v2
      
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Terraform Init
        run: terraform init
      
      - name: Terraform Plan
        run: terraform plan
      
      - name: Terraform Apply
        if: github.ref == 'refs/heads/main'
        run: terraform apply -auto-approve
```

### Azure DevOps Pipeline
```yaml
trigger:
  branches:
    include:
      - main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: TerraformInstaller@0
  inputs:
    terraformVersion: '1.6.0'

- task: AzureCLI@2
  inputs:
    azureSubscription: 'Your Service Connection'
    scriptType: 'bash'
    scriptLocation: 'inlineScript'
    inlineScript: |
      terraform init
      terraform plan
      terraform apply -auto-approve
```

## 💡 Advanced Topics

- **State Encryption**: Additional encryption beyond Azure Storage default
- **Cross-Subscription State**: Managing state across multiple Azure subscriptions
- **State Splitting**: Breaking large state files into smaller, manageable pieces
- **Disaster Recovery**: Backup and recovery strategies for state files
- **Compliance**: Meeting regulatory requirements for state data