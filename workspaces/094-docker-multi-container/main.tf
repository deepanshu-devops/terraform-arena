provider "docker" {
  host = var.docker_host
}

resource "docker_network" "this" {
  # TODO - Complete the shared Docker network.
  # Create the network that both containers join.
}

resource "docker_container" "web" {
  name  = "${var.network_name}-web"
  image = "nginx:alpine"
  ports {
    internal = 80
    external = 8080
  }
  networks_advanced {
    name = docker_network.this.name
  }
}

resource "docker_container" "worker" {
  name  = "${var.network_name}-worker"
  image = "alpine:latest"
  ports {
    internal = 80
    external = 8080
  }
  networks_advanced {
    name = docker_network.this.name
  }
}
