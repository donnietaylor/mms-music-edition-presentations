# Terraform Installation Guide

Transform from clicking in web portals to Infrastructure as Code with Terraform!

## 🔧 Installation Methods

### Windows

#### Option 1: Chocolatey (Recommended)
```powershell
# Install Chocolatey if not already installed
# Then install Terraform
choco install terraform

# Verify installation
terraform --version
```

#### Option 2: Manual Download
```powershell
# Download from https://www.terraform.io/downloads.html
# Extract to C:\terraform\
# Add C:\terraform to PATH environment variable

# Verify in PowerShell
terraform --version
```

### macOS

#### Option 1: Homebrew (Recommended)
```bash
# Install Terraform
brew install terraform

# Verify installation
terraform --version
```

#### Option 2: Manual Download
```bash
# Download from https://www.terraform.io/downloads.html
# Extract to /usr/local/bin/
sudo mv terraform /usr/local/bin/

# Verify installation
terraform --version
```

### Linux (Ubuntu/Debian)

#### Option 1: Package Manager
```bash
# Add HashiCorp GPG key
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -

# Add HashiCorp repository
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"

# Install Terraform
sudo apt-get update && sudo apt-get install terraform

# Verify installation
terraform --version
```

#### Option 2: Manual Download
```bash
# Download and install
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Verify installation
terraform --version
```

## 🔄 Version Management

### tfenv (Terraform Version Manager)

Install tfenv to manage multiple Terraform versions:

```bash
# macOS with Homebrew
brew install tfenv

# List available versions
tfenv list-remote

# Install specific version
tfenv install 1.6.0

# Use specific version
tfenv use 1.6.0

# Set default version
tfenv use default 1.6.0
```

## 🏁 First Steps After Installation

### 1. Verify Installation
```bash
$ terraform --version
Terraform v1.6.0
on darwin_amd64
```

### 2. Enable Tab Completion
```bash
# For Bash
terraform -install-autocomplete

# For PowerShell (Windows)
terraform -install-autocomplete
```

### 3. Create Your First Configuration

Create a file named `main.tf`:
```hcl
terraform {
  required_version = ">= 1.0"
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1"
    }
  }
}

resource "random_pet" "example" {
  length = 2
}

output "pet_name" {
  value = random_pet.example.id
}
```

### 4. Initialize and Apply
```bash
# Initialize Terraform
terraform init

# Preview changes
terraform plan

# Apply changes
terraform apply
```

## 🚀 Next Steps

- Try the [simple-resources](../simple-resources/) examples
- Set up your first [cloud provider authentication](../simple-resources/azure/)
- Learn about [state management](../state-management/)

## 🔍 Troubleshooting

### Common Issues

**Issue**: Command not found  
**Solution**: Ensure Terraform is in your PATH environment variable

**Issue**: Permission denied (Linux/macOS)  
**Solution**: Use `sudo` for installation or check file permissions

**Issue**: Version conflicts  
**Solution**: Use tfenv to manage multiple versions

## 📚 Additional Resources

- [Official Terraform Documentation](https://www.terraform.io/docs)
- [Terraform Registry](https://registry.terraform.io/)
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/)