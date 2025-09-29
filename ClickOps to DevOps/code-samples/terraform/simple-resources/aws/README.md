# AWS Simple Resources - ClickOps to DevOps

This example demonstrates deploying basic AWS resources using Terraform instead of manually clicking through the AWS Console.

## 🎯 What This Demo Shows

**ClickOps Approach** (Manual):
1. Login to AWS Console
2. Navigate to S3 → "Create bucket"
3. Configure bucket settings across multiple screens
4. Manually set up encryption, versioning, access controls
5. Navigate to CloudWatch → Create log group
6. Navigate to IAM → Create role and policies
7. Document everything manually

**DevOps Approach** (Terraform):
1. Define infrastructure in code
2. Run `terraform apply`
3. All resources created with best practices
4. Security settings applied consistently
5. Monitoring included by default

## 📋 Prerequisites

### 1. Install Required Tools
```bash
# Install Terraform (see ../../../installation/)
terraform --version

# Install AWS CLI
# Windows: winget install Amazon.AWSCLI
# macOS: brew install awscli
# Linux: pip install awscli
aws --version
```

### 2. Configure AWS Authentication

#### Option 1: AWS CLI Configuration
```bash
# Configure AWS credentials
aws configure

# Verify configuration
aws sts get-caller-identity
```

#### Option 2: Environment Variables
```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

#### Option 3: IAM Roles (if running on EC2)
AWS credentials will be automatically retrieved from the instance metadata service.

## 🚀 Deploy the Infrastructure

### Step 1: Initialize Terraform
```bash
# Navigate to this directory
cd aws/

# Initialize Terraform (downloads providers)
terraform init
```

### Step 2: Plan the Deployment
```bash
# See what will be created
terraform plan

# Plan with custom values
terraform plan -var="aws_region=us-west-2" -var="environment=dev"
```

### Step 3: Apply the Configuration
```bash
# Deploy the infrastructure
terraform apply

# Deploy with custom values
terraform apply -var="aws_region=us-west-2" -var="environment=dev"
```

### Step 4: View Outputs
```bash
# See all outputs
terraform output

# Get specific output
terraform output s3_bucket_name

# Get complex output as JSON
terraform output -json resource_summary
```

## 📊 What Gets Created

1. **S3 Bucket**: Secure object storage
   - Naming: `clickops-to-devops-demo-{random}`
   - Encryption: AES256 by default
   - Versioning: Enabled
   - Public Access: Blocked

2. **CloudWatch Log Group**: Monitoring and logging
   - Name: `/aws/s3/{bucket-name}`
   - Retention: 7 days (configurable)

3. **IAM Role & Policy**: Secure access control
   - Role: `s3-access-role-{random}`
   - Policy: Read/write access to the S3 bucket

## 🧪 Testing Your Deployment

### Verify Resources with AWS CLI
```bash
# Get bucket name from Terraform output
BUCKET_NAME=$(terraform output -raw s3_bucket_name)

# List bucket details
aws s3api head-bucket --bucket $BUCKET_NAME
aws s3api get-bucket-versioning --bucket $BUCKET_NAME
aws s3api get-bucket-encryption --bucket $BUCKET_NAME
```

### Test S3 Operations
```bash
# Create a test file
echo "Hello from Terraform and AWS!" > test-file.txt

# Upload to S3
aws s3 cp test-file.txt s3://$BUCKET_NAME/

# List bucket contents
aws s3 ls s3://$BUCKET_NAME/

# Download the file
aws s3 cp s3://$BUCKET_NAME/test-file.txt downloaded-file.txt
```

### Check CloudWatch Logs
```bash
# Get log group name
LOG_GROUP=$(terraform output -raw cloudwatch_log_group_name)

# Describe log group
aws logs describe-log-groups --log-group-name-prefix $LOG_GROUP
```

### Test IAM Role
```bash
# Get role ARN
ROLE_ARN=$(terraform output -raw iam_role_arn)

# Describe the role
aws iam get-role --role-name $(terraform output -raw iam_role_name)

# List attached policies
aws iam list-role-policies --role-name $(terraform output -raw iam_role_name)
```

## 🧹 Cleanup

### Remove All Resources
```bash
# First, empty the S3 bucket (if it has objects)
aws s3 rm s3://$(terraform output -raw s3_bucket_name) --recursive

# Then destroy all resources
terraform destroy

# Destroy with auto-approval (use with caution!)
terraform destroy -auto-approve
```

## 🔍 Key DevOps Benefits Demonstrated

1. **Security by Default**: Encryption and access controls built-in
2. **Consistency**: Same configuration every time
3. **Observability**: Monitoring included from the start
4. **Version Control**: All changes tracked in Git
5. **Automation Ready**: Can be integrated into CI/CD
6. **Cost Control**: Resources tagged for cost tracking
7. **Documentation**: Code serves as documentation

## 📚 Files Explained

- **`main.tf`**: Main resource definitions
- **`variables.tf`**: Input parameters with validation
- **`outputs.tf`**: Information extracted from resources
- **`terraform.tfvars.example`**: Example configuration values

## 🔧 Customization

Copy the example variables file and modify:
```bash
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your preferred values
```

Example `terraform.tfvars`:
```hcl
aws_region           = "us-west-2"
bucket_name          = "my-company-demo"
environment          = "dev"
enable_versioning    = true
log_retention_days   = 30
```

## 🚫 Common Issues

**Credentials Error**: Run `aws configure` or set environment variables  
**Bucket Name Conflict**: S3 bucket names must be globally unique  
**Region Mismatch**: Ensure AWS CLI and Terraform use same region  
**Permissions**: Ensure IAM user has necessary permissions for S3, IAM, and CloudWatch  
**State Lock**: If using remote state, ensure DynamoDB table exists

## 🔗 Integration Examples

### Use Outputs in Other Terraform Configurations
```hcl
# In another Terraform configuration
data "terraform_remote_state" "s3_demo" {
  backend = "local"
  config = {
    path = "../aws/terraform.tfstate"
  }
}

# Reference the S3 bucket
resource "aws_s3_bucket_object" "example" {
  bucket = data.terraform_remote_state.s3_demo.outputs.s3_bucket_name
  key    = "example.txt"
  source = "example.txt"
}
```