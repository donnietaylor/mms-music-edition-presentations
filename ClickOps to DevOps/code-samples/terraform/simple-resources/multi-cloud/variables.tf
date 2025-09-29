# Variables for Multi-Cloud Storage Comparison
# This demonstrates how to manage multiple cloud providers with a single configuration

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "demo"
  
  validation {
    condition     = contains(["dev", "staging", "prod", "demo"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod, demo."
  }
}

variable "deploy_azure" {
  description = "Whether to deploy Azure resources"
  type        = bool
  default     = true
}

variable "deploy_aws" {
  description = "Whether to deploy AWS resources"
  type        = bool
  default     = true
}

variable "azure_location" {
  description = "Azure region for resource deployment"
  type        = string
  default     = "East US"
  
  validation {
    condition = contains([
      "East US", "East US 2", "West US", "West US 2", "West US 3",
      "Central US", "North Central US", "South Central US",
      "West Central US", "Canada Central", "Canada East",
      "Brazil South", "UK South", "UK West", "West Europe",
      "North Europe", "France Central", "Germany West Central",
      "Switzerland North", "Norway East", "UAE North",
      "South Africa North", "Australia East", "Australia Southeast",
      "Southeast Asia", "East Asia", "Japan East", "Japan West",
      "Korea Central", "India Central", "India South"
    ], var.azure_location)
    error_message = "Azure location must be a valid Azure region."
  }
}

variable "aws_region" {
  description = "AWS region for resource deployment"
  type        = string
  default     = "us-east-1"
  
  validation {
    condition = contains([
      "us-east-1", "us-east-2", "us-west-1", "us-west-2",
      "eu-west-1", "eu-west-2", "eu-west-3", "eu-central-1",
      "ap-southeast-1", "ap-southeast-2", "ap-northeast-1",
      "ca-central-1", "sa-east-1", "ap-south-1"
    ], var.aws_region)
    error_message = "AWS region must be a valid AWS region."
  }
}

# Local values for regional mapping and cost optimization
locals {
  # Map Azure regions to approximate AWS equivalents
  region_mapping = {
    "East US"           = "us-east-1"
    "East US 2"         = "us-east-2"
    "West US"           = "us-west-1"
    "West US 2"         = "us-west-2"
    "Central US"        = "us-east-1"
    "West Europe"       = "eu-west-1"
    "North Europe"      = "eu-west-2"
    "UK South"          = "eu-west-2"
    "Southeast Asia"    = "ap-southeast-1"
    "East Asia"         = "ap-southeast-1"
    "Japan East"        = "ap-northeast-1"
    "Australia East"    = "ap-southeast-2"
    "Canada Central"    = "ca-central-1"
    "Brazil South"      = "sa-east-1"
    "India Central"     = "ap-south-1"
  }
  
  # Use mapped region if available, otherwise use default
  recommended_aws_region = lookup(local.region_mapping, var.azure_location, var.aws_region)
  
  # Provider-specific configurations
  azure_config = {
    tier        = "Standard"
    replication = "LRS"  # Locally Redundant Storage
    https_only  = true
    min_tls     = "TLS1_2"
  }
  
  aws_config = {
    storage_class = "STANDARD"
    versioning   = true
    encryption   = "AES256"
    public_block = true
  }
  
  # Common tags for both providers
  common_tags = {
    Environment    = var.environment
    Project        = "ClickOps-to-DevOps"
    ManagedBy      = "Terraform"
    MultiCloud     = "true"
    Conference     = "MMS2025"
    CostCenter     = "Platform-Engineering"
    DeployedBy     = "terraform-demo"
  }
}