output "secret_arn" {
  value = aws_secretsmanager_secret.this.arn
}

output "db_endpoint" {
  value = aws_db_instance.this.id
}
