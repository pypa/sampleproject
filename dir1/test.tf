provider "aws" {
  region = "us-west-2"
}

# S3 Bucket with multiple critical issues
resource "aws_s3_bucket" "example" {
  bucket = "critical-example-bucket"

  # Public read access, which will flag as a critical issue
  acl = "public-read"

  # Missing server-side encryption
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = ""
      }
    }
  }

  # Bucket policy allowing full public access, a critical security risk
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": "arn:aws:s3:::critical-example-bucket/*"
    }
  ]
}
EOF
}

# Security Group allowing all traffic, critical exposure
resource "aws_security_group" "critical_sg" {
  name_prefix = "critical-sg-"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"  # Allows all protocols
    cidr_blocks = ["0.0.0.0/0"]  # Allows access from any IP, critical risk
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"  # Allows all protocols
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 Instance with multiple high-severity issues
resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0" # Example AMI
  instance_type = "t2.micro"

  # Missing key_name for SSH access control
  key_name = ""

  # Security group allowing all inbound traffic
  vpc_security_group_ids = [aws_security_group.critical_sg.id]

  # Using default VPC, considered insecure for production
  associate_public_ip_address = true

  # Unencrypted root and data volumes
  root_block_device {
    volume_type           = "gp2"
    volume_size           = 10
    encrypted             = false  # Should be encrypted
  }
}

# RDS Instance with critical issues
resource "aws_db_instance" "example_db" {
  identifier             = "critical-db-instance"
  instance_class         = "db.t2.micro"
  engine                 = "mysql"
  username               = "admin"
  password               = "password123" # Weak password, critical issue
  publicly_accessible    = true  # Publicly accessible DB, critical risk
  storage_encrypted      = false # Storage not encrypted
  skip_final_snapshot    = true  # No backup on deletion, critical risk
  multi_az               = false # Single AZ, high availability concern
}

# IAM Policy allowing full administrative access, a critical security risk
resource "aws_iam_policy" "admin_policy" {
  name        = "AdminPolicy"
  description = "A policy that grants full access to all resources."

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
EOF
}

# IAM User with overly permissive policy
resource "aws_iam_user" "example_user" {
  name = "example-user"
}

resource "aws_iam_user_policy_attachment" "example_attachment" {
  user       = aws_iam_user.example_user.name
  policy_arn = aws_iam_policy.admin_policy.arn
}

# CloudFront Distribution with insecure origin and protocols
resource "aws_cloudfront_distribution" "example_distribution" {
  origin {
    domain_name = "example.com"
    origin_id   = "exampleOrigin"

    # Allows insecure origin protocols, should use HTTPS
    origin_protocol_policy = "http-only"
  }

  default_cache_behavior {
    target_origin_id       = "exampleOrigin"
    viewer_protocol_policy = "allow-all" # Allows HTTP, critical security risk
  }

  enabled = true
}
