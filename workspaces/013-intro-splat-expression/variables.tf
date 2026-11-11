variable "instances" {
  description = "Instance metadata."
  type = list(object({
    name       = string
    private_ip = string
  }))
  default = [
    { name = "web", private_ip = "10.0.1.10" },
    { name = "api", private_ip = "10.0.2.10" },
  ]
}
