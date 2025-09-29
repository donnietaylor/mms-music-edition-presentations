# Terraform Drift Detection and Management

Learn how to identify and handle configuration drift - the silent killer of infrastructure consistency.

## 🎯 What is Configuration Drift?

Configuration drift occurs when the actual state of your infrastructure differs from what's defined in your Terraform configuration. This is a common problem in ClickOps environments but is easily managed with proper DevOps practices.

### ClickOps vs DevOps: Drift Management

| Manual Operations (ClickOps) | Terraform DevOps |
|------------------------------|------------------|
| Drift goes unnoticed for months | Drift detected on every plan |
| Manual fixes create more drift | Automated correction workflows |
| Documentation gets out of sync | Code is always the truth |
| "Works on my machine" problems | Consistent infrastructure everywhere |
| Emergency fixes bypass process | All changes go through code review |
| No audit trail of changes | Full Git history of all modifications |

## 📁 Examples Structure

### [scenarios/](./scenarios/)
Common drift scenarios and how to identify them
- Manual resource modifications
- Tag changes outside of Terraform
- Resource deletions and additions
- Configuration parameter changes

### [workflows/](./workflows/)
Automated drift detection and correction workflows
- CI/CD pipeline integration
- Scheduled drift detection
- Automated alerts and notifications
- Correction workflows

### [best-practices/](./best-practices/)
Best practices for preventing and managing drift
- Preventive measures
- Monitoring and alerting
- Team processes and governance
- Documentation and training

## 🔍 Types of Drift

### 1. Configuration Drift
Changes to resource properties outside of Terraform:
```bash
# Terraform knows about Standard_LRS storage
# But someone manually changed it to Standard_GRS
terraform plan
# Shows: account_replication_type: "Standard_LRS" -> "Standard_GRS"
```

### 2. Resource Drift
Resources added or removed outside of Terraform:
```bash
# Someone manually created additional storage containers
terraform plan
# Doesn't show the manually created resources
```

### 3. State Drift
Terraform state becomes inconsistent with reality:
```bash
# State file says resource exists, but it was manually deleted
terraform plan
# Shows: Error: resource not found
```

## 🔧 Drift Detection Commands

### Basic Drift Detection
```bash
# Refresh state from real infrastructure
terraform refresh

# See what changes Terraform would make
terraform plan

# Show detailed differences
terraform plan -detailed-exitcode

# Check if configuration matches state
terraform validate
```

### Advanced Drift Analysis
```bash
# Show current state
terraform show

# List all resources in state
terraform state list

# Show specific resource details
terraform state show azurerm_storage_account.example

# Compare state with configuration
terraform plan -out=tfplan
terraform show -json tfplan | jq '.resource_changes[]'
```

## 🚨 Common Drift Scenarios

### 1. Manual Portal Changes
**Problem**: Someone changes resource tags in Azure Portal
**Detection**: `terraform plan` shows tag differences
**Solution**: Update Terraform configuration or revert manual changes

### 2. Emergency Fixes
**Problem**: Production issue fixed by manually scaling resources
**Detection**: `terraform plan` shows instance count differences  
**Solution**: Update configuration to match or plan rollback

### 3. Compliance Changes
**Problem**: Security team manually enables encryption
**Detection**: `terraform plan` shows encryption setting changes
**Solution**: Update Terraform to include security requirements

### 4. Resource Deletion
**Problem**: Someone accidentally deletes resources in console
**Detection**: `terraform plan` shows resources to recreate
**Solution**: Run `terraform apply` to recreate resources

## 🔄 Drift Correction Workflows

### 1. Automated Detection
```bash
#!/bin/bash
# drift-check.sh - Run in CI/CD pipeline

terraform init
terraform plan -detailed-exitcode

case $? in
  0)
    echo "✅ No drift detected"
    ;;
  1)
    echo "❌ Error running terraform plan"
    exit 1
    ;;
  2)
    echo "⚠️  Configuration drift detected"
    # Send alert to team
    # Create GitHub issue
    # Update monitoring dashboard
    ;;
esac
```

### 2. Correction Options
When drift is detected, you have options:

#### Option A: Update Configuration (Adopt Manual Changes)
```hcl
# Update Terraform to match manual changes
resource "azurerm_storage_account" "example" {
  # Change configuration to match current state
  account_replication_type = "Standard_GRS"  # Was manually changed
}
```

#### Option B: Revert to Configuration (Fix Drift)
```bash
# Apply Terraform configuration to fix drift
terraform apply
# This reverts manual changes back to configuration
```

#### Option C: Import and Align
```bash
# Import manually created resources
terraform import azurerm_storage_container.new /subscriptions/.../containers/manual-container

# Then update configuration to manage it
```

## 📊 Monitoring and Alerting

### Drift Detection Pipeline
```yaml
# .github/workflows/drift-detection.yml
name: Drift Detection
on:
  schedule:
    - cron: '0 8 * * *'  # Daily at 8 AM

jobs:
  detect-drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
      - name: Check for Drift
        run: |
          terraform init
          terraform plan -detailed-exitcode
        continue-on-error: true
      - name: Alert on Drift
        if: failure()
        run: |
          # Send Slack notification
          # Create GitHub issue
          # Update monitoring dashboard
```

### Metrics to Track
- **Drift Detection Frequency**: How often drift is found
- **Time to Resolution**: How quickly drift is corrected
- **Drift Sources**: Which resources drift most often
- **Team Response Time**: How quickly teams respond to alerts

## 🛡️ Prevention Strategies

### 1. Access Controls
- Limit who can make manual changes
- Use Azure Policy/AWS Config for compliance
- Implement approval workflows for console access

### 2. Monitoring
- Enable resource change notifications
- Set up activity log monitoring
- Configure drift detection alerts

### 3. Training
- Educate team on Infrastructure as Code
- Document emergency procedures
- Regular drift management reviews

### 4. Automation
- Scheduled drift detection
- Automated alerts and notifications
- Self-healing infrastructure where possible

## 📚 Learning Resources

Each subdirectory contains hands-on examples:
- **Scenarios**: Practice identifying different types of drift
- **Workflows**: Implement automated detection and correction
- **Best Practices**: Learn prevention and governance strategies

## 🎯 Success Metrics

A mature drift management process should achieve:
- **< 2 hours** to detect drift
- **< 24 hours** to correct drift
- **< 5%** of resources experiencing drift per month
- **100%** of changes tracked and documented