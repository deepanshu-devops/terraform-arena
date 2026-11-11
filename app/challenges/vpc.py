"""Challenge 03 — Highly Available VPC Foundation (Medium)."""
from __future__ import annotations

import re

from .. import checks as C
from ..evaluator import Challenge, TestCase
from ..hcl import Block, has_ref, literal, norm, unquote


def _declared_count(block: Block) -> int:
    count = C.raw(block, "count")
    if count:
        kind, val = literal(count)
        if kind == "number":
            return int(val)
        return 2  # dynamic count expression — assume multi
    if C.present(block, "for_each"):
        return 2
    return 1


def t_provider(cfg):
    ok, msg = C.required_provider(cfg, "aws")
    if not ok:
        return False, msg
    if "aws" not in cfg.providers():
        return False, 'Missing provider "aws" configuration block.'
    provider = cfg.providers()["aws"]
    return C.is_ref(provider, "region", "var.aws_region")


def t_vpc_cidr_var(cfg):
    ok, msg = C.variable_defined(
        cfg, "vpc_cidr", expected_type="string", expected_default="10.0.0.0/16"
    )
    if not ok:
        return False, msg
    var = C.get_var(cfg, "vpc_cidr")
    text = C.validation_text(var)
    pats = re.findall(r'"([^"]*)"', text or "")
    valid = (
        "cidrhost(" in text
        or "cidrnetmask(" in text
        or any("/" in p and ("\\d" in p or "0-9" in p) for p in pats)
    )
    if not valid:
        return False, "vpc_cidr needs CIDR validation (can(cidrnetmask(...)) or a CIDR regex)."
    return True, "vpc_cidr defaults to 10.0.0.0/16 with CIDR validation."


def t_vpc(cfg):
    vpc = C.first_resource(cfg, "aws_vpc")
    if not vpc:
        return False, "Missing aws_vpc resource."
    ok, msg = C.is_ref(vpc, "cidr_block", "var.vpc_cidr")
    if not ok:
        return False, msg
    if not C.is_true(vpc, "enable_dns_support")[0]:
        return False, "enable_dns_support must be true."
    if not C.is_true(vpc, "enable_dns_hostnames")[0]:
        return False, "enable_dns_hostnames must be true."
    return True, "VPC uses var.vpc_cidr with DNS support and hostnames enabled."


def t_subnets(cfg):
    subnets = cfg.resources("aws_subnet")
    if not subnets:
        return False, "Missing aws_subnet resources."
    total = sum(_declared_count(s) for s in subnets)
    if total < 2:
        return False, f"Only {total} public subnet(s) declared; at least 2 are required."
    for subnet in subnets:
        cidr = C.raw(subnet, "cidr_block") or ""
        if not (
            has_ref(cidr, "var.vpc_cidr")
            or has_ref(cidr, "var.public_subnet_cidrs")
            or "cidrsubnet(" in cidr
            or "var.public_subnet" in cidr
        ):
            return False, f"Subnet CIDR must be derived from a variable, found {cidr!r}."
    return True, f"{total} public subnets derive CIDRs from variables."


def t_subnet_azs(cfg):
    subnets = cfg.resources("aws_subnet")
    if not subnets:
        return False, "Missing aws_subnet resources."
    dynamic = False
    literals: list[str] = []
    for subnet in subnets:
        az = C.raw(subnet, "availability_zone") or ""
        if (
            has_ref(az, "var.availability_zones")
            or "data.aws_availability_zones" in az
            or "each." in az
            or ("count.index" in az and "var." in az)
        ):
            dynamic = True
        else:
            kind, val = literal(az)
            if kind == "string":
                literals.append(val)
    if dynamic:
        return True, "Subnets spread across AZs from a dynamic AZ source."
    if len(set(literals)) >= 2:
        return True, f"Subnets use distinct literal AZs: {', '.join(sorted(set(literals)))}."
    return False, "Subnets must spread across at least two availability zones."


def t_subnet_public(cfg):
    subnets = cfg.resources("aws_subnet")
    if not subnets:
        return False, "Missing aws_subnet resources."
    missing = []
    for subnet in subnets:
        raw = C.raw(subnet, "map_public_ip_on_launch")
        if raw is None or norm(raw) != "true":
            missing.append(subnet.labels[1] if len(subnet.labels) > 1 else "subnet")
    if missing:
        return False, "map_public_ip_on_launch must be true for: " + ", ".join(missing)
    return True, "Public subnets auto-assign public IPs."


def t_igw(cfg):
    igw = C.first_resource(cfg, "aws_internet_gateway")
    if not igw:
        return False, "Missing aws_internet_gateway resource."
    vpc = C.raw(igw, "vpc_id") or ""
    if "aws_vpc." not in vpc:
        return False, f"Internet gateway must attach to the VPC, found vpc_id={vpc!r}."
    return True, "Internet gateway is attached to the VPC."


def t_route_table(cfg):
    rt = C.first_resource(cfg, "aws_route_table")
    if not rt:
        return False, "Missing aws_route_table resource."
    if "aws_vpc." not in (C.raw(rt, "vpc_id") or ""):
        return False, "Route table must belong to the VPC."
    routes = rt.nested("route")
    if not routes:
        return False, "Route table has no route block."
    default = None
    for route in routes:
        cidr = C.raw(route, "cidr_block")
        if cidr and unquote(cidr) == "0.0.0.0/0":
            default = route
            break
    if not default:
        return False, "Missing default route 0.0.0.0/0."
    gateway = C.raw(default, "gateway_id") or ""
    if "aws_internet_gateway." not in gateway:
        return False, f"Default route must target the internet gateway, found {gateway!r}."
    return True, "Route table sends 0.0.0.0/0 to the internet gateway."


def t_associations(cfg):
    assocs = cfg.resources("aws_route_table_association")
    if not assocs:
        return False, "Missing aws_route_table_association resources."
    total = sum(_declared_count(a) for a in assocs)
    if total < 2:
        return False, f"Only {total} route table association(s); every public subnet needs one."
    for assoc in assocs:
        subnet = C.raw(assoc, "subnet_id") or ""
        rt = C.raw(assoc, "route_table_id") or ""
        if "aws_subnet." not in subnet:
            return False, f"Association subnet_id must reference aws_subnet, found {subnet!r}."
        if "aws_route_table." not in rt:
            return False, f"Association route_table_id must reference aws_route_table, found {rt!r}."
    return True, f"{total} associations link public subnets to the route table."


def t_outputs(cfg):
    missing = []
    for name in ("vpc_id", "public_subnet_ids", "internet_gateway_id"):
        ok, msg = C.output_ok(cfg, name)
        if not ok:
            missing.append(msg)
    if missing:
        return False, "; ".join(missing)
    vpc_out = C.get_output(cfg, "vpc_id")
    if vpc_out and "aws_vpc." not in (C.raw(vpc_out, "value") or ""):
        return False, "vpc_id output must reference the aws_vpc resource."
    subnet_out = C.get_output(cfg, "public_subnet_ids")
    if subnet_out and "aws_subnet." not in (C.raw(subnet_out, "value") or ""):
        return False, "public_subnet_ids output must reference aws_subnet."
    return True, "VPC, subnet and gateway outputs are exposed."


def t_tags(cfg):
    required = {
        "Project": "var.project_name",
        "Environment": "var.environment",
        "ManagedBy": '"terraform"',
    }
    issues = []
    for rtype in ("aws_vpc", "aws_subnet", "aws_internet_gateway", "aws_route_table"):
        res = C.first_resource(cfg, rtype)
        if not res:
            continue
        merged = C.effective_tags(cfg, res)
        for key, expected in required.items():
            if key not in merged:
                issues.append(f"{rtype}: missing tag {key}")
            elif norm(merged[key]) != norm(expected):
                issues.append(f"{rtype}: tag {key} expected {expected!r}, found {merged[key]!r}")
    if issues:
        return False, "; ".join(issues[:8])
    return True, "Core VPC resources carry consistent tags."


def t_no_open_ingress(cfg):
    for sg in cfg.resources("aws_security_group"):
        for rule in sg.nested("ingress"):
            cidrs = C.raw(rule, "cidr_blocks") or ""
            if "0.0.0.0/0" in cidrs and ("22" in (C.raw(rule, "from_port") or "") and "22" in (C.raw(rule, "to_port") or "")):
                return False, "SSH (22) open to 0.0.0.0/0 is blocked by policy."
    return True, "No world-open SSH ingress detected."


def t_usage(cfg):
    used = cfg.referenced_variables()
    missing = [n for n in ("vpc_cidr", "aws_region", "project_name", "environment") if n not in used]
    if missing:
        return False, "Variables declared but not referenced: " + ", ".join(missing)
    return True, "Core variables are wired into resources."


CHALLENGE = Challenge(
    id="ha-vpc-foundation",
    number=3,
    title="Highly Available VPC Foundation",
    difficulty="Medium",
    points=150,
    tags=["aws", "vpc", "networking", "count", "for_each"],
    scenario=(
        "Your platform team is standardising network foundations. Build a reusable VPC with "
        "two public subnets spread across distinct availability zones, an internet gateway, "
        "a public route table with a default route, and associations for every subnet. "
        "Everything must be parameterized so the same code can be reused per environment."
    ),
    constraints=[
        "Provider: AWS (hashicorp/aws) with region from var.aws_region.",
        "vpc_cidr must default to 10.0.0.0/16 and be validated as a CIDR.",
        "Create exactly one aws_vpc with DNS support and DNS hostnames enabled.",
        "Create at least two aws_subnet resources across distinct AZs (use count/for_each, not copy-paste).",
        "Subnet CIDRs must be derived from variables (cidrsubnet or a CIDR list) — no magic literals.",
        "Public subnets must set map_public_ip_on_launch = true.",
        "Attach one internet gateway and one route table with a 0.0.0.0/0 default route to the gateway.",
        "Create a route table association for every public subnet.",
        "Tag VPC, subnets, gateway and route table with Project, Environment, ManagedBy = \"terraform\".",
        "Outputs: vpc_id, public_subnet_ids, internet_gateway_id.",
    ],
    variables=[
        {"name": "vpc_cidr", "type": "string", "default": "10.0.0.0/16", "validation": True},
        {"name": "public_subnet_cidrs", "type": "list(string)", "default": ["10.0.1.0/24", "10.0.2.0/24"]},
        {"name": "availability_zones", "type": "list(string)", "default": ["us-east-1a", "us-east-1b"]},
        {"name": "aws_region", "type": "string", "default": "us-east-1"},
        {"name": "project_name", "type": "string", "default": "terraform-practice"},
        {"name": "environment", "type": "string", "default": "dev", "validation": True},
    ],
    expected_resources=[
        "aws_vpc",
        "aws_subnet",
        "aws_internet_gateway",
        "aws_route_table",
        "aws_route_table_association",
    ],
    expected_outputs=["vpc_id", "public_subnet_ids", "internet_gateway_id"],
    starter={
        "versions.tf": "# versions.tf\n# TODO: terraform block + AWS provider.\n",
        "variables.tf": "# variables.tf\n# TODO: vpc_cidr, public_subnet_cidrs, availability_zones, aws_region, project_name, environment.\n",
        "main.tf": "# main.tf\n# TODO: VPC, public subnets, internet gateway, route table and associations.\n",
        "outputs.tf": "# outputs.tf\n# TODO: vpc_id, public_subnet_ids, internet_gateway_id.\n",
    },
    allowlist=[
        "aws_vpc",
        "aws_subnet",
        "aws_internet_gateway",
        "aws_route_table",
        "aws_route_table_association",
        "aws_security_group",
        "aws_eip",
        "aws_nat_gateway",
    ],
    data_allowlist=["aws_availability_zones", "aws_region", "aws_caller_identity"],
    tests=[
        TestCase("vpc-provider", "AWS provider + region variable", "Providers", 6, t_provider),
        TestCase("vpc-cidr-var", "vpc_cidr default + CIDR validation", "Variables", 8, t_vpc_cidr_var),
        TestCase("vpc-resource", "VPC with DNS support/hostnames", "Resources", 7, t_vpc),
        TestCase("vpc-subnets", "Two+ subnets with variable-derived CIDRs", "Resources", 9, t_subnets),
        TestCase("vpc-azs", "Subnets spread across AZs", "Lifecycle", 8, t_subnet_azs),
        TestCase("vpc-public", "Public subnets auto-assign IPs", "Security", 6, t_subnet_public),
        TestCase("vpc-igw", "Internet gateway attached", "Resources", 6, t_igw),
        TestCase("vpc-route", "Default route to internet gateway", "Resources", 8, t_route_table),
        TestCase("vpc-assoc", "Association for every subnet", "Resources", 9, t_associations),
        TestCase("vpc-outputs", "Required outputs exposed", "Outputs", 6, t_outputs),
        TestCase("vpc-tags", "Consistent resource tags", "Lifecycle", 6, t_tags),
        TestCase("vpc-ssh", "No world-open SSH ingress", "Security", 5, t_no_open_ingress),
        TestCase("vpc-usage", "Variables wired into resources", "Modularity", 5, t_usage),
    ],
)
