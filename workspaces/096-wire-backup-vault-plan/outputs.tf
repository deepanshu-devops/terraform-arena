output "vault_arn" {
  value = aws_backup_vault.this.arn
}

output "plan_arn" {
  value = aws_backup_plan.this.arn
}
