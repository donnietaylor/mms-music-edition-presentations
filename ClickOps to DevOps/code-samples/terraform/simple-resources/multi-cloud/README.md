# Multi-Cloud Storage Comparison

This example demonstrates how to create equivalent storage resources across Azure and AWS using a single Terraform configuration. Perfect for understanding the power of Infrastructure as Code in multi-cloud scenarios.

## 🎯 Multi-Cloud: ClickOps vs DevOps

| Manual Approach (ClickOps) | Terraform Multi-Cloud (DevOps) |
|----------------------------|--------------------------------|
| Learn two different web consoles | Single consistent configuration language |
| Different procedures for each cloud | Same terraform commands everywhere |
| Maintain separate documentation | Code documents both environments |
| Manual consistency checks | Automated resource comparison |
| Cloud-specific knowledge silos | Unified infrastructure management |
| Difficult to switch providers | Easy provider migration |

## 📋 What This Example Creates

### Azure Resources
- **Resource Group**: Container for Azure resources
- **Storage Account**: Blob storage with security settings
- **Storage Container**: Private container for files

### AWS Resources
- **S3 Bucket**: Object storage with versioning
- **Encryption Configuration**: Server-side encryption
- **Public Access Block**: Security restrictions

### Feature Comparison
The example outputs show side-by-side comparisons of:
- Storage capacity and durability
- Pricing models
- Availability guarantees
- Access tier options
- Integration capabilities

## 📋 Prerequisites

### Required Tools
```bash
# Terraform
terraform --version

# Azure CLI (if deploying Azure resources)
az --version

# AWS CLI (if deploying AWS resources) 
aws --version

# jq for JSON processing (optional, for pretty output)
jq --version
```

### Authentication Setup

#### Azure Authentication
```bash
# Interactive login
az login

# Service principal (for automation)
export ARM_CLIENT_ID="your-client-id"
export ARM_CLIENT_SECRET="your-client-secret"
export ARM_SUBSCRIPTION_ID="your-subscription-id"
export ARM_TENANT_ID="your-tenant-id"
```

#### AWS Authentication
```bash
# Configure AWS credentials
aws configure

# Or use environment variables
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

## 🚀 Deployment Options

### Option 1: Deploy Both Clouds (Full Comparison)
```bash
# Initialize Terraform
terraform init

# Plan deployment for both clouds
terraform plan

# Deploy to both Azure and AWS
terraform apply
```

### Option 2: Azure Only
```bash
# Deploy only Azure resources
terraform apply -var="deploy_aws=false"
```

### Option 3: AWS Only
```bash
# Deploy only AWS resources
terraform apply -var="deploy_azure=false"
```

### Option 4: Custom Regions
```bash
# Deploy to specific regions
terraform apply \
  -var="azure_location=West Europe" \
  -var="aws_region=eu-west-1" \
  -var="environment=prod"
```

## 🔍 Understanding the Results

### View the Comparison
```bash
# See detailed comparison of resources
terraform output multi_cloud_comparison

# Pretty print with jq
terraform output -json multi_cloud_comparison | jq
```

### Usage Examples
```bash
# Get commands for interacting with storage
terraform output usage_examples

# See cost estimates
terraform output estimated_monthly_costs
```

### Test Storage Upload

#### Azure
```bash
# Get Azure storage account name
AZURE_STORAGE_ACCOUNT=$(terraform output -json multi_cloud_comparison | jq -r '.azure.storage_account.name')

# Create test file
echo "Hello from Azure!" > test-azure.txt

# Upload to Azure (requires storage key or SAS token)
az storage blob upload \
  --account-name $AZURE_STORAGE_ACCOUNT \
  --container-name multicloud-container \
  --file test-azure.txt \
  --name test-azure.txt
```

#### AWS
```bash
# Get AWS S3 bucket name
AWS_BUCKET=$(terraform output -json multi_cloud_comparison | jq -r '.aws.s3_bucket.name')

# Create test file
echo "Hello from AWS!" > test-aws.txt

# Upload to S3
aws s3 cp test-aws.txt s3://$AWS_BUCKET/test-aws.txt
```

## 📊 Feature Comparison Analysis

### Storage Models
- **Azure Blob Storage**: Account → Container → Blob hierarchy
- **AWS S3**: Bucket → Object flat structure (folders are prefixes)

### Security Defaults
- **Azure**: Private by default, explicit security settings
- **AWS**: Public block must be explicitly configured

### Pricing Models
- **Azure**: Storage tier-based (Hot, Cool, Archive)
- **AWS**: Storage class-based (Standard, IA, Glacier, Deep Archive)

### Access Patterns
```bash
# Azure: Hierarchical access
https://storageaccount.blob.core.windows.net/container/blob

# AWS: Flat with prefixes
https://bucket.s3.region.amazonaws.com/object-key
```

## 💰 Cost Comparison

Run the example to see estimated costs:
```bash
terraform output estimated_monthly_costs
```

### Factors Affecting Cost
1. **Storage Amount**: Both charge per GB stored
2. **Access Frequency**: Hot vs Cool (Azure) or Standard vs IA (AWS)
3. **Data Transfer**: Egress charges apply to both
4. **Transactions**: Different pricing per operation
5. **Region**: Costs vary by geographic location

## 🔄 Migration Scenarios

### Azure to AWS Migration
```bash
# 1. Deploy AWS resources alongside Azure
terraform apply -var="deploy_aws=true"

# 2. Migrate data using cloud-native tools
# Azure: azcopy, AWS: aws s3 sync

# 3. Update applications to use AWS endpoints

# 4. Remove Azure resources
terraform apply -var="deploy_azure=false"
```

### AWS to Azure Migration
```bash
# 1. Deploy Azure resources alongside AWS
terraform apply -var="deploy_azure=true"

# 2. Migrate data
# 3. Update applications
# 4. Remove AWS resources
terraform apply -var="deploy_aws=false"
```

## 🎯 Real-World Use Cases

### 1. Disaster Recovery
```hcl
# Primary in Azure, backup in AWS
deploy_azure = true
deploy_aws   = true
environment  = "prod"
```

### 2. Cost Optimization
```bash
# Compare costs across regions
terraform plan -var="azure_location=West Europe" -var="aws_region=eu-west-1"
terraform plan -var="azure_location=East US" -var="aws_region=us-east-1"
```

### 3. Compliance Requirements
```bash
# Deploy only in specific regions for data sovereignty
terraform apply \
  -var="azure_location=Germany West Central" \
  -var="aws_region=eu-central-1"
```

### 4. Vendor Risk Mitigation
```bash
# Maintain presence in multiple clouds
terraform apply \
  -var="deploy_azure=true" \
  -var="deploy_aws=true" \
  -var="environment=prod"
```

## 🧹 Cleanup

### Remove All Resources
```bash
# Destroy all resources in both clouds
terraform destroy
```

### Selective Cleanup
```bash
# Remove only AWS resources
terraform apply -var="deploy_aws=false"

# Remove only Azure resources  
terraform apply -var="deploy_azure=false"
```

## 🔧 Customization

### Environment-Specific Configuration
```bash
# Copy example variables
cp terraform.tfvars.example terraform.tfvars

# Edit for your needs
vim terraform.tfvars
```

### Example terraform.tfvars
```hcl
environment     = "staging"
deploy_azure    = true
deploy_aws      = true
azure_location  = "West US 2"
aws_region      = "us-west-2"
```

## 📚 Learning Outcomes

After completing this example, you'll understand:

1. **Multi-Cloud Patterns**: How to manage resources across multiple cloud providers
2. **Provider Differences**: Similarities and differences between Azure and AWS
3. **Resource Mapping**: How equivalent services compare across clouds
4. **Cost Considerations**: Pricing model differences and optimization strategies
5. **Migration Planning**: How to approach cloud-to-cloud migrations
6. **Terraform Power**: Single configuration managing multiple providers

## 🔍 Advanced Scenarios

### Cross-Cloud Data Replication
```hcl
# Example: Sync data between Azure and AWS storage
resource "null_resource" "data_sync" {
  provisioner "local-exec" {
    command = <<-EOT
      # Sync from Azure to AWS
      azcopy copy "https://${azurerm_storage_account.comparison.name}.blob.core.windows.net/${azurerm_storage_container.comparison.name}" \
                  "s3://${aws_s3_bucket.comparison.bucket}/" --recursive
    EOT
  }
}
```

### Multi-Cloud Load Balancing
```hcl
# Route traffic between clouds based on latency/availability
# (Would require additional DNS and load balancing resources)
```

## 💡 Pro Tips

1. **Start Small**: Begin with one cloud, then expand
2. **Use Modules**: Create reusable modules for each cloud
3. **Tag Everything**: Consistent tagging across all clouds
4. **Monitor Costs**: Set up billing alerts in both clouds
5. **Automate Compliance**: Use cloud-native policy tools
6. **Document Differences**: Maintain a comparison matrix
7. **Test Regularly**: Verify resources in both clouds work as expected

## 🚫 Common Pitfalls

- **Authentication Mix-ups**: Ensure correct credentials for each provider
- **Resource Naming**: Different naming requirements per cloud
- **Region Mismatch**: Verify regions support required services
- **Cost Surprises**: Understand data transfer charges between clouds
- **Feature Parity**: Not all features available in all clouds/regions