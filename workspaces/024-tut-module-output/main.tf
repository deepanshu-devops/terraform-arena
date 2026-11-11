module "storage" {
  source      = "./modules/storage"
  bucket_name = var.bucket_name
}

output "bucket_id" {
  # TODO - Wire the module output.
  # Set the root output value to the module's storage_id output.
}
