# Remote State Backend - Azure Storage Example
# This configuration sets up Azure Storage as a remote backend for Terraform state
# This enables team collaboration and prevents state file conflicts

terraform {
  required_version = ">= 1.0"
  
  # Remote backend configuration for Azure Storage
  # This MUST be configured after creating the storage account
  backend "azurerm" {
    # These values should be provided via CLI or environment variables
    # terraform init -backend-config="storage_account_name=mystorageaccount"
    
    # storage_account_name = "terraformstateXXXXXX"  # Created by setup script
    # container_name       = "terraform-state"
    # key                 = "prod.terraform.tfstate"
    # resource_group_name = "rg-terraform-state"
  }
  
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

# This configuration creates a simple resource to demonstrate remote state
resource "random_pet" "example" {
  length = 2
}

resource "azurerm_resource_group" "example" {
  name     = "rg-remote-state-demo-${random_pet.example.id}"
  location = "East US"

  tags = {
    Purpose       = "Remote State Demo"
    ManagedBy     = "Terraform"
    StateLocation = "Azure Storage"
    Team          = "Platform Engineering"
  }
}

resource "azurerm_storage_account" "example" {
  name                     = "demo${replace(random_pet.example.id, "-", "")}"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    Purpose       = "Remote State Demo"
    ManagedBy     = "Terraform"
    StateLocation = "Azure Storage"
  }
}

# Output information about where the state is stored
output "remote_state_info" {
  description = "Information about the remote state configuration"
  value = {
    backend_type           = "azurerm"
    state_resource_group   = "Check your backend configuration"
    state_storage_account  = "Check your backend configuration"
    state_container        = "Check your backend configuration"
    state_key             = "Check your backend configuration"
    demo_resource_group   = azurerm_resource_group.example.name
    demo_storage_account  = azurerm_storage_account.example.name
  }
}

# Example of data that would be sensitive in state file
resource "azurerm_key_vault" "example" {
  name                = "kv-${replace(random_pet.example.id, "-", "")}"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  # This demonstrates why remote state security is important
  # Key Vault access policies contain sensitive tenant/object IDs
  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    secret_permissions = [
      "Get",
      "List",
      "Set",
      "Delete",
    ]
  }

  tags = {
    Purpose       = "Remote State Demo"
    ManagedBy     = "Terraform"
    StateLocation = "Azure Storage"
    Contains      = "Sensitive Data"
  }
}

data "azurerm_client_config" "current" {}