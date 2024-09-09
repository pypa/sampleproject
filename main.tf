provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "example" {
  bucket = "example-bucket"

  # This will flag because public access is allowed
  acl = "public-read"

  # Flags for enabling server access logging
  # Access logs should be enabled
  logging {
    target_bucket = ""
  }

  # Flags for bucket policy allowing public access
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::example-bucket/*"
    }
  ]
}
EOF
}

resource "aws_security_group" "example" {
  name_prefix = "example-sg-"

  # This will flag because it allows ingress on port 22 from any IP
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # This will flag because it allows ingress on port 80 from any IP
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # This will flag because it allows egress on all ports to any IP
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "example" {
  identifier = "example-db"

  # This will flag because encryption is disabled
  storage_encrypted = false

  # This will flag for allowing public accessibility
  publicly_accessible = true

  instance_class = "db.t2.micro"
  engine = "mysql"
  username = "admin"
  password = "password123" # Weak password
}

resource "aws_ebs_volume" "example" {
  availability_zone = "us-west-2a"
  size = 10

  # This will flag because encryption is disabled
  encrypted = false
}

resource "aws_cloudfront_distribution" "example" {
  origin {
    domain_name = "example.com"

    # This will flag because the origin protocol policy is 'http-only'
    origin_id = "origin"
    origin_protocol_policy = "http-only"
  }

  enabled = true
  default_cache_behavior {
    target_origin_id = "origin"
    viewer_protocol_policy = "allow-all"
  }
}
