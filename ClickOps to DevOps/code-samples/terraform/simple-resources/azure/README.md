# Azure Simple Resources - ClickOps to DevOps

This example demonstrates deploying basic Azure resources using Terraform instead of manually clicking through the Azure Portal.

## 🎯 What This Demo Shows

**ClickOps Approach** (Manual):
1. Login to Azure Portal
2. Navigate to "Resource groups" → "Create"
3. Fill out form with name, region, tags
4. Navigate to "Storage accounts" → "Create"
5. Fill multiple pages of configuration
6. Manually create blob container
7. Document details manually

**DevOps Approach** (Terraform):
1. Define infrastructure in code
2. Run `terraform apply`
3. All resources created consistently
4. Configuration version controlled
5. Outputs automatically available

## 📋 Prerequisites

### 1. Install Required Tools
```bash
# Install Terraform (see ../../../installation/)
terraform --version

# Install Azure CLI
# Windows: winget install Microsoft.AzureCLI
# macOS: brew install azure-cli
# Linux: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
az --version
```

### 2. Authenticate with Azure
```bash
# Login to Azure
az login

# Verify your subscription
az account show

# Set subscription if needed
az account set --subscription "Your Subscription Name"
```

## 🚀 Deploy the Infrastructure

### Step 1: Initialize Terraform
```bash
# Navigate to this directory
cd azure/

# Initialize Terraform (downloads providers)
terraform init
```

### Step 2: Plan the Deployment
```bash
# See what will be created
terraform plan

# Plan with custom values
terraform plan -var="location=West US 2" -var="environment=dev"
```

### Step 3: Apply the Configuration
```bash
# Deploy the infrastructure
terraform apply

# Deploy with custom values
terraform apply -var="location=West US 2" -var="environment=dev"
```

### Step 4: View Outputs
```bash
# See all outputs
terraform output

# Get specific output
terraform output storage_account_name

# Get sensitive output (access key)
terraform output -raw storage_account_primary_access_key
```

## 📊 What Gets Created

1. **Resource Group**: Container for all resources
   - Naming: `rg-clickops-to-devops-{random}`
   - Tags: Environment, Purpose, ManagedBy, CreatedBy

2. **Storage Account**: Blob storage with security settings
   - Naming: `storage{random}`
   - Security: HTTPS only, TLS 1.2 minimum
   - Replication: Locally Redundant Storage (LRS)

3. **Blob Container**: Private container for file storage
   - Name: `demo-container`
   - Access: Private (no anonymous access)

## 🧪 Testing Your Deployment

### Verify Resources in Azure Portal
```bash
# Get resource group name
RESOURCE_GROUP=$(terraform output -raw resource_group_name)

# List resources in the group
az resource list --resource-group $RESOURCE_GROUP --output table
```

### Test Storage Account
```bash
# Get storage account details
STORAGE_ACCOUNT=$(terraform output -raw storage_account_name)
az storage account show --name $STORAGE_ACCOUNT --resource-group $RESOURCE_GROUP
```

### Upload a Test File
```bash
# Get storage account key
STORAGE_KEY=$(terraform output -raw storage_account_primary_access_key)

# Create a test file
echo "Hello from Terraform!" > test-file.txt

# Upload to container
az storage blob upload \
  --account-name $STORAGE_ACCOUNT \
  --account-key $STORAGE_KEY \
  --container-name demo-container \
  --file test-file.txt \
  --name test-file.txt
```

## 🧹 Cleanup

### Remove All Resources
```bash
# Destroy all created resources
terraform destroy

# Destroy with auto-approval (use with caution!)
terraform destroy -auto-approve
```

## 🔍 Key DevOps Benefits Demonstrated

1. **Repeatability**: Same code = same infrastructure everywhere
2. **Version Control**: Track all changes in Git
3. **Documentation**: Code is living documentation
4. **Consistency**: No human error in configuration
5. **Automation**: Can be integrated into CI/CD pipelines
6. **Collaboration**: Team can review infrastructure changes
7. **Rollback**: Easy to revert to previous versions

## 📚 Files Explained

- **`main.tf`**: Main resource definitions
- **`variables.tf`**: Input parameters and validation
- **`outputs.tf`**: Information extracted from created resources
- **`terraform.tfvars.example`**: Example values file (copy to `terraform.tfvars`)

## 🔧 Customization

Copy the example variables file and modify:
```bash
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your preferred values
```

Example `terraform.tfvars`:
```hcl
resource_group_name = "my-demo-rg"
location           = "West US 2"
environment        = "dev"
```

## 🚫 Common Issues

**Authentication Error**: Run `az login` and verify subscription  
**Naming Conflicts**: Storage account names must be globally unique  
**Permissions**: Ensure you have Contributor role on the subscription  
**Provider Errors**: Run `terraform init -upgrade` to update providers