variable "bucket_name" {
  type = string
}

resource "terraform_data" "storage" {
  input = var.bucket_name
}

output "bucket_name" {
  value = var.bucket_name
}
