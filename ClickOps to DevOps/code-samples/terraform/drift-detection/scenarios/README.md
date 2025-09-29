# Drift Detection Scenarios

This directory contains practical examples for experiencing and understanding configuration drift in real scenarios.

## 🎯 Learning Objectives

After completing these scenarios, you'll understand:
- How drift occurs in real-world situations
- How to detect drift using Terraform commands
- Different types of drift and their impacts
- How to correct drift issues

## 📋 Prerequisites

- Terraform installed and configured
- Azure CLI installed and authenticated (`az login`)
- Basic understanding of Terraform and Azure resources

## 🧪 Scenario 1: Azure Storage Account Drift

### File: `azure-storage-drift.tf`

This scenario creates an Azure storage account and demonstrates common drift situations.

### Step 1: Deploy Initial Infrastructure
```bash
# Initialize and deploy
terraform init
terraform apply
```

### Step 2: Note the Initial State
```bash
# See what Terraform knows about
terraform show

# Get the storage account details
terraform output drift_test_info
```

### Step 3: Create Drift Manually

#### Option A: Change Storage Replication Type
```bash
# Get the resource names
STORAGE_ACCOUNT=$(terraform output -json drift_test_info | jq -r '.storage_account_name')
RESOURCE_GROUP=$(terraform output -json drift_test_info | jq -r '.resource_group_name')

# Manually change replication from LRS to GRS
az storage account update \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --sku Standard_GRS
```

#### Option B: Change Container Access Level
```bash
# Change container from private to public blob access
az storage container set-permission \
  --name drift-container \
  --account-name $STORAGE_ACCOUNT \
  --public-access blob
```

#### Option C: Add Manual Tags
```bash
# Add tags that aren't in Terraform configuration
az resource tag \
  --resource-group $RESOURCE_GROUP \
  --name $STORAGE_ACCOUNT \
  --resource-type 'Microsoft.Storage/storageAccounts' \
  --tags ManualChange=true EmergencyFix=applied
```

### Step 4: Detect the Drift
```bash
# This should show no changes (Terraform doesn't know about manual changes yet)
terraform plan

# Refresh state to detect changes from Azure
terraform refresh

# Now plan should show the drift
terraform plan
```

### Step 5: Analyze the Drift
```bash
# See detailed differences
terraform plan -detailed-exitcode

# Check current Azure state
az storage account show \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --query '{sku: sku.name, tags: tags, location: location}'
```

### Step 6: Handle the Drift

#### Option A: Accept the Manual Changes (Update Terraform)
```hcl
# Edit azure-storage-drift.tf
resource "azurerm_storage_account" "drift_example" {
  # ... other configuration ...
  account_replication_type = "GRS"  # Changed from "LRS"
  
  tags = {
    # ... existing tags ...
    ManualChange = "true"
    EmergencyFix = "applied"
  }
}
```

#### Option B: Revert to Terraform Configuration
```bash
# Apply Terraform configuration to fix drift
terraform apply
# This will revert the manual changes
```

### Step 7: Clean Up
```bash
terraform destroy
```

## 🔍 What You'll Observe

### Before Manual Changes
```bash
$ terraform plan
No changes. Infrastructure is up-to-date.
```

### After Manual Changes (Before Refresh)
```bash
$ terraform plan
No changes. Infrastructure is up-to-date.
# Terraform doesn't know about manual changes yet!
```

### After Refresh
```bash
$ terraform refresh
$ terraform plan
Terraform will perform the following actions:

  # azurerm_storage_account.drift_example will be updated in-place
  ~ resource "azurerm_storage_account" "drift_example" {
      ~ account_replication_type = "GRS" -> "LRS"
      ~ tags                     = {
          - "EmergencyFix"  = "applied" -> null
          - "ManualChange"  = "true" -> null
        }
    }
```

## 📊 Types of Drift Demonstrated

1. **Configuration Drift**: Storage replication type changed
2. **Metadata Drift**: Tags added/modified outside Terraform
3. **Access Control Drift**: Container permissions changed
4. **State Inconsistency**: Terraform state vs. actual Azure state

## 🚨 Real-World Scenarios

### Emergency Response
```bash
# Production issue - need to quickly change storage redundancy
# ❌ Manual approach: Change in Azure Portal
# ✅ DevOps approach: Update Terraform and apply

# Emergency hotfix
git checkout -b emergency/storage-redundancy
# Edit terraform files
git commit -m "Emergency: Increase storage redundancy to GRS"
terraform plan
terraform apply
git push && create PR
```

### Compliance Audit
```bash
# Security audit finds missing tags
# ❌ Manual approach: Add tags in portal to hundreds of resources
# ✅ DevOps approach: Update Terraform configuration

# Add compliance tags to all resources
locals {
  compliance_tags = {
    DataClassification = "internal"
    CostCenter        = "IT-Infrastructure"
    Owner            = "platform-team"
  }
}
```

## 🎓 Key Lessons

1. **Drift is Silent**: Manual changes don't trigger alerts until you run `terraform plan`
2. **Refresh is Key**: Always refresh state before planning in production
3. **Documentation Matters**: Code tells you what should exist, not what does exist
4. **Process Prevents Problems**: Good processes prevent most drift scenarios
5. **Automation Catches Issues**: Regular drift detection finds problems early

## 🔗 Next Steps

- Try the [workflows](../workflows/) examples for automated drift detection
- Learn [best practices](../best-practices/) for preventing drift
- Explore remote state management for team collaboration

## 💡 Pro Tips

- Run `terraform plan` daily in production environments
- Use `terraform plan -detailed-exitcode` in CI/CD for automated drift detection
- Always refresh state before important operations
- Keep detailed git commit messages for infrastructure changes
- Use resource tagging to identify manual changes