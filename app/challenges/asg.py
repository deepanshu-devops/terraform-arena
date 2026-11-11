"""Challenge 04 — Auto Scaling Web Tier (Hard)."""
from __future__ import annotations

import re

from .. import checks as C
from ..evaluator import Challenge, TestCase
from ..hcl import has_ref, norm, object_map, unquote


def t_provider(cfg):
    ok, msg = C.required_provider(cfg, "aws")
    if not ok:
        return False, msg
    provider = cfg.providers().get("aws")
    if not provider:
        return False, 'Missing provider "aws" configuration block.'
    return C.is_ref(provider, "region", "var.aws_region")


def t_ami_data(cfg):
    sources = cfg.data_sources("aws_ami")
    if not sources:
        return False, "Missing data source 'aws_ami' for the machine image."
    ami = sources[0]
    if not C.is_true(ami, "most_recent")[0]:
        return False, "data.aws_ami must set most_recent = true."
    owners = C.raw(ami, "owners") or ""
    if "amazon" not in owners:
        return False, "data.aws_ami owners must include \"amazon\"."
    filters = ami.nested("filter")
    if not filters:
        return False, "data.aws_ami should filter on the Amazon Linux image name."
    names = " ".join((C.raw(f, "name") or "") for f in filters)
    if "name" not in names:
        return False, "data.aws_ami filter should match on the image 'name'."
    return True, "AMI is discovered dynamically from Amazon."


def t_instance_var(cfg):
    ok, msg = C.variable_defined(
        cfg, "instance_type", expected_type="string", expected_default="t2.micro"
    )
    if not ok:
        return False, msg
    var = C.get_var(cfg, "instance_type")
    text = C.validation_text(var)
    allowed = ("t2.micro", "t3.micro", "t2.small", "t3.small")
    if "contains(" not in text or not any(a in text for a in allowed):
        return False, "instance_type must be validated against a free-tier allowlist."
    return True, "instance_type defaults to t2.micro and is allowlisted."


def t_asg_vars(cfg):
    for name, default in (("asg_min", 1), ("asg_max", 2), ("asg_desired", 1)):
        ok, msg = C.variable_defined(cfg, name, expected_type="number", expected_default=default)
        if not ok:
            return False, msg
    var = C.get_var(cfg, "asg_max")
    text = C.validation_text(var)
    if "4" not in text or ("<=" not in text and "<" not in text):
        return False, "asg_max needs validation to cap the fleet (e.g. <= 4)."
    return True, "ASG size variables are typed, defaulted and capped."


def t_security_group(cfg):
    sg = C.first_resource(cfg, "aws_security_group")
    if not sg:
        return False, "Missing aws_security_group resource."
    ingress = sg.nested("ingress")
    egress = sg.nested("egress")
    if not ingress:
        return False, "Security group has no ingress rules."
    http = None
    for rule in ingress:
        frm = C.raw(rule, "from_port")
        to = C.raw(rule, "to_port")
        if frm and to and norm(frm) == "80" and norm(to) == "80":
            http = rule
    if not http:
        return False, "Security group must allow HTTP on port 80."
    cidrs = C.raw(http, "cidr_blocks") or ""
    if "0.0.0.0/0" not in cidrs:
        return False, "Port 80 ingress must allow 0.0.0.0/0 for the public ALB."
    if not egress:
        return False, "Security group should define an egress rule."
    return True, "Security group allows HTTP/80 ingress and has egress."


def t_no_open_ssh(cfg):
    sg = C.first_resource(cfg, "aws_security_group")
    if not sg:
        return False, "Missing aws_security_group resource."
    for rule in sg.nested("ingress"):
        frm = C.raw(rule, "from_port") or ""
        to = C.raw(rule, "to_port") or ""
        cidrs = C.raw(rule, "cidr_blocks") or ""
        if norm(frm) == "22" and norm(to) == "22" and "0.0.0.0/0" in cidrs:
            return False, "SSH (22) must not be open to 0.0.0.0/0."
    return True, "No world-open SSH ingress."


def t_launch_template(cfg):
    lt = C.first_resource(cfg, "aws_launch_template")
    if not lt:
        return False, "Missing aws_launch_template resource."
    image = C.raw(lt, "image_id") or ""
    if "data.aws_ami." not in image:
        return False, f"Launch template image_id must use the AMI data source, found {image!r}."
    ok, msg = C.is_ref(lt, "instance_type", "var.instance_type")
    if not ok:
        return False, msg
    return True, "Launch template uses the discovered AMI and var.instance_type."


def t_imdsv2(cfg):
    lt = C.first_resource(cfg, "aws_launch_template")
    if not lt:
        return False, "Missing aws_launch_template resource."
    opts = lt.nested("metadata_options")
    if not opts:
        return False, "Launch template must configure metadata_options (IMDSv2)."
    tokens = C.raw(opts[0], "http_tokens")
    if "required" not in (tokens or ""):
        return False, "metadata_options.http_tokens must be 'required' (IMDSv2)."
    return True, "IMDSv2 is enforced via http_tokens = required."


def t_lt_tags(cfg):
    lt = C.first_resource(cfg, "aws_launch_template")
    if not lt:
        return False, "Missing aws_launch_template resource."
    specs = lt.nested("tag_specifications")
    if not specs:
        return False, "Launch template should tag instances via tag_specifications."
    tags = object_map(specs[0].attr("tags")) or {}
    missing = [k for k in ("Project", "Environment", "ManagedBy") if k not in tags]
    if missing:
        return False, "tag_specifications tags missing: " + ", ".join(missing)
    return True, "Instances launched by the template receive the standard tags."


def t_alb(cfg):
    alb = C.first_resource(cfg, "aws_lb")
    if not alb:
        return False, "Missing aws_lb resource."
    ok, msg = C.equals(alb, "load_balancer_type", '"application"')
    if not ok:
        return False, msg
    subnets = C.raw(alb, "subnets") or ""
    if "var.subnet_ids" not in subnets:
        return False, f"ALB subnets must reference var.subnet_ids, found {subnets!r}."
    if "aws_security_group." not in (C.raw(alb, "security_groups") or ""):
        return False, "ALB must use the managed security group."
    return True, "Application load balancer spans var.subnet_ids."


def t_target_group(cfg):
    tg = C.first_resource(cfg, "aws_lb_target_group")
    if not tg:
        return False, "Missing aws_lb_target_group resource."
    if norm(C.raw(tg, "port") or "") != "80":
        return False, "Target group port must be 80."
    if norm(C.raw(tg, "protocol") or "") != '"HTTP"':
        return False, "Target group protocol must be HTTP."
    if "var.vpc_id" not in (C.raw(tg, "vpc_id") or ""):
        return False, "Target group vpc_id must reference var.vpc_id."
    hc = tg.nested("health_check")
    if not hc:
        return False, "Target group is missing a health_check block."
    path = C.raw(hc[0], "path") or ""
    if "var.health_check_path" not in path and unquote(path) != "/":
        return False, "health_check.path must reference var.health_check_path."
    return True, "Target group is wired to port 80 with a parameterized health check."


def t_listener(cfg):
    listener = C.first_resource(cfg, "aws_lb_listener")
    if not listener:
        return False, "Missing aws_lb_listener resource."
    if norm(C.raw(listener, "port") or "") != "80":
        return False, "Listener must listen on port 80."
    if "aws_lb." not in (C.raw(listener, "load_balancer_arn") or ""):
        return False, "Listener must reference the aws_lb resource."
    actions = listener.nested("default_action")
    if not actions:
        return False, "Listener is missing default_action."
    forward = actions[0].nested("forward")
    targets = C.raw(actions[0], "target_group_arn") or ""
    if forward:
        targets = C.raw(forward[0], "target_group_arn") or targets
    if "aws_lb_target_group." not in targets:
        return False, "Listener default_action must forward to the target group."
    return True, "Listener forwards HTTP/80 to the target group."


def t_asg(cfg):
    asg = C.first_resource(cfg, "aws_autoscaling_group")
    if not asg:
        return False, "Missing aws_autoscaling_group resource."
    for attr, var in (("min_size", "var.asg_min"), ("max_size", "var.asg_max"), ("desired_capacity", "var.asg_desired")):
        if var not in (C.raw(asg, attr) or ""):
            return False, f"{attr} must reference {var}."
    if "var.subnet_ids" not in (C.raw(asg, "vpc_zone_identifier") or ""):
        return False, "ASG vpc_zone_identifier must reference var.subnet_ids."
    if "aws_lb_target_group." not in (C.raw(asg, "target_group_arns") or ""):
        return False, "ASG must register with the target group."
    if "ELB" not in (C.raw(asg, "health_check_type") or ""):
        return False, "ASG health_check_type should be ELB for the ALB."
    return True, "ASG scales across subnets and registers with the target group."


def t_asg_tags(cfg):
    asg = C.first_resource(cfg, "aws_autoscaling_group")
    if not asg:
        return False, "Missing aws_autoscaling_group resource."
    tags = {}
    for block in asg.nested("tag"):
        key = C.raw(block, "key")
        val = C.raw(block, "value")
        if key:
            tags[unquote(key) or key] = val
    dynamic = asg.nested("dynamic")
    missing = [k for k in ("Project", "Environment", "ManagedBy") if k not in tags]
    if missing and not dynamic:
        return False, "ASG tag blocks missing: " + ", ".join(missing)
    return True, "ASG propagates the standard tags to instances."


def t_outputs(cfg):
    missing = []
    for name in ("alb_dns_name", "asg_name", "security_group_id"):
        ok, msg = C.output_ok(cfg, name)
        if not ok:
            missing.append(msg)
    if missing:
        return False, "; ".join(missing)
    checks = {
        "alb_dns_name": "aws_lb.",
        "asg_name": "aws_autoscaling_group.",
        "security_group_id": "aws_security_group.",
    }
    for name, ref in checks.items():
        out = C.get_output(cfg, name)
        if out and ref not in (C.raw(out, "value") or ""):
            return False, f"Output {name} must reference {ref}"
    return True, "ALB, ASG and security-group outputs are exposed."


def t_tags(cfg):
    for rtype in ("aws_lb", "aws_security_group", "aws_lb_target_group"):
        res = C.first_resource(cfg, rtype)
        if not res:
            return False, f"Missing {rtype}."
        merged = C.effective_tags(cfg, res)
        for key in ("Project", "Environment", "ManagedBy"):
            if key not in merged:
                return False, f"{rtype} is missing tag '{key}'."
    return True, "ALB, target group and security group carry standard tags."


def t_usage(cfg):
    used = cfg.referenced_variables()
    missing = [
        n
        for n in ("vpc_id", "subnet_ids", "instance_type", "asg_min", "asg_max", "asg_desired")
        if n not in used
    ]
    if missing:
        return False, "Variables declared but not referenced: " + ", ".join(missing)
    return True, "Core variables are wired into resources."


CHALLENGE = Challenge(
    id="autoscaling-web-tier",
    number=4,
    title="Auto Scaling Web Tier",
    difficulty="Hard",
    points=250,
    tags=["aws", "alb", "autoscaling", "launch-template", "security"],
    scenario=(
        "Expose a stateless web tier behind an Application Load Balancer. The fleet must be "
        "built from a hardened launch template (IMDSv2 enforced), scale between configurable "
        "bounds across the provided subnets, and register automatically with an ALB target "
        "group. This is the production-shaped version of the classic 'web app on EC2' task."
    ),
    constraints=[
        "Provider: AWS with region from var.aws_region.",
        "Discover the Amazon Linux AMI through a data.aws_ami source (do not hardcode an AMI id).",
        "instance_type defaults to t2.micro and is validated against a free-tier allowlist.",
        "asg_min / asg_max / asg_desired are number variables; asg_max must be capped (<= 4).",
        "vpc_id (string) and subnet_ids (list(string)) are required inputs — no defaults.",
        "Security group must allow HTTP/80 from 0.0.0.0/0 and must not expose SSH/22 to the world.",
        "Launch template must enforce IMDSv2 (metadata_options.http_tokens = required) and tag instances.",
        "ALB must be application type, span var.subnet_ids and use the security group.",
        "Target group on HTTP/80 with a health check path from var.health_check_path.",
        "Listener forwards port 80 to the target group.",
        "ASG uses the size variables, spans var.subnet_ids, registers with the target group and uses ELB health checks.",
        "Outputs: alb_dns_name, asg_name, security_group_id.",
    ],
    variables=[
        {"name": "vpc_id", "type": "string", "default": None},
        {"name": "subnet_ids", "type": "list(string)", "default": None},
        {"name": "instance_type", "type": "string", "default": "t2.micro", "validation": True},
        {"name": "asg_min", "type": "number", "default": 1},
        {"name": "asg_max", "type": "number", "default": 2, "validation": True},
        {"name": "asg_desired", "type": "number", "default": 1},
        {"name": "health_check_path", "type": "string", "default": "/"},
        {"name": "aws_region", "type": "string", "default": "us-east-1"},
        {"name": "project_name", "type": "string", "default": "terraform-practice"},
        {"name": "environment", "type": "string", "default": "dev", "validation": True},
    ],
    expected_resources=[
        "aws_security_group",
        "aws_launch_template",
        "aws_lb",
        "aws_lb_target_group",
        "aws_lb_listener",
        "aws_autoscaling_group",
    ],
    expected_outputs=["alb_dns_name", "asg_name", "security_group_id"],
    starter={
        "versions.tf": "# versions.tf\n# TODO: terraform block + AWS provider.\n",
        "variables.tf": "# variables.tf\n# TODO: networking inputs, instance_type, ASG sizing, health_check_path, tags.\n",
        "main.tf": "# main.tf\n# TODO: AMI data source, SG, launch template, ALB, target group, listener, ASG.\n",
        "outputs.tf": "# outputs.tf\n# TODO: alb_dns_name, asg_name, security_group_id.\n",
    },
    allowlist=[
        "aws_security_group",
        "aws_launch_template",
        "aws_lb",
        "aws_lb_target_group",
        "aws_lb_listener",
        "aws_autoscaling_group",
        "aws_autoscaling_policy",
        "aws_cloudwatch_metric_alarm",
        "aws_eip",
        "aws_nat_gateway",
    ],
    data_allowlist=["aws_ami", "aws_availability_zones", "aws_region", "aws_caller_identity"],
    tests=[
        TestCase("asg-provider", "AWS provider + region variable", "Providers", 5, t_provider),
        TestCase("asg-ami", "AMI discovered via data source", "Resources", 6, t_ami_data),
        TestCase("asg-instance-var", "instance_type allowlisted", "Variables", 6, t_instance_var),
        TestCase("asg-sizing-vars", "ASG size variables validated", "Variables", 6, t_asg_vars),
        TestCase("asg-sg", "HTTP/80 ingress + egress", "Security", 8, t_security_group),
        TestCase("asg-ssh", "No world-open SSH", "Security", 6, t_no_open_ssh),
        TestCase("asg-lt", "Launch template wiring", "Resources", 7, t_launch_template),
        TestCase("asg-imdsv2", "IMDSv2 enforced", "Security", 8, t_imdsv2),
        TestCase("asg-lt-tags", "Instance tagging via tag_specifications", "Lifecycle", 6, t_lt_tags),
        TestCase("asg-alb", "Application LB across subnets", "Resources", 7, t_alb),
        TestCase("asg-tg", "Target group + health check", "Resources", 8, t_target_group),
        TestCase("asg-listener", "Listener forwards to target group", "Resources", 8, t_listener),
        TestCase("asg-asg", "ASG sizing, subnets and registration", "Resources", 9, t_asg),
        TestCase("asg-asg-tags", "ASG propagates standard tags", "Lifecycle", 5, t_asg_tags),
        TestCase("asg-outputs", "Required outputs exposed", "Outputs", 5, t_outputs),
        TestCase("asg-tags", "Core resources tagged", "Lifecycle", 5, t_tags),
        TestCase("asg-usage", "Variables wired into resources", "Modularity", 5, t_usage),
    ],
)
