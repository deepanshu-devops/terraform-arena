output "alb_dns_name" {
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
