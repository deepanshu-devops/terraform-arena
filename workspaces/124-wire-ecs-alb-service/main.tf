provider "aws" {
  region = var.aws_region
}

resource "aws_ecs_cluster" "this" {
  name = "app-cluster"
}

resource "aws_ecs_task_definition" "this" {
  family                   = "app-task"
  cpu                      = 256
  memory                   = 512
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  container_definitions    = jsonencode([{ name = "app", image = "nginx:alpine", essential = true }])
}

resource "aws_ecs_service" "this" {
  # TODO - Complete the aws_ecs_service resource.
  # Add the arguments and nested blocks required for aws_ecs_service.
}

resource "aws_lb" "this" {
  name               = "app-alb"
  load_balancer_type = "application"
}

resource "aws_lb_target_group" "this" {
  name     = "app-tg"
  port     = 80
  protocol = "HTTP"
  health_check {
    path = "/"
  }
}

resource "aws_lb_listener" "this" {
  port     = 80
  protocol = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.this.arn
  }
}
