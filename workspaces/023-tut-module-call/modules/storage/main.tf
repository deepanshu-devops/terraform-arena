# The local module is provided with the scenario.
variable "bucket_name" {
  type = string
}

resource "terraform_data" "storage" {
  input = var.bucket_name
}
