provider "aws" {
  region = var.aws_region
}

resource "aws_lb" "this" {
  name               = "app-alb"
  load_balancer_type = "application"
  subnets            = var.subnet_ids
}

resource "aws_lb_target_group" "this" {
  name     = "app-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id
  health_check {
    path = "/"
  }
}

resource "aws_lb_listener" "this" {
  # TODO - Complete the aws_lb_listener resource.
  # Add the arguments and nested blocks required for aws_lb_listener.
}
