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
    {
        "id": "intro-local-values",
        "title": "Local Values and References",
        "difficulty": "Easy",
        "points": 56,
        "tags": ["terraform", "hcl", "locals"],
        "scenario": (
            "Local values name expressions so they can be reused without turning "
            "them into input variables. Declare the project name and derive a "
            "bucket name from it."
        ),
        "constraints": [
            'Set local.project to "arena".',
            'Derive local.bucket_name as "${local.project}-logs".',
            "Use references rather than repeating the literal value.",
        ],
        "variables": [],
        "expected_resources": [],
        "expected_outputs": [],
        "allowlist": [],
        "tests": [
            T("project", "project local is defined", "Syntax", 10, kind="file_contains", text="local.project"),
            T("bucket", "bucket_name local is defined", "Syntax", 10, kind="file_contains", text="bucket_name"),
            T(
                "reference",
                "bucket_name references local.project",
                "Syntax",
                12,
                kind="file_contains",
                text="${local.project}-logs",
            ),
        ],
        "reference": {
            "main.tf": (
                "locals {\n"
                f"  {FOCUS_START}\n"
                '  project     = "arena"\n'
                '  bucket_name = "${local.project}-logs"\n'
                f"  {FOCUS_END}\n"
                "}\n"
            )
        },
        "focus": {
            "kind": "top",
            "file": "main.tf",
            "block": "locals",
            "title": "Add the local values",
            "todo": "Define project and derive bucket_name with an interpolation.",
        },
        "level": LEVEL,
        "level_name": LEVEL_NAME,
    },
    {
        "id": "intro-conditional",
        "title": "Conditional Expressions",
        "difficulty": "Easy",
        "points": 57,
        "tags": ["terraform", "hcl", "expressions"],
        "scenario": (
            "A conditional expression chooses one of two values: "
            "condition ? true_value : false_value. Use the environment variable "
            "to pick a production flag and a log-retention period."
        ),
        "constraints": [
            'Treat "prod" as production.',
            "Set log retention to 30 days in production and 7 otherwise.",
            "Derive both values in the locals block.",
        ],
        "variables": [V("environment", "string", "dev")],
        "expected_resources": [],
        "expected_outputs": [],
        "allowlist": [],
        "tests": [
            T(
                "condition",
                "production condition is present",
                "Syntax",
                12,
                kind="file_contains",
                text='var.environment == "prod"',
            ),
            T("flag", "is_production local is defined", "Syntax", 8, kind="file_contains", text="is_production"),
            T("retention", "retention local is defined", "Syntax", 8, kind="file_contains", text="log_retention"),
            T("days", "both retention values are present", "Syntax", 8, kind="file_contains", text="30 : 7"),
        ],
        "reference": {
            "variables.tf": (
                'variable "environment" {\n'
                '  description = "Deployment environment."\n'
                "  type        = string\n"
                '  default     = "dev"\n'
                "}\n"
            ),
            "main.tf": (
                "locals {\n"
                f"  {FOCUS_START}\n"
                '  is_production = var.environment == "prod" ? true : false\n'
                "  log_retention = local.is_production ? 30 : 7\n"
                f"  {FOCUS_END}\n"
                "}\n"
            ),
        },
        "focus": {
            "kind": "top",
            "file": "main.tf",
            "block": "locals",
            "title": "Add the conditional locals",
            "todo": "Compare the environment and choose retention values.",
        },
        "level": LEVEL,
        "level_name": LEVEL_NAME,
    },
    {
        "id": "intro-for-expression",
        "title": "For Expressions",
        "difficulty": "Easy",
        "points": 58,
        "tags": ["terraform", "hcl", "expressions"],
        "scenario": (
            "For expressions transform collections without a loop block. Build a "
            "list of upper-case names and a map from each name to its upper-case "
            "form."
        ),
        "constraints": [
            "Use a list for expression with upper(name).",
            "Use a map for expression with name => upper(name).",
            "Derive both from var.names.",
        ],
        "variables": [V("names", "list(string)", ["web", "api"])],
        "expected_resources": [],
        "expected_outputs": [],
        "allowlist": [],
        "tests": [
            T("list", "list for expression is present", "Syntax", 12, kind="file_contains", text="[for name in var.names"),
            T("map", "map for expression is present", "Syntax", 12, kind="file_contains", text="name => upper(name)"),
            T("upper", "upper function is used", "Syntax", 8, kind="file_contains", text="upper(name)"),
        ],
        "reference": {
            "variables.tf": (
                'variable "names" {\n'
                '  description = "Service names."\n'
                "  type        = list(string)\n"
                '  default     = ["web", "api"]\n'
                "}\n"
            ),
            "main.tf": (
                "locals {\n"
                f"  {FOCUS_START}\n"
                "  upper_names = [for name in var.names : upper(name)]\n"
                "  name_map    = { for name in var.names : name => upper(name) }\n"
                f"  {FOCUS_END}\n"
                "}\n"
            ),
        },
        "focus": {
            "kind": "top",
            "file": "main.tf",
            "block": "locals",
            "title": "Transform the names",
            "todo": "Write list and map for expressions over var.names.",
        },
        "level": LEVEL,
        "level_name": LEVEL_NAME,
    },
    {
        "id": "intro-functions",
        "title": "Built-in Functions",
        "difficulty": "Easy",
        "points": 59,
        "tags": ["terraform", "hcl", "functions"],
        "scenario": (
            "Terraform ships with functions for strings, collections, numbers and "
            "encoding. Normalise a bucket name with lower() and take a short "
            "prefix with substr()."
        ),
        "constraints": [
            "Use lower() to build the bucket name.",
            "Use substr() to derive a short name.",
            "Reference local.bucket_name from the short name.",
        ],
        "variables": [V("project_name", "string", "Terraform-Arena")],
        "expected_resources": [],
        "expected_outputs": [],
        "allowlist": [],
        "tests": [
            T("lower", "lower function is used", "Syntax", 10, kind="file_contains", text="lower("),
            T("substr", "substr function is used", "Syntax", 10, kind="file_contains", text="substr("),
            T(
                "reference",
                "short name references the bucket name",
                "Syntax",
                10,
                kind="file_contains",
                text="local.bucket_name",
            ),
            T("suffix", "bucket suffix is present", "Syntax", 6, kind="file_contains", text="-LOGS"),
        ],
        "reference": {
            "variables.tf": (
                'variable "project_name" {\n'
                '  description = "Project name."\n'
                "  type        = string\n"
                '  default     = "Terraform-Arena"\n'
                "}\n"
            ),
            "main.tf": (
                "locals {\n"
                f"  {FOCUS_START}\n"
                '  bucket_name = lower("${var.project_name}-LOGS")\n'
                "  short_name  = substr(local.bucket_name, 0, 10)\n"
                f"  {FOCUS_END}\n"
                "}\n"
            ),
        },
        "focus": {
            "kind": "top",
            "file": "main.tf",
            "block": "locals",
            "title": "Normalise the bucket name",
            "todo": "Use lower and substr in the locals block.",
        },
        "level": LEVEL,
        "level_name": LEVEL_NAME,
    },
    {
        "id": "intro-null-default",
        "title": "Optional Values With coalesce",
        "difficulty": "Easy",
        "points": 60,
        "tags": ["terraform", "hcl", "functions"],
        "scenario": (
            "Variables can default to null to represent an optional value. Use "
            "coalesce() to fall back to a friendly default when the caller does "
            "not provide a nickname."
        ),
        "constraints": [
            "Declare nickname with a null default.",
            'Use coalesce(var.nickname, "learner") in a local value.',
            "Name the local display_name.",
        ],
        "variables": [V("nickname", "string", None)],
        "expected_resources": [],
        "expected_outputs": [],
        "allowlist": [],
        "tests": [
            T("null", "nickname defaults to null", "Variables", 8, kind="var_attr", name="nickname", attr="default", equals="null"),
            T(
                "coalesce",
                "coalesce is used",
                "Syntax",
                12,
                kind="file_contains",
                text="coalesce(var.nickname",
            ),
            T("local", "display_name local is defined", "Syntax", 8, kind="file_contains", text="display_name"),
        ],
        "reference": {
            "variables.tf": (
                'variable "nickname" {\n'
                '  description = "Optional display name."\n'
                "  type        = string\n"
                "  default     = null\n"
                "}\n"
            ),
            "main.tf": (
                "locals {\n"
                f"  {FOCUS_START}\n"
                '  display_name = coalesce(var.nickname, "learner")\n'
                f"  {FOCUS_END}\n"
                "}\n"
            ),
        },
        "focus": {
            "kind": "top",
            "file": "main.tf",
            "block": "locals",
            "title": "Add the fallback value",
            "todo": "Use coalesce with the optional variable and a default string.",
        },
        "level": LEVEL,
        "level_name": LEVEL_NAME,
    },
    {
        "id": "intro-splat-expression",
        "title": "Splat Expressions",
        "difficulty": "Easy",
        "points": 61,
        "tags": ["terraform", "hcl", "expressions"],
        "scenario": (
            "Splat expressions extract one attribute from every object in a list, "
            "and index syntax reads a single object. Build a list of names and "
            "the first instance's private IP."
        ),
        "constraints": [
            "Use var.instances[*].name for the name list.",
            "Use var.instances[0].private_ip for the primary IP.",
            "Keep both values in the locals block.",
        ],
        "variables": [],
        "expected_resources": [],
        "expected_outputs": [],
        "allowlist": [],
        "tests": [
            T("names", "splat expression is present", "Syntax", 12, kind="file_contains", text="var.instances[*].name"),
            T(
                "index",
                "index expression is present",
                "Syntax",
                12,
                kind="file_contains",
                text="var.instances[0].private_ip",
            ),
            T("local", "instance_names local is defined", "Syntax", 8, kind="file_contains", text="instance_names"),
        ],
        "reference": {
            "variables.tf": (
                'variable "instances" {\n'
                '  description = "Instance metadata."\n'
                "  type = list(object({\n"
                "    name       = string\n"
                "    private_ip = string\n"
                "  }))\n"
                "  default = [\n"
                '    { name = "web", private_ip = "10.0.1.10" },\n'
                '    { name = "api", private_ip = "10.0.2.10" },\n'
                "  ]\n"
                "}\n"
            ),
            "main.tf": (
                "locals {\n"
                f"  {FOCUS_START}\n"
                "  instance_names = var.instances[*].name\n"
                "  primary_ip     = var.instances[0].private_ip\n"
                f"  {FOCUS_END}\n"
                "}\n"
            ),
        },
        "focus": {
            "kind": "top",
            "file": "main.tf",
            "block": "locals",
            "title": "Extract instance attributes",
            "todo": "Use a splat for every name and index for the first IP.",
        },
        "level": LEVEL,
        "level_name": LEVEL_NAME,
    },
    {
        "id": "intro-sensitive-output",
        "title": "Sensitive Outputs",
        "difficulty": "Easy",
        "points": 62,
        "tags": ["terraform", "hcl", "outputs", "security"],
        "scenario": (
            "Outputs can carry secrets. Mark a token output sensitive so Terraform "
            "redacts it in plan and apply output while still making the value "
            "available to the caller."
        ),
        "constraints": [
            "Declare an output named session_token.",
            "Set value to var.session_token.",
            "Mark the output sensitive.",
        ],
        "variables": [V("session_token", "string", "demo-token")],
        "expected_outputs": ["session_token"],
        "allowlist": [],
        "tests": [
            T("out", "session_token output exists", "Outputs", 10, kind="output_exists", name="session_token"),
            T(
                "ref",
                "output uses the variable",
                "Outputs",
                10,
                kind="output_ref",
                name="session_token",
                ref="var.session_token",
            ),
            T("sensitive", "output is marked sensitive", "Security", 10, kind="output_attr", name="session_token", attr="sensitive", equals="true"),
        ],
        "reference": {
            "variables.tf": (
                'variable "session_token" {\n'
                '  description = "Demo session token."\n'
                "  type        = string\n"
                '  default     = "demo-token"\n'
                "}\n"
            ),
            "outputs.tf": (
                'output "session_token" {\n'
                f"  {FOCUS_START}\n"
                '  description = "Session token for the caller."\n'
                "  value       = var.session_token\n"
                "  sensitive   = true\n"
                f"  {FOCUS_END}\n"
                "}\n"
            ),
        },
        "focus": {
            "kind": "top",
            "file": "outputs.tf",
            "block": "output",
            "name": "session_token",
            "title": "Complete the sensitive output",
            "todo": "Set the value from the variable and mark the output sensitive.",
        },
        "level": LEVEL,
        "level_name": LEVEL_NAME,
    },
    {
        "id": "intro-resource-tags",
        "title": "Resource Arguments and Tags",
        "difficulty": "Easy",
        "points": 63,
        "tags": ["terraform", "hcl", "resources", "tags"],
        "scenario": (
            "Resources are blocks with a type and a name. Complete an S3 bucket "
            "so the bucket name comes from a variable and the resource carries a "
            "Project tag."
        ),
        "constraints": [
            "Keep the aws_s3_bucket resource.",
            "Set bucket from var.bucket_name.",
            'Add a tags map with Project = "arena".',
        ],
        "variables": [V("bucket_name", "string", "terraform-arena-logs")],
        "expected_resources": ["aws_s3_bucket"],
        "allowlist": ["aws_s3_bucket"],
        "tests": [
            T("bucket", "bucket is provisioned", "Resources", 10, kind="resource_exists", type="aws_s3_bucket"),
            T(
                "name",
                "bucket name comes from the variable",
                "Resources",
                12,
                kind="attr_ref",
                resource="aws_s3_bucket",
                attr="bucket",
                ref="var.bucket_name",
            ),
            T(
                "tags",
                "Project tag is present",
                "Security",
                8,
                kind="tagged",
                resources=["aws_s3_bucket"],
                tags={"Project": '"arena"'},
            ),
        ],
        "reference": {
            "variables.tf": (
                'variable "bucket_name" {\n'
                '  description = "Bucket name."\n'
                "  type        = string\n"
                '  default     = "terraform-arena-logs"\n'
                "}\n"
            ),
            "main.tf": (
                'resource "aws_s3_bucket" "this" {\n'
                f"  {FOCUS_START}\n"
                "  bucket = var.bucket_name\n"
                "  tags = {\n"
                '    Project = "arena"\n'
                "  }\n"
                f"  {FOCUS_END}\n"
                "}\n"
            ),
        },
        "focus": {
            "kind": "resource",
            "file": "main.tf",
            "rtype": "aws_s3_bucket",
            "name": "this",
            "title": "Complete the bucket resource",
            "todo": "Set the bucket argument and add the Project tag.",
        },
        "level": LEVEL,
        "level_name": LEVEL_NAME,
    },
]

__all__ = ["INTRO_SPECS", "LEVEL", "LEVEL_NAME"]
