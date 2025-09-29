# AWS Simple Resource Deployment Example
# This demonstrates creating basic AWS resources with Terraform
# instead of clicking through the AWS Console

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = var.aws_region

  # Default tags applied to all resources
  default_tags {
    tags = {
      Environment = var.environment
      Purpose     = "ClickOps to DevOps Demo"
      ManagedBy   = "Terraform"
      CreatedBy   = "MMS2025-Demo"
    }
  }
}

# Generate a random suffix for unique naming
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

# Create an S3 bucket
# ClickOps: AWS Console -> S3 -> Create bucket -> Multiple configuration screens
# DevOps: Consistent configuration, version controlled, reproducible
resource "aws_s3_bucket" "example" {
  bucket = "${var.bucket_name}-${random_string.suffix.result}"

  tags = {
    Name        = "${var.bucket_name}-${random_string.suffix.result}"
    Environment = var.environment
    Purpose     = "ClickOps to DevOps Demo"
  }
}

# Configure bucket versioning
# ClickOps: Separate configuration screen in AWS Console
# DevOps: Defined alongside bucket creation
resource "aws_s3_bucket_versioning" "example" {
  bucket = aws_s3_bucket.example.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Configure bucket encryption
# ClickOps: Security settings often overlooked in manual deployment
# DevOps: Security by default, consistent across all deployments
resource "aws_s3_bucket_server_side_encryption_configuration" "example" {
  bucket = aws_s3_bucket.example.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Block public access
# ClickOps: Security setting that might be missed
# DevOps: Security by default
resource "aws_s3_bucket_public_access_block" "example" {
  bucket = aws_s3_bucket.example.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Create a CloudWatch log group for monitoring
# ClickOps: Monitoring setup often forgotten
# DevOps: Observability included from the start
resource "aws_cloudwatch_log_group" "example" {
  name              = "/aws/s3/${aws_s3_bucket.example.bucket}"
  retention_in_days = 7

  tags = {
    Name        = "S3 Access Logs - ${aws_s3_bucket.example.bucket}"
    Environment = var.environment
  }
}

# Create an IAM role for S3 access (example)
# ClickOps: IAM configuration through multiple screens
# DevOps: Permissions as code, reviewable and consistent
resource "aws_iam_role" "s3_access_role" {
  name = "s3-access-role-${random_string.suffix.result}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "S3 Access Role"
    Environment = var.environment
  }
}

# Attach a policy to the IAM role
resource "aws_iam_role_policy" "s3_access_policy" {
  name = "s3-access-policy"
  role = aws_iam_role.s3_access_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = "${aws_s3_bucket.example.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket"
        ]
        Resource = aws_s3_bucket.example.arn
      }
    ]
  })
}