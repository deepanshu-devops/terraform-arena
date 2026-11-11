"""Complete reference solutions for the five hand-authored flagships.

Each reference is a working configuration.  Exactly one region is wrapped in
``# arena:focus-start`` / ``# arena:focus-end``; the registry masks that region
to produce the learner starter, leaving all surrounding code complete.
"""
from __future__ import annotations

from ..catalog.reference import FOCUS_END, FOCUS_START

S3_REFERENCE = {
    "versions.tf": """terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
""",
    "variables.tf": """variable "bucket_name" {
  description = "Globally unique S3 bucket name."
  type        = string

  validation {
    condition     = length(var.bucket_name) >= 3 && length(var.bucket_name) <= 63 && can(regex("^[a-z0-9-]+$", var.bucket_name))
    error_message = "Use 3-63 lowercase letters, numbers, or hyphens."
  }
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging or prod."
  }
}

variable "aws_region" {
  description = "AWS region."
  type        = string
  default     = "us-east-1"
}

variable "enable_versioning" {
  description = "Enable bucket versioning."
  type        = bool
  default     = true
}

variable "project_name" {
  description = "Project name used for tags."
  type        = string
  default     = "terraform-practice"
}
""",
    "main.tf": """provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "this" {
  # arena:focus-start
  bucket = var.bucket_name

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
  # arena:focus-end
}

resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.id

  versioning_configuration {
    status = var.enable_versioning ? "Enabled" : "Suspended"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  bucket = aws_s3_bucket.this.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "this" {
  bucket = aws_s3_bucket.this.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
""",
    "outputs.tf": """output "bucket_id" {
  description = "Bucket id."
  value       = aws_s3_bucket.this.id
}

output "bucket_arn" {
  description = "Bucket ARN."
  value       = aws_s3_bucket.this.arn
}

output "bucket_region" {
  description = "Bucket region."
  value       = aws_s3_bucket.this.region
}
""",
}

DOCKER_REFERENCE = {
    "versions.tf": """terraform {
  required_version = ">= 1.5.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}
""",
    "variables.tf": """variable "docker_host" {
  description = "Docker daemon endpoint."
  type        = string
  default     = "npipe:////./pipe/docker_engine"
}

variable "container_name" {
  description = "Container name."
  type        = string
  default     = "tf-arena-nginx"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]*$", var.container_name))
    error_message = "Use lowercase letters, numbers and hyphens."
  }
}

variable "host_port" {
  description = "Host port."
  type        = number
  default     = 8080

  validation {
    condition     = var.host_port >= 1024 && var.host_port <= 65535
    error_message = "Use a port between 1024 and 65535."
  }
}

variable "image_name" {
  description = "Container image."
  type        = string
  default     = "nginx:alpine"
}

variable "project_name" {
  description = "Project name used for labels."
  type        = string
  default     = "terraform-practice"
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "dev"
}
""",
    "main.tf": """provider "docker" {
  host = var.docker_host
}

resource "docker_image" "this" {
  name = var.image_name
}

resource "docker_container" "this" {
  # arena:focus-start
  name  = var.container_name
  image = docker_image.this.image_id

  restart = "unless-stopped"

  ports {
    internal = 80
    external = var.host_port
  }

  labels {
    label = "Project"
    value = var.project_name
  }

  labels {
    label = "Environment"
    value = var.environment
  }

  labels {
    label = "ManagedBy"
    value = "terraform"
  }
  # arena:focus-end
}
""",
    "outputs.tf": """output "container_id" {
  description = "Container id."
  value       = docker_container.this.id
}

output "container_name" {
  description = "Container name."
  value       = docker_container.this.name
}

output "url" {
  description = "Local URL for the published port."
  value       = "http://localhost:${var.host_port}"
}
""",
}

VPC_REFERENCE = {
    "versions.tf": """terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
""",
    "variables.tf": """variable "vpc_cidr" {
  description = "VPC CIDR block."
  type        = string
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrnetmask(var.vpc_cidr))
    error_message = "vpc_cidr must be a valid IPv4 CIDR."
  }
}

variable "public_subnet_cidrs" {
  description = "Public subnet CIDR blocks."
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "availability_zones" {
  description = "Availability zones for the public subnets."
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "aws_region" {
  description = "AWS region."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used for tags."
  type        = string
  default     = "terraform-practice"
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging or prod."
  }
}
""",
    "main.tf": """provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "this" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_subnet" "this" {
  # arena:focus-start
  count                   = length(var.public_subnet_cidrs)
  vpc_id                  = aws_vpc.this.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
  # arena:focus-end
}

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_route_table" "this" {
  vpc_id = aws_vpc.this.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.this.id
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_route_table_association" "this" {
  count          = length(var.public_subnet_cidrs)
  subnet_id      = aws_subnet.this[count.index].id
  route_table_id = aws_route_table.this.id
}
""",
    "outputs.tf": """output "vpc_id" {
  description = "VPC id."
  value       = aws_vpc.this.id
}

output "public_subnet_ids" {
  description = "Public subnet ids."
  value       = aws_subnet.this[*].id
}

output "internet_gateway_id" {
  description = "Internet gateway id."
  value       = aws_internet_gateway.this.id
}
""",
}

ASG_REFERENCE = {
    "versions.tf": """terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
""",
    "variables.tf": """variable "vpc_id" {
  description = "VPC id for the web tier."
  type        = string
}

variable "subnet_ids" {
  description = "Subnets for the ALB and Auto Scaling group."
  type        = list(string)
}

variable "instance_type" {
  description = "Free-tier instance type."
  type        = string
  default     = "t2.micro"

  validation {
    condition     = contains(["t2.micro", "t3.micro", "t2.small", "t3.small"], var.instance_type)
    error_message = "Use a free-tier instance type."
  }
}

variable "asg_min" {
  description = "Minimum fleet size."
  type        = number
  default     = 1
}

variable "asg_max" {
  description = "Maximum fleet size."
  type        = number
  default     = 2

  validation {
    condition     = var.asg_max >= 1 && var.asg_max <= 4
    error_message = "asg_max must be between 1 and 4."
  }
}

variable "asg_desired" {
  description = "Desired fleet size."
  type        = number
  default     = 1
}

variable "health_check_path" {
  description = "Target group health check path."
  type        = string
  default     = "/"
}

variable "aws_region" {
  description = "AWS region."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used for tags."
  type        = string
  default     = "terraform-practice"
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging or prod."
  }
}
""",
    "main.tf": """provider "aws" {
  region = var.aws_region
}

data "aws_ami" "latest" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

resource "aws_security_group" "this" {
  name        = "arena-web-sg"
  description = "Web tier security group"
  vpc_id      = var.vpc_id

  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_launch_template" "this" {
  name          = "arena-web-lt"
  image_id      = data.aws_ami.latest.id
  instance_type = var.instance_type

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required"
  }

  tag_specifications {
    resource_type = "instance"

    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

resource "aws_lb" "this" {
  name               = "arena-web-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.this.id]
  subnets            = var.subnet_ids

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_lb_target_group" "this" {
  name     = "arena-web-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    path = var.health_check_path
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_lb_listener" "this" {
  load_balancer_arn = aws_lb.this.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.this.arn
  }
}

resource "aws_autoscaling_group" "this" {
  # arena:focus-start
  name                = "arena-web-asg"
  min_size            = var.asg_min
  max_size            = var.asg_max
  desired_capacity    = var.asg_desired
  vpc_zone_identifier = var.subnet_ids
  target_group_arns   = [aws_lb_target_group.this.arn]
  health_check_type   = "ELB"

  launch_template {
    id      = aws_launch_template.this.id
    version = "$Latest"
  }

  tag {
    key                 = "Project"
    value               = var.project_name
    propagate_at_launch = true
  }

  tag {
    key                 = "Environment"
    value               = var.environment
    propagate_at_launch = true
  }

  tag {
    key                 = "ManagedBy"
    value               = "terraform"
    propagate_at_launch = true
  }
  # arena:focus-end
}
""",
    "outputs.tf": """output "alb_dns_name" {
  description = "Public DNS name of the load balancer."
  value       = aws_lb.this.dns_name
}

output "asg_name" {
  description = "Auto Scaling group name."
  value       = aws_autoscaling_group.this.name
}

output "security_group_id" {
  description = "Web tier security group id."
  value       = aws_security_group.this.id
}
""",
}

SERVERLESS_REFERENCE = {
    "versions.tf": """terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
""",
    "variables.tf": """variable "table_name" {
  description = "DynamoDB table name."
  type        = string
  default     = "items"
}

variable "lambda_runtime" {
  description = "Lambda runtime."
  type        = string
  default     = "python3.12"
}

variable "lambda_memory" {
  description = "Lambda memory size in MB."
  type        = number
  default     = 128

  validation {
    condition     = var.lambda_memory >= 128 && var.lambda_memory <= 512
    error_message = "lambda_memory must be between 128 and 512 MB."
  }
}

variable "api_stage" {
  description = "HTTP API stage name."
  type        = string
  default     = "prod"
}

variable "aws_region" {
  description = "AWS region."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used for tags."
  type        = string
  default     = "terraform-practice"
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging or prod."
  }
}
""",
    "main.tf": """provider "aws" {
  region = var.aws_region
}

resource "aws_dynamodb_table" "this" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  server_side_encryption {
    enabled = true
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "this" {
  name               = "arena-items-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

data "aws_iam_policy_document" "lambda_policy" {
  statement {
    sid       = "DynamoDbReadWrite"
    effect    = "Allow"
    actions   = ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:Query"]
    resources = [aws_dynamodb_table.this.arn]
  }
}

resource "aws_iam_policy" "this" {
  name   = "arena-items-policy"
  policy = data.aws_iam_policy_document.lambda_policy.json

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_iam_role_policy_attachment" "this" {
  role       = aws_iam_role.this.name
  policy_arn = aws_iam_policy.this.arn
}

resource "aws_lambda_function" "this" {
  # arena:focus-start
  function_name                  = "arena-items"
  role                           = aws_iam_role.this.arn
  runtime                        = var.lambda_runtime
  memory_size                    = var.lambda_memory
  handler                        = "handler.lambda_handler"
  filename                       = "lambda.zip"
  timeout                        = 10
  reserved_concurrent_executions = 5

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.this.name
    }
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
  # arena:focus-end
}

resource "aws_apigatewayv2_api" "this" {
  name          = "arena-items-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "this" {
  api_id                 = aws_apigatewayv2_api.this.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.this.invoke_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "this" {
  api_id    = aws_apigatewayv2_api.this.id
  route_key = "GET /items"
  target    = "integrations/${aws_apigatewayv2_integration.this.id}"
}

resource "aws_apigatewayv2_stage" "this" {
  api_id      = aws_apigatewayv2_api.this.id
  name        = var.api_stage
  auto_deploy = true
}

resource "aws_lambda_permission" "this" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.this.execution_arn}/*/*"
}
""",
    "outputs.tf": """output "api_endpoint" {
  description = "HTTP API endpoint."
  value       = aws_apigatewayv2_api.this.api_endpoint
}

output "lambda_name" {
  description = "Lambda function name."
  value       = aws_lambda_function.this.function_name
}

output "table_name" {
  description = "DynamoDB table name."
  value       = aws_dynamodb_table.this.name
}
""",
}

REFERENCES: dict[str, dict[str, str]] = {
    "secure-s3-bucket": S3_REFERENCE,
    "docker-nginx-sandbox": DOCKER_REFERENCE,
    "ha-vpc-foundation": VPC_REFERENCE,
    "autoscaling-web-tier": ASG_REFERENCE,
    "serverless-item-api": SERVERLESS_REFERENCE,
}

FOCUS: dict[str, dict] = {
    "secure-s3-bucket": {
        "kind": "resource",
        "file": "main.tf",
        "rtype": "aws_s3_bucket",
        "name": "this",
        "title": "Complete the S3 bucket resource",
        "todo": "Set the bucket name from the input variable and add the three standard tags.",
    },
    "docker-nginx-sandbox": {
        "kind": "resource",
        "file": "main.tf",
        "rtype": "docker_container",
        "name": "this",
        "title": "Complete the Nginx container",
        "todo": "Wire the name, image, restart policy, published port and operational labels.",
    },
    "ha-vpc-foundation": {
        "kind": "resource",
        "file": "main.tf",
        "rtype": "aws_subnet",
        "name": "this",
        "title": "Complete the public subnet definition",
        "todo": "Create one subnet per CIDR, spread them across AZs, make them public and tag them.",
    },
    "autoscaling-web-tier": {
        "kind": "resource",
        "file": "main.tf",
        "rtype": "aws_autoscaling_group",
        "name": "this",
        "title": "Complete the Auto Scaling group",
        "todo": "Wire the size variables, subnets, target group, launch template and propagated tags.",
    },
    "serverless-item-api": {
        "kind": "resource",
        "file": "main.tf",
        "rtype": "aws_lambda_function",
        "name": "this",
        "title": "Complete the Lambda function",
        "todo": "Wire the role, runtime, memory, handler, timeout, concurrency cap, environment and tags.",
    },
}

__all__ = ["REFERENCES", "FOCUS", "FOCUS_START", "FOCUS_END"]
