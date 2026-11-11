provider "docker" {
  host = var.docker_host
}

resource "docker_image" "this" {
  name = var.image_name
}

resource "docker_container" "this" {
  # TODO - Complete the Nginx container.
  # Wire the name, image, restart policy, published port and operational labels.
}
