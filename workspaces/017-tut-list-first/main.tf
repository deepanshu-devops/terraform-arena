locals {
  # TODO - Create the ordered list.
  # Add three environment names in deployment order.
}

output "first_environment" {
  value = local.environments[0]
}

output "environment_count" {
  value = length(local.environments)
}
