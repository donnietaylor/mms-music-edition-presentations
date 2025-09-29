#!/bin/bash
# Setup Azure Storage Backend for Terraform Remote State
# This script creates the Azure resources needed for remote state storage

set -e  # Exit on any error

# Configuration variables
RESOURCE_GROUP_NAME="rg-terraform-state"
STORAGE_ACCOUNT_NAME="terraformstate$(openssl rand -hex 4)"
CONTAINER_NAME="terraform-state"
LOCATION="East US"

echo "🚀 Setting up Azure Storage backend for Terraform remote state..."

# Check if Azure CLI is installed and user is logged in
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Please install it first."
    echo "   https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Check if user is logged in
if ! az account show &> /dev/null; then
    echo "❌ Not logged into Azure. Please run: az login"
    exit 1
fi

echo "✅ Azure CLI is installed and authenticated"

# Get current subscription info
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
SUBSCRIPTION_NAME=$(az account show --query name -o tsv)
echo "📋 Using subscription: $SUBSCRIPTION_NAME ($SUBSCRIPTION_ID)"

# Create resource group
echo "🏗️  Creating resource group: $RESOURCE_GROUP_NAME"
az group create \
    --name "$RESOURCE_GROUP_NAME" \
    --location "$LOCATION" \
    --tags \
        Purpose="Terraform Remote State" \
        ManagedBy="Setup Script" \
        CreatedBy="ClickOps-to-DevOps-Demo"

# Create storage account
echo "💾 Creating storage account: $STORAGE_ACCOUNT_NAME"
az storage account create \
    --name "$STORAGE_ACCOUNT_NAME" \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --location "$LOCATION" \
    --sku Standard_LRS \
    --encryption-services blob \
    --https-only true \
    --min-tls-version TLS1_2 \
    --tags \
        Purpose="Terraform Remote State" \
        ManagedBy="Setup Script" \
        CreatedBy="ClickOps-to-DevOps-Demo"

# Get storage account key
echo "🔑 Getting storage account access key..."
ACCOUNT_KEY=$(az storage account keys list \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --account-name "$STORAGE_ACCOUNT_NAME" \
    --query '[0].value' -o tsv)

# Create blob container
echo "📦 Creating blob container: $CONTAINER_NAME"
az storage container create \
    --name "$CONTAINER_NAME" \
    --account-name "$STORAGE_ACCOUNT_NAME" \
    --account-key "$ACCOUNT_KEY" \
    --public-access off

echo ""
echo "✅ Azure Storage backend setup complete!"
echo ""
echo "📝 Backend Configuration:"
echo "========================="
echo "Resource Group:    $RESOURCE_GROUP_NAME"
echo "Storage Account:   $STORAGE_ACCOUNT_NAME"
echo "Container:         $CONTAINER_NAME"
echo "Subscription ID:   $SUBSCRIPTION_ID"
echo ""

echo "🔧 To use this backend, update your terraform block:"
echo "terraform {"
echo "  backend \"azurerm\" {"
echo "    resource_group_name  = \"$RESOURCE_GROUP_NAME\""
echo "    storage_account_name = \"$STORAGE_ACCOUNT_NAME\""
echo "    container_name       = \"$CONTAINER_NAME\""
echo "    key                 = \"terraform.tfstate\""
echo "  }"
echo "}"
echo ""

echo "🏃 Or initialize with command line parameters:"
echo "terraform init \\"
echo "  -backend-config=\"resource_group_name=$RESOURCE_GROUP_NAME\" \\"
echo "  -backend-config=\"storage_account_name=$STORAGE_ACCOUNT_NAME\" \\"
echo "  -backend-config=\"container_name=$CONTAINER_NAME\" \\"
echo "  -backend-config=\"key=terraform.tfstate\""
echo ""

echo "🌍 Environment variables for authentication:"
echo "export ARM_SUBSCRIPTION_ID=\"$SUBSCRIPTION_ID\""
echo "export ARM_CLIENT_ID=\"<your-client-id>\""
echo "export ARM_CLIENT_SECRET=\"<your-client-secret>\""
echo "export ARM_TENANT_ID=\"<your-tenant-id>\""
echo ""

echo "💡 Pro tip: Save this configuration in a backend.hcl file:"
cat > backend.hcl << EOF
resource_group_name  = "$RESOURCE_GROUP_NAME"
storage_account_name = "$STORAGE_ACCOUNT_NAME"
container_name       = "$CONTAINER_NAME"
key                 = "terraform.tfstate"
EOF

echo "✅ Created backend.hcl file for easy initialization"
echo "   Use with: terraform init -backend-config=backend.hcl"
echo ""

echo "🧹 To clean up later, run:"
echo "az group delete --name $RESOURCE_GROUP_NAME --yes --no-wait"
echo ""
echo "🎉 Setup complete! You can now use remote state with your Terraform configurations."