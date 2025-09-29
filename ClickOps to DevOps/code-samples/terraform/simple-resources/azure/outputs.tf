# Outputs for Azure Simple Resource Deployment
# This demonstrates how to extract important information from deployed resources
# ClickOps Problem: Have to manually note down resource details
# DevOps Solution: Outputs are automatically available and can be used by other systems

output "resource_group_name" {
  description = "Name of the created resource group"
  value       = azurerm_resource_group.example.name
}

output "resource_group_location" {
  description = "Location of the created resource group"
  value       = azurerm_resource_group.example.location
}

output "resource_group_id" {
  description = "ID of the created resource group"
  value       = azurerm_resource_group.example.id
}

output "storage_account_name" {
  description = "Name of the created storage account"
  value       = azurerm_storage_account.example.name
}

output "storage_account_primary_endpoint" {
  description = "Primary blob endpoint of the storage account"
  value       = azurerm_storage_account.example.primary_blob_endpoint
}

output "storage_account_primary_access_key" {
  description = "Primary access key for the storage account"
  value       = azurerm_storage_account.example.primary_access_key
  sensitive   = true  # This marks the output as sensitive
}

output "storage_container_name" {
  description = "Name of the created blob container"
  value       = azurerm_storage_container.example.name
}

output "storage_container_url" {
  description = "URL of the created blob container"
  value       = "${azurerm_storage_account.example.primary_blob_endpoint}${azurerm_storage_container.example.name}"
}

# Example of computed outputs combining multiple resource attributes
output "resource_summary" {
  description = "Summary of created resources"
  value = {
    resource_group = {
      name     = azurerm_resource_group.example.name
      location = azurerm_resource_group.example.location
      id       = azurerm_resource_group.example.id
    }
    storage_account = {
      name             = azurerm_storage_account.example.name
      tier            = azurerm_storage_account.example.account_tier
      replication     = azurerm_storage_account.example.account_replication_type
      https_only      = azurerm_storage_account.example.enable_https_traffic_only
      container_name  = azurerm_storage_container.example.name
    }
    deployment_info = {
      terraform_version = terraform.version
      random_suffix    = random_string.suffix.result
      deployed_at      = timestamp()
    }
  }
}