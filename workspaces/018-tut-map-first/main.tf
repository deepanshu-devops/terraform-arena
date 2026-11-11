locals {
  # TODO - Create the lookup map.
  # Add a two-entry map with a small dev size and a larger prod size.
}

output "dev_instance_type" {
  value = local.instance_types["dev"]
}

output "all_instance_types" {
  value = local.instance_types
}
