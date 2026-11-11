"""Level 0: HCL foundations.

These scenarios are deliberately small.  Each one teaches a single syntactic
idea - blocks, arguments, strings, collections, files, providers and
formatting - while the surrounding file is already complete.
"""
from __future__ import annotations

from .reference import FOCUS_END, FOCUS_START
from .specs import T, V

LEVEL = 0
LEVEL_NAME = "Level 0 - HCL Foundations"


INTRO_SPECS: list[dict] = [
    {
        "id": "intro-hcl-blocks",
        "title": "Your First HCL Block",
        "difficulty": "Easy",
        "points": 40,
        "tags": ["terraform", "hcl", "syntax"],
        "scenario": (
            "HCL is built from blocks. A block has a type (here locals), no "
            "labels, and a body of arguments. Complete the locals block so the "
            "configuration records the application name."
        ),
        "constraints": [
            "Use a locals block.",
            'Define app_name with the value "terraform-arena".',
            "Keep the surrounding file valid HCL.",
        ],
        "variables": [],
        "expected_resources": [],
        "expected_outputs": [],
        "allowlist": [],
        "tests": [
            T("locals", "locals block exists", "Syntax", 10, kind="file_contains", text="locals"),
            T("app", "app_name is defined", "Syntax", 10, kind="file_contains", text="app_name"),
            T("value", "app_name uses the requested value", "Syntax", 10, kind="file_contains", text="terraform-arena"),
        ],
        "reference": {
            "main.tf": (
                "locals {\n"
                f"  {FOCUS_START}\n"
                '  app_name = "terraform-arena"\n'
                f"  {FOCUS_END}\n"
                "}\n"
            )
        },
        "focus": {
            "kind": "top",
            "file": "main.tf",
            "block": "locals",
            "title": "Complete the locals block",
            "todo": "Add the application name argument inside the block.",
        },
        "level": LEVEL,
        "level_name": LEVEL_NAME,
    },
    {
        "id": "intro-hcl-arguments",
        "title": "Arguments and Variable Blocks",
        "difficulty": "Easy",
        "points": 45,
        "tags": ["terraform", "hcl", "variables"],
        "scenario": (
            "Arguments are key/value pairs inside a block. Declare the app_name "
            "input variable with a description, a string type and a default."
        ),
        "constraints": [
            "Declare variable app_name.",
            "Type must be string.",
            'Default must be "terraform-arena".',
        ],
        "variables": [V("app_name", "string", "terraform-arena")],
        "expected_resources": [],
        "expected_outputs": [],
        "allowlist": [],
        "tests": [
            T(
                "var",
                "app_name is declared with type and default",
                "Variables",
                14,
                kind="var_defined",
                name="app_name",
                type="string",
                default="terraform-arena",
                validation=False,
            ),
            T("default", "default argument is present", "Syntax", 8, kind="file_contains", text="default"),
            T("assign", "assignment syntax is used", "Syntax", 8, kind="file_contains", text=" = "),
        ],
        "reference": {
            "variables.tf": (
                'variable "app_name" {\n'
                f"  {FOCUS_START}\n"
                '  description = "Application name."\n'
                "  type        = string\n"
                '  default     = "terraform-arena"\n'
                f"  {FOCUS_END}\n"
                "}\n"
            )
        },
        "focus": {
            "kind": "top",
            "file": "variables.tf",
            "block": "variable",
            "name": "app_name",
            "title": "Complete the variable block",
            "todo": "Add the description, type and default arguments.",
        },
        "level": LEVEL,
        "level_name": LEVEL_NAME,
    },
    {
        "id": "intro-hcl-strings",
        "title": "Strings and Interpolation",
        "difficulty": "Easy",
        "points": 45,
        "tags": ["terraform", "hcl", "strings"],
        "scenario": (
            "Strings are written in double quotes. Interpolation embeds an "
            "expression inside a string. Complete the greeting output."
        ),
        "constraints": [
            'Create output "greeting".',
            'The value must be "Hello, ${var.app_name}!".',
        ],
        "variables": [V("app_name", "string", "terraform-arena")],
        "expected_resources": [],
        "expected_outputs": ["greeting"],
        "allowlist": [],
        "tests": [
            T("out", "greeting output exists", "Outputs", 12, kind="output_exists", name="greeting"),
            T("interp", "the value uses interpolation", "Syntax", 12, kind="file_contains", text="${var.app_name}"),
            T("hello", "the value starts with Hello", "Syntax", 8, kind="file_contains", text="Hello,"),
        ],
        "reference": {
            "variables.tf": (
                'variable "app_name" {\n'
                '  description = "Application name."\n'
                "  type        = string\n"
                '  default     = "terraform-arena"\n'
                "}\n"
            ),
            "outputs.tf": (
                'output "greeting" {\n'
                f"  {FOCUS_START}\n"
                '  value = "Hello, ${var.app_name}!"\n'
                f"  {FOCUS_END}\n"
                "}\n"
            ),
        },
        "focus": {
            "kind": "top",
            "file": "outputs.tf",
            "block": "output",
            "name": "greeting",
            "title": "Complete the greeting output",
            "todo": "Write a quoted string that embeds the variable.",
        },
        "level": LEVEL,
        "level_name": LEVEL_NAME,
    },
    {
        "id": "intro-hcl-collections",
        "title": "Lists and Maps",
        "difficulty": "Easy",
        "points": 50,
        "tags": ["terraform", "hcl", "collections"],
        "scenario": (
            "Lists and maps are first-class HCL values. Define a list of subnet "
            "CIDRs and a map of tags in a locals block."
        ),
        "constraints": [
            "Define a subnets list with two CIDR strings.",
            "Define a tags map with Project and Environment keys.",
        ],
        "variables": [],
        "expected_resources": [],
        "expected_outputs": [],
        "allowlist": [],
        "tests": [
            T("subnets", "subnets list exists", "Syntax", 10, kind="file_contains", text="subnets"),
            T("cidr", "first CIDR is present", "Syntax", 9, kind="file_contains", text="10.0.1.0/24"),
            T("tags", "tags map exists", "Syntax", 10, kind="file_contains", text="tags"),
            T("project", "Project key is present", "Syntax", 8, kind="file_contains", text="Project"),
            T("environment", "Environment key is present", "Syntax", 8, kind="file_contains", text="Environment"),
        ],
        "reference": {
            "main.tf": (
                "locals {\n"
                f"  {FOCUS_START}\n"
                '  subnets = ["10.0.1.0/24", "10.0.2.0/24"]\n'
                "  tags = {\n"
                '    Project     = "arena"\n'
                '    Environment = "dev"\n'
                "  }\n"
                f"  {FOCUS_END}\n"
                "}\n"
            )
        },
        "focus": {
            "kind": "top",
            "file": "main.tf",
            "block": "locals",
            "title": "Complete the collections",
            "todo": "Add the subnet list and the tag map.",
        },
        "level": LEVEL,
        "level_name": LEVEL_NAME,
    },
    {
        "id": "intro-provider-block",
        "title": "Provider and Version Blocks",
        "difficulty": "Easy",
        "points": 50,
        "tags": ["terraform", "providers", "versions"],
        "scenario": (
            "The terraform block declares required providers and versions. The "
            "provider block configures AWS. Complete the provider block so the "
            "region comes from a variable."
        ),
        "constraints": [
            "Require hashicorp/aws in versions.tf.",
            "Configure provider aws with region = var.aws_region.",
            "Declare aws_region with a default of us-east-1.",
        ],
        "variables": [V("aws_region", "string", "us-east-1")],
        "expected_resources": [],
        "expected_outputs": [],
        "allowlist": [],
        "tests": [
            T("req", "AWS provider is required", "Providers", 12, kind="required_provider", name="aws"),
            T(
                "provider",
                "provider region comes from a variable",
                "Providers",
                12,
                kind="provider_ref",
                provider="aws",
                attr="region",
                ref="var.aws_region",
            ),
            T(
                "var",
                "aws_region is declared",
                "Variables",
                8,
                kind="var_defined",
                name="aws_region",
                type="string",
                default="us-east-1",
                validation=False,
            ),
        ],
        "reference": {
            "versions.tf": (
                "terraform {\n"
                '  required_version = ">= 1.5.0"\n'
                "  required_providers {\n"
                "    aws = {\n"
                '      source  = "hashicorp/aws"\n'
                '      version = "~> 5.0"\n'
                "    }\n"
                "  }\n"
                "}\n"
            ),
            "variables.tf": (
                'variable "aws_region" {\n'
                '  description = "AWS region."\n'
                "  type        = string\n"
                '  default     = "us-east-1"\n'
                "}\n"
            ),
            "main.tf": (
                'provider "aws" {\n'
                f"  {FOCUS_START}\n"
                "  region = var.aws_region\n"
                f"  {FOCUS_END}\n"
                "}\n"
            ),
        },
        "focus": {
            "kind": "top",
            "file": "main.tf",
            "block": "provider",
            "name": "aws",
            "title": "Complete the provider block",
            "todo": "Set the provider region from the declared variable.",
        },
        "level": LEVEL,
        "level_name": LEVEL_NAME,
    },
    {
        "id": "intro-hcl-formatting",
        "title": "Format HCL by Hand",
        "difficulty": "Easy",
        "points": 50,
        "tags": ["terraform", "hcl", "formatting"],
        "scenario": (
            "Terraform style is two spaces per level, no tabs, and a final "
            "newline. The block below works but is badly formatted. Fix it, or "
            "run terraform fmt, so the formatting check passes."
        ),
        "constraints": [
            "Use two-space indentation.",
            "Replace tabs with spaces.",
            "Keep app_name defined as terraform-arena.",
        ],
        "variables": [],
        "expected_resources": [],
        "expected_outputs": [],
        "allowlist": [],
        "tests": [
            T("fmt", "Formatting is clean", "Formatting", 20, kind="formatting_clean"),
            T("app", "app_name is still defined", "Syntax", 8, kind="file_contains", text="app_name"),
        ],
        "reference": {
            "main.tf": 'locals {\n  app_name = "terraform-arena"\n}\n'
        },
        "starter_override": {
            "main.tf": 'locals {\n\tapp_name = "terraform-arena"\n  }\n'
        },
        "focus": {
            "kind": "top",
            "file": "main.tf",
            "block": "locals",
            "title": "Fix the formatting",
            "todo": "Replace the tab and correct the indentation.",
        },
        "level": LEVEL,
        "level_name": LEVEL_NAME,
    },
    {
        "id": "intro-file-layout",
        "title": "Split a Configuration Across Files",
        "difficulty": "Easy",
        "points": 55,
        "tags": ["terraform", "files", "layout"],
        "scenario": (
            "Terraform reads every .tf file in a directory as one configuration. "
            "The versions, variables and outputs files are complete; finish the "
            "resource in main.tf."
        ),
        "constraints": [
            "Keep the provider and versions in versions.tf.",
            "Use var.app_name for the bucket name.",
            "bucket_id must reference the bucket.",
        ],
        "variables": [V("app_name", "string", "terraform-arena"), V("aws_region", "string", "us-east-1")],
        "expected_resources": ["aws_s3_bucket"],
        "expected_outputs": ["bucket_id"],
        "allowlist": ["aws_s3_bucket"],
        "tests": [
            T(
                "var",
                "app_name is declared",
                "Variables",
                8,
                kind="var_defined",
                name="app_name",
                type="string",
                default="terraform-arena",
                validation=False,
            ),
            T("bucket", "bucket is provisioned", "Resources", 10, kind="resource_exists", type="aws_s3_bucket"),
            T(
                "name",
                "bucket name comes from the variable",
                "Resources",
                12,
                kind="attr_ref",
                resource="aws_s3_bucket",
                attr="bucket",
                ref="var.app_name",
            ),
            T("out", "bucket_id output", "Outputs", 8, kind="output_ref", name="bucket_id", ref="aws_s3_bucket."),
        ],
        "reference": {
            "versions.tf": (
                "terraform {\n"
                '  required_version = ">= 1.5.0"\n'
                "  required_providers {\n"
                "    aws = {\n"
                '      source  = "hashicorp/aws"\n'
                '      version = "~> 5.0"\n'
                "    }\n"
                "  }\n"
                "}\n"
            ),
            "variables.tf": (
                'variable "app_name" {\n'
                '  description = "Application name."\n'
                "  type        = string\n"
                '  default     = "terraform-arena"\n'
                "}\n"
                "\n"
                'variable "aws_region" {\n'
                '  description = "AWS region."\n'
                "  type        = string\n"
                '  default     = "us-east-1"\n'
                "}\n"
            ),
            "main.tf": (
                'provider "aws" {\n'
                "  region = var.aws_region\n"
                "}\n"
                "\n"
                'resource "aws_s3_bucket" "this" {\n'
                f"  {FOCUS_START}\n"
                "  bucket = var.app_name\n"
                f"  {FOCUS_END}\n"
                "}\n"
            ),
            "outputs.tf": (
                'output "bucket_id" {\n'
                "  value = aws_s3_bucket.this.id\n"
                "}\n"
            ),
        },
        "focus": {
            "kind": "resource",
            "file": "main.tf",
            "rtype": "aws_s3_bucket",
            "name": "this",
            "title": "Complete the bucket resource",
            "todo": "Set the bucket argument from the input variable.",
        },
        "level": LEVEL,
        "level_name": LEVEL_NAME,
    },
]

__all__ = ["INTRO_SPECS", "LEVEL", "LEVEL_NAME"]
