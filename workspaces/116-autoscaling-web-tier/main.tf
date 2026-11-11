provider "aws" {
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
  # TODO - Complete the Auto Scaling group.
  # Wire the size variables, subnets, target group, launch template and propagated tags.
}
