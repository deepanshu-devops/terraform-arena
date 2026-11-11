"""Challenge 02 — Docker Nginx Sandbox (Easy)."""
from __future__ import annotations

import re

from .. import checks as C
from ..evaluator import Challenge, TestCase
from ..hcl import has_ref, norm, unquote


def _labels(container):
    out = {}
    if not container:
        return out
    for block in container.nested("labels"):
        key = C.raw(block, "label")
        val = C.raw(block, "value")
        if key:
            out[unquote(key) or key] = val
    return out


def t_provider(cfg):
    ok, msg = C.required_provider(cfg, "docker")
    if not ok:
        return False, msg
    if "docker" not in cfg.providers():
        return False, 'Missing provider "docker" configuration block.'
    return True, "Docker provider is declared and configured."


def t_provider_host(cfg):
    provider = cfg.providers().get("docker")
    if not provider:
        return False, 'Missing provider "docker" block.'
    return C.is_ref(provider, "host", "var.docker_host")


def t_container_name_var(cfg):
    var = C.get_var(cfg, "container_name")
    if not var:
        return False, "Variable 'container_name' is not defined."
    if norm(C.var_type(var) or "") != "string":
        return False, "container_name must be type string."
    text = C.validation_text(var)
    pats = re.findall(r'"([^"]*)"', text or "")
    if "regex(" not in text or not any(("a-z" in p and "-" in p) for p in pats):
        return False, "container_name needs a regex validation for lowercase/hyphen names."
    return True, "container_name is validated."


def t_port_var(cfg):
    var = C.get_var(cfg, "host_port")
    if not var:
        return False, "Variable 'host_port' is not defined."
    if norm(C.var_type(var) or "") != "number":
        return False, "host_port must be type number."
    _, default = C.var_default(var)
    if default != 8080:
        return False, f"host_port default must be 8080, found {default!r}."
    text = C.validation_text(var)
    if not ("1024" in text and "65535" in text):
        return False, "host_port validation must enforce the range 1024–65535."
    return True, "host_port is a number defaulting to 8080 with range validation."


def t_image_var(cfg):
    var = C.get_var(cfg, "image_name")
    if not var:
        return False, "Variable 'image_name' is not defined."
    _, default = C.var_default(var)
    if default != "nginx:alpine":
        return False, f"image_name default must be nginx:alpine, found {default!r}."
    return True, "image_name defaults to nginx:alpine."


def t_image_resource(cfg):
    image = C.first_resource(cfg, "docker_image")
    if not image:
        return False, "Missing docker_image resource."
    name = C.raw(image, "name")
    if not name or not has_ref(name, "var.image_name"):
        return False, f"docker_image.name must reference var.image_name, found {name!r}."
    return True, "docker_image pulls var.image_name."


def t_container_resource(cfg):
    container = C.first_resource(cfg, "docker_container")
    if not container:
        return False, "Missing docker_container resource."
    name = C.raw(container, "name")
    if not name or not has_ref(name, "var.container_name"):
        return False, f"docker_container.name must reference var.container_name, found {name!r}."
    image = C.raw(container, "image")
    if not image or "docker_image." not in image:
        return False, f"docker_container.image must reference the docker_image resource, found {image!r}."
    return True, "Container name is parameterized and wired to docker_image."


def t_ports(cfg):
    container = C.first_resource(cfg, "docker_container")
    if not container:
        return False, "Missing docker_container resource."
    ports = container.nested("ports")
    if not ports:
        return False, "Missing ports block on docker_container."
    port = ports[0]
    internal = C.raw(port, "internal")
    external = C.raw(port, "external")
    if norm(internal or "") != "80":
        return False, f"ports.internal must be 80, found {internal!r}."
    if not external or not has_ref(external, "var.host_port"):
        return False, f"ports.external must reference var.host_port, found {external!r}."
    return True, "Port 80 is published on var.host_port."


def t_restart(cfg):
    container = C.first_resource(cfg, "docker_container")
    if not container:
        return False, "Missing docker_container resource."
    return C.equals(container, "restart", '"unless-stopped"')


def t_not_privileged(cfg):
    container = C.first_resource(cfg, "docker_container")
    if not container:
        return False, "Missing docker_container resource."
    raw = C.raw(container, "privileged")
    if raw is None:
        return True, "privileged is absent (defaults to false)."
    if norm(raw) == "false":
        return True, "privileged = false."
    return False, f"privileged must be false, found {raw!r}."


def t_no_docker_socket(cfg):
    container = C.first_resource(cfg, "docker_container")
    if not container:
        return False, "Missing docker_container resource."
    for vol in container.nested("volumes"):
        container_path = C.raw(vol, "container_path") or ""
        if "docker.sock" in container_path:
            return False, "Mounting the Docker socket into the container is blocked."
    if norm(C.raw(container, "network_mode") or "") == '"host"':
        return False, "network_mode = host is blocked."
    return True, "No Docker-socket mount or host networking."


def t_labels(cfg):
    container = C.first_resource(cfg, "docker_container")
    if not container:
        return False, "Missing docker_container resource."
    labels = _labels(container)
    issues = []
    for key, expected in (
        ("Project", "var.project_name"),
        ("Environment", "var.environment"),
        ("ManagedBy", '"terraform"'),
    ):
        if key not in labels:
            issues.append(f"missing label {key}")
        elif norm(labels[key]) != norm(expected):
            issues.append(f"label {key} expected {expected!r}, found {labels[key]!r}")
    if issues:
        return False, "; ".join(issues)
    return True, "Container carries Project, Environment and ManagedBy labels."


def t_outputs(cfg):
    missing = []
    for name in ("container_id", "container_name", "url"):
        ok, msg = C.output_ok(cfg, name)
        if not ok:
            missing.append(msg)
    if missing:
        return False, "; ".join(missing)
    url = C.get_output(cfg, "url")
    if url:
        val = C.raw(url, "value") or ""
        if not has_ref(val, "var.host_port") and "localhost" not in val and "127.0.0.1" not in val:
            return False, "url output should reference var.host_port (e.g. http://localhost:${var.host_port})."
    return True, "container_id, container_name and url outputs exist."


def t_usage(cfg):
    used = cfg.referenced_variables()
    missing = [n for n in ("docker_host", "container_name", "host_port", "image_name") if n not in used]
    if missing:
        return False, "Variables declared but not referenced: " + ", ".join(missing)
    return True, "Core variables are wired into resources."


CHALLENGE = Challenge(
    id="docker-nginx-sandbox",
    number=2,
    title="Docker Nginx Sandbox",
    difficulty="Easy",
    points=100,
    tags=["docker", "sandbox", "providers", "outputs"],
    scenario=(
        "Before shipping AWS challenges to a live judge, you must prove the workflow on a "
        "zero-cost local sandbox. Using the Docker provider, provision an Nginx container that "
        "publishes port 80 on a configurable host port, restarts unless stopped, and carries "
        "operational labels. This challenge can be applied and destroyed against your local "
        "Docker daemon — no cloud bill."
    ),
    constraints=[
        "Provider: kreuzwerker/docker declared in required_providers.",
        "Docker provider host must reference var.docker_host (default: npipe:////./pipe/docker_engine).",
        "container_name must be a validated lowercase/hyphen string.",
        "host_port must be a number defaulting to 8080 with validation 1024–65535.",
        "image_name must default to nginx:alpine.",
        "The container must publish internal port 80 on var.host_port.",
        "restart policy must be unless-stopped.",
        "privileged must be false; mounting docker.sock and host networking are blocked.",
        "Container must carry labels: Project, Environment, ManagedBy = \"terraform\".",
        "Outputs must expose container_id, container_name and url.",
    ],
    variables=[
        {"name": "docker_host", "type": "string", "default": "npipe:////./pipe/docker_engine"},
        {"name": "container_name", "type": "string", "default": "tf-arena-nginx", "validation": True},
        {"name": "host_port", "type": "number", "default": 8080, "validation": True},
        {"name": "image_name", "type": "string", "default": "nginx:alpine"},
        {"name": "project_name", "type": "string", "default": "terraform-practice"},
        {"name": "environment", "type": "string", "default": "dev"},
    ],
    expected_resources=["docker_image", "docker_container"],
    expected_outputs=["container_id", "container_name", "url"],
    starter={
        "versions.tf": "# versions.tf\n# TODO: declare the docker provider (source + version).\n",
        "variables.tf": "# variables.tf\n# TODO: declare docker_host, container_name, host_port, image_name, project_name, environment.\n",
        "main.tf": "# main.tf\n# TODO: configure the docker provider, pull the image and run the container.\n",
        "outputs.tf": "# outputs.tf\n# TODO: expose container_id, container_name and url.\n",
    },
    allowlist=["docker_image", "docker_container", "docker_network", "docker_volume"],
    apply_sandbox=True,
    tests=[
        TestCase("docker-provider", "Docker provider declared", "Providers", 7, t_provider),
        TestCase("docker-host", "Provider host from var.docker_host", "Providers", 7, t_provider_host),
        TestCase("docker-name-var", "container_name validated", "Variables", 7, t_container_name_var),
        TestCase("docker-port-var", "host_port default + range validation", "Variables", 8, t_port_var),
        TestCase("docker-image-var", "image_name defaults to nginx:alpine", "Variables", 5, t_image_var),
        TestCase("docker-image", "docker_image resource wired to variable", "Resources", 7, t_image_resource),
        TestCase("docker-container", "docker_container wired correctly", "Resources", 8, t_container_resource),
        TestCase("docker-ports", "Port 80 published on var.host_port", "Resources", 8, t_ports),
        TestCase("docker-restart", "restart = unless-stopped", "Lifecycle", 6, t_restart),
        TestCase("docker-privileged", "Container not privileged", "Security", 7, t_not_privileged),
        TestCase("docker-socket", "No docker.sock mount / host network", "Security", 8, t_no_docker_socket),
        TestCase("docker-labels", "Operational labels present", "Lifecycle", 7, t_labels),
        TestCase("docker-outputs", "Required outputs exposed", "Outputs", 6, t_outputs),
        TestCase("docker-usage", "Variables wired into resources", "Modularity", 5, t_usage),
    ],
)
