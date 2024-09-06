# This Terraform file creates an AWS S3 bucket with public access enabled.
# It is intentionally insecure to trigger a tfsec security scan failure.

provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "insecure_bucket" {
  bucket = "insecure-bucket-example"

  # Enabling public access which is considered insecure
  acl    = "public-read"

  tags = {
    Name = "InsecureBucket"
  }
}

resource "aws_s3_bucket_policy" "insecure_policy" {
  bucket = aws_s3_bucket.insecure_bucket.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::insecure-bucket-example/*"
    }
  ]
}
EOF
}
