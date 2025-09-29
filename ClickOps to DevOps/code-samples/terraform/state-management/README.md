# Terraform State Management Examples

Learn how Terraform tracks your infrastructure and why proper state management is crucial for the ClickOps to DevOps transformation.

## 🎯 State Management: ClickOps vs DevOps

| Manual Operations (ClickOps) | Terraform State (DevOps) |
|------------------------------|---------------------------|
| No tracking of what exists | Complete inventory in state file |
| Changes cause conflicts | State prevents conflicts |
| Manual documentation needed | Automatic resource tracking |
| Team coordination nightmare | Shared state enables collaboration |
| Drift goes unnoticed | State enables drift detection |
| No rollback capability | State enables safe rollbacks |

## 📁 Examples

### [local-state/](./local-state/)
Understanding Terraform's local state file
- How state files work
- Inspecting and understanding state
- Local state limitations
- Best practices for single-user scenarios

### [remote-state/](./remote-state/)
Configuring remote state backends for team collaboration
- Azure Storage backend configuration
- AWS S3 backend with DynamoDB locking
- Team collaboration workflows
- State locking and consistency

### [state-operations/](./state-operations/)
Common state manipulation operations
- Importing existing resources
- Moving resources between states
- Removing resources from state
- State backup and recovery

## 🚀 Learning Path

1. **Start with Local State**: Understand the basics with [local-state/](./local-state/)
2. **Move to Remote State**: Set up team collaboration with [remote-state/](./remote-state/)
3. **Master State Operations**: Learn advanced techniques in [state-operations/](./state-operations/)

## 🔑 Key Concepts

### What is Terraform State?
Terraform state is a file that maps your configuration to real-world resources. It's Terraform's way of keeping track of what it has created and managing changes over time.

### Why State Matters
- **Resource Tracking**: Knows what resources exist
- **Performance**: Caches resource attributes for large infrastructures
- **Collaboration**: Enables teams to work together safely
- **Drift Detection**: Can identify changes made outside of Terraform

### State File Contents
```json
{
  "version": 4,
  "terraform_version": "1.6.0",
  "resources": [
    {
      "type": "azurerm_resource_group",
      "name": "example",
      "instances": [
        {
          "attributes": {
            "name": "rg-example",
            "location": "East US"
          }
        }
      ]
    }
  ]
}
```

## ⚠️ State Security Considerations

### Sensitive Data in State
State files can contain sensitive information:
- Database passwords
- API keys
- Private keys
- Connection strings

### Best Practices
1. **Never commit state to version control**
2. **Use remote state with encryption**
3. **Restrict access to state files**
4. **Use state locking to prevent conflicts**
5. **Regular state backups**

## 🛡️ State Locking

State locking prevents multiple users from running Terraform simultaneously against the same state file, preventing corruption.

### Supported Backends with Locking
- **AWS S3 + DynamoDB**: Full locking support
- **Azure Storage**: Native locking support
- **Terraform Cloud**: Built-in locking
- **Consul**: Distributed locking

## 📊 Troubleshooting State Issues

### Common Problems
1. **State File Corruption**: Use backups and validation
2. **Resource Drift**: Use `terraform refresh` and `terraform plan`
3. **Lock Conflicts**: Use `terraform force-unlock` carefully
4. **Missing Resources**: Use `terraform import` to add existing resources

### Recovery Commands
```bash
# Refresh state from real infrastructure
terraform refresh

# Show current state
terraform show

# List resources in state
terraform state list

# Show specific resource
terraform state show aws_s3_bucket.example

# Validate state file
terraform validate
```

## 🔗 Integration with CI/CD

State management is crucial for automated deployments:

```yaml
# Example GitHub Actions workflow
- name: Terraform Plan
  run: terraform plan -out=tfplan
  
- name: Terraform Apply
  run: terraform apply tfplan
  if: github.ref == 'refs/heads/main'
```

Each example directory contains practical demonstrations of these concepts with step-by-step instructions.