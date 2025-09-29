# Azure Simple Resource Deployment Example
# This demonstrates creating basic Azure resources with Terraform
# instead of clicking through the Azure Portal

terraform {
  required_version = ">= 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1"
    }
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
}

# Generate a random suffix for unique naming
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

# Create a resource group
# ClickOps: Portal -> Resource groups -> Create -> Fill form -> Create
# DevOps: Define once, deploy anywhere, track in git
resource "azurerm_resource_group" "example" {
  name     = "${var.resource_group_name}-${random_string.suffix.result}"
  location = var.location

  tags = {
    Environment = var.environment
    Purpose     = "ClickOps to DevOps Demo"
    ManagedBy   = "Terraform"
    CreatedBy   = "MMS2025-Demo"
  }
}

# Create a storage account
# ClickOps: Portal -> Storage accounts -> Create -> Multiple pages of forms
# DevOps: Consistent configuration, version controlled, reproducible
resource "azurerm_storage_account" "example" {
  name                     = "storage${random_string.suffix.result}"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  
  # Security settings that might be forgotten in manual deployment
  allow_nested_items_to_be_public = false
  enable_https_traffic_only       = true
  min_tls_version                 = "TLS1_2"

  tags = {
    Environment = var.environment
    Purpose     = "ClickOps to DevOps Demo"
    ManagedBy   = "Terraform"
    CreatedBy   = "MMS2025-Demo"
  }
}

# Create a blob container
# ClickOps: Navigate to storage account -> Containers -> New container
# DevOps: Defined alongside storage account, consistent naming
resource "azurerm_storage_container" "example" {
  name                  = "demo-container"
  storage_account_name  = azurerm_storage_account.example.name
  container_access_type = "private"
}