# Azure Storage Drift Scenario Example
# This example demonstrates how to create and detect configuration drift

terraform {
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

provider "azurerm" {
  features {}
}

resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

# Create a resource group for drift testing
resource "azurerm_resource_group" "drift_example" {
  name     = "rg-drift-demo-${random_string.suffix.result}"
  location = "East US"

  tags = {
    Environment     = "demo"
    Purpose         = "drift-detection"
    ManagedBy      = "Terraform"
    DriftExercise  = "true"
  }
}

# Storage account that we'll modify manually to create drift
resource "azurerm_storage_account" "drift_example" {
  name                     = "driftstorage${random_string.suffix.result}"
  resource_group_name      = azurerm_resource_group.drift_example.name
  location                 = azurerm_resource_group.drift_example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"  # We'll manually change this to create drift
  
  # These settings might be changed manually
  enable_https_traffic_only = true
  min_tls_version          = "TLS1_2"
  
  tags = {
    Environment     = "demo"
    Purpose         = "drift-detection"
    ManagedBy      = "Terraform"
    DriftExercise  = "true"
    OriginalConfig = "Standard-LRS"
  }
}

# Container that might be modified or deleted manually
resource "azurerm_storage_container" "drift_example" {
  name                  = "drift-container"
  storage_account_name  = azurerm_storage_account.drift_example.name
  container_access_type = "private"  # Might be changed to "blob" manually
}

# Network rules that are commonly modified manually
resource "azurerm_storage_account_network_rules" "drift_example" {
  storage_account_id = azurerm_storage_account.drift_example.id

  default_action = "Allow"  # Commonly changed to "Deny" for security
  bypass         = ["Metrics", "AzureServices"]
  
  # IP rules that might be added manually
  ip_rules = [
    # "203.0.113.0/24",  # Might be added manually
  ]
}

# Outputs to help with drift detection testing
output "drift_test_info" {
  description = "Information for testing drift scenarios"
  value = {
    resource_group_name   = azurerm_resource_group.drift_example.name
    storage_account_name  = azurerm_storage_account.drift_example.name
    container_name        = azurerm_storage_container.drift_example.name
    
    # Commands to manually create drift
    manual_changes = {
      change_replication = "az storage account update --name ${azurerm_storage_account.drift_example.name} --resource-group ${azurerm_resource_group.drift_example.name} --sku Standard_GRS"
      change_container_access = "az storage container set-permission --name ${azurerm_storage_container.drift_example.name} --account-name ${azurerm_storage_account.drift_example.name} --public-access blob"
      add_tag = "az resource tag --resource-group ${azurerm_resource_group.drift_example.name} --name ${azurerm_storage_account.drift_example.name} --resource-type 'Microsoft.Storage/storageAccounts' --tags ManualChange=true"
      delete_container = "az storage container delete --name ${azurerm_storage_container.drift_example.name} --account-name ${azurerm_storage_account.drift_example.name}"
    }
    
    # Commands to detect drift
    drift_detection = {
      terraform_plan = "terraform plan"
      terraform_refresh = "terraform refresh"
      terraform_show = "terraform show"
      check_azure_state = "az storage account show --name ${azurerm_storage_account.drift_example.name} --resource-group ${azurerm_resource_group.drift_example.name}"
    }
  }
}