# Multi-Cloud Storage Comparison Example
# This demonstrates how to create similar storage resources across different cloud providers
# Shows the power of Terraform's multi-cloud capabilities

terraform {
  required_version = ">= 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1"
    }
  }
}

# Configure providers
provider "azurerm" {
  features {}
  # Uncomment and configure if you want to deploy Azure resources
  # skip_provider_registration = true
}

provider "aws" {
  region = var.aws_region
  # Uncomment and configure if you want to deploy AWS resources
  # skip_credentials_validation = true
  # skip_metadata_api_check     = true
  # skip_region_validation      = true
}

# Generate unique suffix for resource naming
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

# Local values for consistent naming and tagging
locals {
  common_tags = {
    Environment   = var.environment
    Project       = "ClickOps-to-DevOps"
    ManagedBy     = "Terraform"
    MultiCloud    = "true"
    Conference    = "MMS2025"
  }
  
  naming_prefix = "${var.environment}-multicloud-${random_string.suffix.result}"
}

#
# AZURE RESOURCES
# Same functionality as AWS but using Azure services
#

resource "azurerm_resource_group" "comparison" {
  count = var.deploy_azure ? 1 : 0
  
  name     = "rg-${local.naming_prefix}"
  location = var.azure_location

  tags = merge(local.common_tags, {
    CloudProvider = "Azure"
    Purpose      = "Multi-cloud storage comparison"
  })
}

resource "azurerm_storage_account" "comparison" {
  count = var.deploy_azure ? 1 : 0
  
  name                     = replace("sa${local.naming_prefix}", "-", "")
  resource_group_name      = azurerm_resource_group.comparison[0].name
  location                 = azurerm_resource_group.comparison[0].location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  
  # Security settings (equivalent to AWS S3 security)
  allow_nested_items_to_be_public = false
  enable_https_traffic_only       = true
  min_tls_version                 = "TLS1_2"

  tags = merge(local.common_tags, {
    CloudProvider = "Azure"
    StorageType   = "Blob"
    SecurityLevel = "High"
  })
}

resource "azurerm_storage_container" "comparison" {
  count = var.deploy_azure ? 1 : 0
  
  name                  = "multicloud-container"
  storage_account_name  = azurerm_storage_account.comparison[0].name
  container_access_type = "private"
}

#
# AWS RESOURCES  
# Same functionality as Azure but using AWS services
#

resource "aws_s3_bucket" "comparison" {
  count = var.deploy_aws ? 1 : 0
  
  bucket = "${local.naming_prefix}-s3-bucket"

  tags = merge(local.common_tags, {
    CloudProvider = "AWS"
    Purpose       = "Multi-cloud storage comparison"
    StorageType   = "S3"
  })
}

resource "aws_s3_bucket_versioning" "comparison" {
  count = var.deploy_aws ? 1 : 0
  
  bucket = aws_s3_bucket.comparison[0].id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "comparison" {
  count = var.deploy_aws ? 1 : 0
  
  bucket = aws_s3_bucket.comparison[0].id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "comparison" {
  count = var.deploy_aws ? 1 : 0
  
  bucket = aws_s3_bucket.comparison[0].id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

#
# COMPARISON OUTPUTS
# Show the equivalent resources and their differences
#

output "multi_cloud_comparison" {
  description = "Comparison of equivalent resources across cloud providers"
  value = {
    azure = var.deploy_azure ? {
      resource_group = {
        name     = azurerm_resource_group.comparison[0].name
        location = azurerm_resource_group.comparison[0].location
        id       = azurerm_resource_group.comparison[0].id
      }
      storage_account = {
        name         = azurerm_storage_account.comparison[0].name
        tier         = azurerm_storage_account.comparison[0].account_tier
        replication  = azurerm_storage_account.comparison[0].account_replication_type
        https_only   = azurerm_storage_account.comparison[0].enable_https_traffic_only
        endpoint     = azurerm_storage_account.comparison[0].primary_blob_endpoint
      }
      container = {
        name   = azurerm_storage_container.comparison[0].name
        access = azurerm_storage_container.comparison[0].container_access_type
      }
      equivalent_aws_services = {
        resource_group  = "Not applicable (AWS doesn't have resource groups)"
        storage_account = "AWS S3 Bucket"
        container      = "S3 Bucket (containers are implied)"
      }
    } : "Azure resources not deployed"
    
    aws = var.deploy_aws ? {
      s3_bucket = {
        name         = aws_s3_bucket.comparison[0].bucket
        region       = aws_s3_bucket.comparison[0].region
        arn          = aws_s3_bucket.comparison[0].arn
        versioning   = aws_s3_bucket_versioning.comparison[0].versioning_configuration[0].status
        encryption   = "AES256"
        public_block = "Enabled"
      }
      equivalent_azure_services = {
        s3_bucket             = "Azure Storage Account + Container"
        versioning           = "Azure Storage Account versioning"
        encryption           = "Azure Storage Account encryption"
        public_access_block  = "Azure Storage Account public access settings"
      }
    } : "AWS resources not deployed"
    
    feature_comparison = {
      storage_capacity = {
        azure = "Virtually unlimited (Blob Storage)"
        aws   = "Virtually unlimited (S3)"
      }
      pricing_model = {
        azure = "Pay per GB stored + transactions"
        aws   = "Pay per GB stored + requests"
      }
      availability = {
        azure = "99.9% (LRS) to 99.99% (RA-GRS)"
        aws   = "99.999999999% (11 9's) durability"
      }
      access_patterns = {
        azure = "Hot, Cool, Archive tiers"
        aws   = "Standard, IA, Glacier, Deep Archive"
      }
      integration = {
        azure = "Native Azure service integration"
        aws   = "Native AWS service integration"
      }
    }
  }
}

# Practical usage examples
output "usage_examples" {
  description = "Example commands for using the storage resources"
  value = {
    azure = var.deploy_azure ? {
      upload_file = "az storage blob upload --account-name ${azurerm_storage_account.comparison[0].name} --container-name ${azurerm_storage_container.comparison[0].name} --file local-file.txt --name remote-file.txt"
      list_blobs  = "az storage blob list --account-name ${azurerm_storage_account.comparison[0].name} --container-name ${azurerm_storage_container.comparison[0].name}"
      download    = "az storage blob download --account-name ${azurerm_storage_account.comparison[0].name} --container-name ${azurerm_storage_container.comparison[0].name} --name remote-file.txt --file downloaded-file.txt"
    } : null
    
    aws = var.deploy_aws ? {
      upload_file = "aws s3 cp local-file.txt s3://${aws_s3_bucket.comparison[0].bucket}/remote-file.txt"
      list_objects = "aws s3 ls s3://${aws_s3_bucket.comparison[0].bucket}/"
      download    = "aws s3 cp s3://${aws_s3_bucket.comparison[0].bucket}/remote-file.txt downloaded-file.txt"
    } : null
  }
}

# Cost estimation (rough approximation)
output "estimated_monthly_costs" {
  description = "Rough monthly cost estimates for minimal usage"
  value = {
    azure = {
      storage_account = "$0.02 per GB (Hot tier)"
      transactions   = "$0.004 per 10,000 transactions"
      data_transfer  = "$0.087 per GB (outbound)"
      minimum_cost   = "~$0.01/month for minimal usage"
    }
    aws = {
      s3_standard    = "$0.023 per GB"
      requests      = "$0.004 per 1,000 PUT requests"
      data_transfer = "$0.09 per GB (outbound)"
      minimum_cost  = "~$0.01/month for minimal usage"
    }
    note = "Costs vary by region and actual usage. These are rough estimates for comparison."
  }
}