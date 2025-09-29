# Variables for AWS Simple Resource Deployment
# This file demonstrates how to make Terraform configurations reusable
# ClickOps Problem: Each manual deployment might use different values
# DevOps Solution: Consistent, documented, and version-controlled parameters

variable "aws_region" {
  description = "AWS region where resources will be deployed"
  type        = string
  default     = "us-east-1"
  
  validation {
    condition = contains([
      "us-east-1", "us-east-2", "us-west-1", "us-west-2",
      "eu-west-1", "eu-west-2", "eu-west-3", "eu-central-1",
      "ap-southeast-1", "ap-southeast-2", "ap-northeast-1",
      "ca-central-1", "sa-east-1", "ap-south-1"
    ], var.aws_region)
    error_message = "AWS region must be a valid region."
  }
}

variable "bucket_name" {
  description = "Base name for the S3 bucket (random suffix will be added)"
  type        = string
  default     = "clickops-to-devops-demo"
  
  validation {
    condition     = can(regex("^[a-z0-9-]+$", var.bucket_name)) && length(var.bucket_name) >= 3 && length(var.bucket_name) <= 40
    error_message = "Bucket name must be lowercase, contain only letters, numbers, and hyphens, and be 3-40 characters long."
  }
}

variable "environment" {
  description = "Environment tag for resources (dev, staging, prod)"
  type        = string
  default     = "demo"
  
  validation {
    condition     = contains(["dev", "staging", "prod", "demo"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod, demo."
  }
}

variable "enable_versioning" {
  description = "Enable versioning on the S3 bucket"
  type        = bool
  default     = true
}

variable "log_retention_days" {
  description = "Number of days to retain CloudWatch logs"
  type        = number
  default     = 7
  
  validation {
    condition     = contains([1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, 3653], var.log_retention_days)
    error_message = "Log retention must be a valid CloudWatch log retention value."
  }
}

# Local values for computed configurations
locals {
  # Common tags applied to all resources
  common_tags = {
    Environment   = var.environment
    ManagedBy     = "Terraform"
    Project       = "ClickOps-to-DevOps"
    Conference    = "MMS2025"
    Presentation  = "Infrastructure-as-Code-Demo"
  }
  
  # AWS naming conventions
  naming_prefix = "${var.environment}-clickops-devops"
  
  # Bucket configuration
  bucket_full_name = "${var.bucket_name}-${var.environment}"
}

# Data sources for dynamic configuration
data "aws_caller_identity" "current" {}

data "aws_availability_zones" "available" {
  state = "available"
}