# Variables for Azure Simple Resource Deployment
# This file demonstrates how to make Terraform configurations reusable
# ClickOps Problem: Each manual deployment might use different values
# DevOps Solution: Consistent, documented, and version-controlled parameters

variable "resource_group_name" {
  description = "Name of the Azure Resource Group"
  type        = string
  default     = "rg-clickops-to-devops"
  
  validation {
    condition     = length(var.resource_group_name) > 0 && length(var.resource_group_name) <= 50
    error_message = "Resource group name must be between 1 and 50 characters."
  }
}

variable "location" {
  description = "Azure region where resources will be deployed"
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
    ], var.location)
    error_message = "Location must be a valid Azure region."
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

# Optional: Define locals for computed values
locals {
  # Common tags that will be applied to all resources
  common_tags = {
    Environment   = var.environment
    ManagedBy     = "Terraform"
    Project       = "ClickOps-to-DevOps"
    Conference    = "MMS2025"
    Presentation  = "Infrastructure-as-Code-Demo"
  }
  
  # Naming convention for consistent resource naming
  naming_prefix = "${var.environment}-clickops-devops"
}