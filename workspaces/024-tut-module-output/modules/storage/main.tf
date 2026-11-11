variable "bucket_name" {
  type = string
}

resource "terraform_data" "storage" {
  input = var.bucket_name
}

output "storage_id" {
  value = terraform_data.storage.id
}
