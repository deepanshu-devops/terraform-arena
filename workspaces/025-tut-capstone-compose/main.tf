locals {
  # TODO - Build the module input map.
  # Turn the environment list into a map of stable bucket names.
}

module "storage" {
  source      = "./modules/storage"
  for_each    = local.environment_map
  bucket_name = each.value
}

output "bucket_names" {
  value = { for env, bucket in module.storage : env => bucket.bucket_name }
}
