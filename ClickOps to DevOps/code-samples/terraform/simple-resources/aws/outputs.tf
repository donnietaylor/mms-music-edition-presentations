# Outputs for AWS Simple Resource Deployment
# This demonstrates how to extract important information from deployed resources
# ClickOps Problem: Have to manually note down resource details
# DevOps Solution: Outputs are automatically available and can be used by other systems

output "s3_bucket_name" {
  description = "Name of the created S3 bucket"
  value       = aws_s3_bucket.example.bucket
}

output "s3_bucket_arn" {
  description = "ARN of the created S3 bucket"
  value       = aws_s3_bucket.example.arn
}

output "s3_bucket_region" {
  description = "Region of the created S3 bucket"
  value       = aws_s3_bucket.example.region
}

output "s3_bucket_domain_name" {
  description = "Domain name of the S3 bucket"
  value       = aws_s3_bucket.example.bucket_domain_name
}

output "s3_bucket_hosted_zone_id" {
  description = "Hosted zone ID for the S3 bucket"
  value       = aws_s3_bucket.example.hosted_zone_id
}

output "cloudwatch_log_group_name" {
  description = "Name of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.example.name
}

output "cloudwatch_log_group_arn" {
  description = "ARN of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.example.arn
}

output "iam_role_name" {
  description = "Name of the created IAM role"
  value       = aws_iam_role.s3_access_role.name
}

output "iam_role_arn" {
  description = "ARN of the created IAM role"
  value       = aws_iam_role.s3_access_role.arn
}

# Sensitive information (be careful with these)
output "aws_account_id" {
  description = "AWS Account ID where resources were created"
  value       = data.aws_caller_identity.current.account_id
}

# Complex output combining multiple resource attributes
output "resource_summary" {
  description = "Summary of created AWS resources"
  value = {
    s3_bucket = {
      name               = aws_s3_bucket.example.bucket
      arn                = aws_s3_bucket.example.arn
      region             = aws_s3_bucket.example.region
      versioning_enabled = aws_s3_bucket_versioning.example.versioning_configuration[0].status
      encryption_enabled = true
      public_access_blocked = true
    }
    monitoring = {
      log_group_name = aws_cloudwatch_log_group.example.name
      log_retention  = aws_cloudwatch_log_group.example.retention_in_days
    }
    security = {
      iam_role_name = aws_iam_role.s3_access_role.name
      iam_role_arn  = aws_iam_role.s3_access_role.arn
    }
    deployment_info = {
      terraform_version = terraform.version
      aws_region        = var.aws_region
      random_suffix     = random_string.suffix.result
      deployed_at       = timestamp()
      account_id        = data.aws_caller_identity.current.account_id
    }
  }
}

# Useful commands output
output "useful_commands" {
  description = "Useful AWS CLI commands for the created resources"
  value = {
    list_bucket_contents = "aws s3 ls s3://${aws_s3_bucket.example.bucket}/"
    upload_file         = "aws s3 cp <local-file> s3://${aws_s3_bucket.example.bucket}/"
    download_file       = "aws s3 cp s3://${aws_s3_bucket.example.bucket}/<file> ."
    view_logs          = "aws logs describe-log-groups --log-group-name-prefix ${aws_cloudwatch_log_group.example.name}"
    assume_role        = "aws sts assume-role --role-arn ${aws_iam_role.s3_access_role.arn} --role-session-name terraform-demo"
  }
}