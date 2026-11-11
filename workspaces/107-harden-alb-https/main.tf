provider "aws" {
  region = var.aws_region
}

resource "aws_lb_listener" "https" {
  # TODO - Complete the graded block.
  # Complete this block using the challenge requirements.
}

resource "aws_lb_listener" "http" {
  port              = 80
  protocol          = "HTTP"
  load_balancer_arn = var.lb_arn
  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}
