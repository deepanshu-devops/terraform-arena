"""Level 0: a guided tutorial track.

The first fifteen Level 0 scenarios isolate HCL syntax.  These ten scenarios
are a short guided project instead: each step adds one idea that appears in
almost every real Terraform module, in the order a beginner usually meets it.

The points are deliberately just above the existing Level 0 range so the
tutorial appears after the syntax warm-ups without renumbering existing
challenges (and therefore without moving existing workspaces).
"""
from __future__ import annotations

from .reference import FOCUS_END, FOCUS_START
from .specs import T, V

LEVEL = 0
LEVEL_NAME = "Level 0 - HCL Foundations"


def _hints(why: str, what: str, when: str, how: str) -> dict[str, str]:
    return {"why": why, "what": what, "when": when, "how": how}


TUTORIAL_SPECS: list[dict] = [
    {
        "id": "tut-variable-first",
        "title": "Tutorial: Reuse a Value With a Variable",
        "difficulty": "Easy",
        "points": 64,
        "tags": ["terraform", "tutorial", "variables"],
        "scenario": (
            "Welcome to the guided track. A variable is a named input: the caller "
            "can change it without editing the block that uses it. Declare one "
            "input variable and expose it through an output."
        ),
        "constraints": [
            "Declare variable app_name.",
            "Use type string and default demo-app.",
            "Create output app_name that reads var.app_name.",
        ],
        "variables": [V("app_name", "string", "demo-app")],
        "expected_outputs": ["app_name"],
        "allowlist": [],
        "tests": [
            T(
                "var",
                "app_name is declared with the expected type and default",
                "Variables",
                14,
                kind="var_defined",
                name="app_name",
                type="string",
                default="demo-app",
                validation=False,
            ),
            T("desc", "the variable has a description", "Variables", 8, kind="file_contains", text="description"),
            T("out", "the app_name output references the variable", "Outputs", 8, kind="output_ref", name="app_name", ref="var.app_name"),
        ],
        "reference": {
            "variables.tf": (
                'variable "app_name" {\n'
                f"  {FOCUS_START}\n"
                '  description = "Name of the application."\n'
                "  type        = string\n"
                '  default     = "demo-app"\n'
                f"  {FOCUS_END}\n"
                "}\n"
            ),
            "outputs.tf": (
                'output "app_name" {\n'
                "  value = var.app_name\n"
                "}\n"
            ),
        },
        "focus": {
            "kind": "top",
            "file": "variables.tf",
            "block": "variable",
            "name": "app_name",
            "title": "Declare the input variable",
            "todo": "Add the variable metadata, its type and a default value.",
        },
        "hints": _hints(
            "Variables are the seam between a reusable configuration and the environment that calls it. Once a value is an input, changing environments does not require editing resource code.",
            "Complete the variable block in variables.tf. It needs a description, a string type and the default shown in the constraints. The output already shows how the caller reads it.",
            "Reach for an input variable when a value changes per environment, must be supplied securely, or should be controlled by whoever calls the configuration.",
            "Start at the top of the `variable \"app_name\"` block. Add `description`, `type = string`, and `default`; keep the quotes around the default because it is a string. Run the tests and compare each failure with the constraint list.",
        ),
    },
    {
        "id": "tut-list-first",
        "title": "Tutorial: Work With a List",
        "difficulty": "Easy",
        "points": 65,
        "tags": ["terraform", "tutorial", "collections"],
        "scenario": (
            "A list keeps values in order. Terraform can index a list, count it, "
            "or iterate over it. Build a small list of environment names and read "
            "the first item and the length."
        ),
        "constraints": [
            "Define local.environments as a list of three names.",
            "The first value must be dev and the last must be prod.",
            "Output first_environment as local.environments[0].",
            "Output environment_count with length(local.environments).",
        ],
        "variables": [],
        "expected_outputs": ["first_environment", "environment_count"],
        "allowlist": [],
        "tests": [
            T("list", "the environments list contains the requested names", "Collections", 12, kind="file_contains", text="staging"),
            T("first", "the first environment is indexed", "Collections", 8, kind="file_contains", text="local.environments[0]"),
            T("count", "the list length is calculated", "Collections", 8, kind="file_contains", text="length(local.environments)"),
            T("out", "first_environment is exported", "Outputs", 6, kind="output_ref", name="first_environment", ref="local.environments"),
            T("out-count", "environment_count is exported", "Outputs", 6, kind="output_ref", name="environment_count", ref="local.environments"),
        ],
        "reference": {
            "main.tf": (
                "locals {\n"
                f"  {FOCUS_START}\n"
                '  environments = ["dev", "staging", "prod"]\n'
                f"  {FOCUS_END}\n"
                "}\n"
                "\n"
                'output "first_environment" {\n'
                "  value = local.environments[0]\n"
                "}\n"
                "\n"
                'output "environment_count" {\n'
                "  value = length(local.environments)\n"
                "}\n"
            ),
        },
        "focus": {
            "kind": "top",
            "file": "main.tf",
            "block": "locals",
            "title": "Create the ordered list",
            "todo": "Add three environment names in deployment order.",
        },
        "hints": _hints(
            "Lists are the starting point for repetition in Terraform. Indexing teaches that positions matter; length teaches how a configuration can adapt when the list grows.",
            "Add one local named environments. It should contain three strings in order, starting with dev and ending with prod. The two outputs are already wired to demonstrate indexing and length.",
            "Use a list when values have a natural order or when every item is interchangeable. If each item needs a stable name, a map is usually a better fit.",
            "Inside `locals`, add `environments = [...]` with three quoted strings in deployment order. The existing outputs already use `local.environments[0]` and `length(local.environments)`, so keep the local name exactly `environments`.",
        ),
    },
    {
        "id": "tut-map-first",
        "title": "Tutorial: Look Up Values in a Map",
        "difficulty": "Easy",
        "points": 66,
        "tags": ["terraform", "tutorial", "collections"],
        "scenario": (
            "A map gives every value a name. Instead of remembering an index, a "
            "caller looks up a key. Build a map of instance sizes and read one "
            "entry by key."
        ),
        "constraints": [
            "Define local.instance_types as a map with dev and prod keys.",
            "Use a small instance size for dev and a larger one for prod.",
            "Output dev_instance_type with local.instance_types[\"dev\"].",
        ],
        "variables": [],
        "expected_outputs": ["dev_instance_type", "all_instance_types"],
        "allowlist": [],
        "tests": [
            T("map", "the map contains the production size", "Collections", 12, kind="file_contains", text="m5.large"),
            T("lookup", "the dev entry is read by key", "Collections", 8, kind="file_contains", text='local.instance_types["dev"]'),
            T("out", "dev_instance_type is exported", "Outputs", 6, kind="output_ref", name="dev_instance_type", ref="local.instance_types"),
            T("out-map", "all_instance_types is exported", "Outputs", 6, kind="output_ref", name="all_instance_types", ref="local.instance_types"),
        ],
        "reference": {
            "main.tf": (
                "locals {\n"
                f"  {FOCUS_START}\n"
                "  instance_types = {\n"
                '    dev  = "t3.micro"\n'
                '    prod = "m5.large"\n'
                "  }\n"
                f"  {FOCUS_END}\n"
                "}\n"
                "\n"
                'output "dev_instance_type" {\n'
                '  value = local.instance_types["dev"]\n'
                "}\n"
                "\n"
                'output "all_instance_types" {\n'
                "  value = local.instance_types\n"
                "}\n"
            ),
        },
        "focus": {
            "kind": "top",
            "file": "main.tf",
            "block": "locals",
            "title": "Create the lookup map",
            "todo": "Add a two-entry map with a small dev size and a larger prod size.",
        },
        "hints": _hints(
            "Maps turn positional data into named data. That is what makes for_each and module inputs readable: the key documents what the value is for.",
            "Create a local map named instance_types with dev and prod keys. The outputs show both a single-key lookup and the whole map.",
            "Use a map when each item has a meaningful name, when the order should not matter, or when you want stable keys for for_each.",
            "Inside `locals`, add `instance_types = { ... }` with `dev` and `prod` keys. Keep the keys unquoted because they are valid identifiers, and quote the instance-size values. The outputs already look up `local.instance_types[\"dev\"]` and the whole map, so keep the local name `instance_types`.",
        ),
    },
    {
        "id": "tut-functions-first",
        "title": "Tutorial: Compose Strings With Functions",
        "difficulty": "Easy",
        "points": 67,
        "tags": ["terraform", "tutorial", "functions", "strings"],
        "scenario": (
            "Terraform's built-in functions transform values without hardcoding the "
            "result. Build a URL-friendly slug from an input, then format a versioned "
            "label from that slug."
        ),
        "constraints": [
            "Use var.app_name as the source value.",
            "Build local.slug with lower() and replace().",
            "Build local.label with format().",
            "Export both values as outputs.",
        ],
        "variables": [V("app_name", "string", "My App")],
        "expected_outputs": ["slug", "label"],
        "allowlist": [],
        "tests": [
            T("var", "app_name is declared", "Variables", 8, kind="var_defined", name="app_name", type="string", default="My App", validation=False),
            T("lower", "lower() is used", "Functions", 8, kind="file_contains", text="lower("),
            T("replace", "replace() is used", "Functions", 8, kind="file_contains", text="replace("),
            T("format", "format() is used", "Functions", 8, kind="file_contains", text="format("),
            T("out-slug", "slug is exported", "Outputs", 5, kind="output_ref", name="slug", ref="local.slug"),
            T("out-label", "label is exported", "Outputs", 5, kind="output_ref", name="label", ref="local.label"),
        ],
        "reference": {
            "variables.tf": (
                'variable "app_name" {\n'
                '  description = "Human-readable application name."\n'
                "  type        = string\n"
                '  default     = "My App"\n'
                "}\n"
            ),
            "main.tf": (
                "locals {\n"
                f"  {FOCUS_START}\n"
                '  slug  = lower(replace(var.app_name, " ", "-"))\n'
                '  label = format("%s-%s", local.slug, "v1")\n'
                f"  {FOCUS_END}\n"
                "}\n"
                "\n"
                'output "slug" {\n'
                "  value = local.slug\n"
                "}\n"
                "\n"
                'output "label" {\n'
                "  value = local.label\n"
                "}\n"
            ),
        },
        "focus": {
            "kind": "top",
            "file": "main.tf",
            "block": "locals",
            "title": "Build the derived strings",
            "todo": "Create a lowercase, hyphenated slug and a formatted version label.",
        },
        "hints": _hints(
            "Functions make derived values declarative. A slug built from the same input every time is easier to trust than a value someone copied into the file.",
            "Compute two locals. The first should turn the input name into a lowercase string with spaces replaced by hyphens. The second should combine that slug with a version suffix using format().",
            "Use string functions when a value is composed from inputs and should update automatically. Avoid them when a plain literal is clearer.",
            "Build `slug` first: nest the case-changing function outside the character-replacement function, and pass `var.app_name` as the innermost input. Build `label` with `format()`: the template comes first, followed by `local.slug` and the version suffix. Keep both local names exactly as the outputs expect.",
        ),
    },
    {
        "id": "tut-for-expression",
        "title": "Tutorial: Transform a List With for",
        "difficulty": "Easy",
        "points": 68,
        "tags": ["terraform", "tutorial", "expressions", "collections"],
        "scenario": (
            "A for expression builds a new collection from an existing one. Use it "
            "to turn a list of team names into uppercase labels and a map of owners, "
            "without writing each entry twice."
        ),
        "constraints": [
            "Define local.teams with platform and security.",
            "Use a for expression to build local.upper_teams.",
            "Use a for expression to build local.team_owners.",
            "Export both derived collections.",
        ],
        "variables": [],
        "expected_outputs": ["upper_teams", "team_owners"],
        "allowlist": [],
        "tests": [
            T("for", "a list comprehension is used", "Expressions", 10, kind="file_contains", text="[for "),
            T("upper", "names are uppercased", "Expressions", 8, kind="file_contains", text="upper("),
            T("map", "a map comprehension is used", "Expressions", 8, kind="file_contains", text="=>"),
            T("out-list", "upper_teams is exported", "Outputs", 6, kind="output_ref", name="upper_teams", ref="local.upper_teams"),
            T("out-map", "team_owners is exported", "Outputs", 6, kind="output_ref", name="team_owners", ref="local.team_owners"),
        ],
        "reference": {
            "main.tf": (
                "locals {\n"
                f"  {FOCUS_START}\n"
                '  teams       = ["platform", "security"]\n'
                "  upper_teams = [for team in local.teams : upper(team)]\n"
                '  team_owners = { for team in local.teams : team => "${team}-owner" }\n'
                f"  {FOCUS_END}\n"
                "}\n"
                "\n"
                'output "upper_teams" {\n'
                "  value = local.upper_teams\n"
                "}\n"
                "\n"
                'output "team_owners" {\n'
                "  value = local.team_owners\n"
                "}\n"
            ),
        },
        "focus": {
            "kind": "top",
            "file": "main.tf",
            "block": "locals",
            "title": "Derive the collections",
            "todo": "Create the source list, then transform it into a list and a map.",
        },
        "hints": _hints(
            "for expressions are the bridge between a plain collection and the shape a resource or module needs. They remove the copy-paste step that causes drift.",
            "Create one source list and two derived locals. One derived value is a list of uppercase names; the other is a map from each name to an owner string.",
            "Use a for expression when you need to transform every item in a collection. Use a map comprehension when each result needs a key.",
            "Start with `teams` as a list. Build `upper_teams` with a bracketed `for` expression over `local.teams` and apply the uppercase function to the loop variable. Build `team_owners` with a braced `for` expression that maps each team name to its owner string using an arrow. Keep the three local names the outputs expect.",
        ),
    },
    {
        "id": "tut-count-first",
        "title": "Tutorial: Repeat a Resource With count",
        "difficulty": "Easy",
        "points": 69,
        "tags": ["terraform", "tutorial", "count", "aws", "s3"],
        "scenario": (
            "count creates several instances of one resource block. Each instance "
            "gets an index, which you can use to pick the matching value from a list. "
            "Create one bucket per entry in a list."
        ),
        "constraints": [
            "Keep the aws_s3_bucket resource block.",
            "Set count from the length of var.bucket_names.",
            "Select each name with count.index.",
            "Export the bucket ids.",
        ],
        "variables": [
            V("bucket_names", "list(string)", ["arena-demo-one", "arena-demo-two"]),
            V("aws_region", "string", "us-east-1"),
        ],
        "expected_resources": ["aws_s3_bucket"],
        "expected_outputs": ["bucket_ids"],
        "allowlist": ["aws_s3_bucket"],
        "tests": [
            T("var", "bucket_names is declared as a list", "Variables", 8, kind="var_defined", name="bucket_names", type="list(string)", validation=False),
            T("res", "the bucket resource exists", "Resources", 10, kind="resource_exists", type="aws_s3_bucket"),
            T("count", "the resource uses count or for_each", "Modularity", 10, kind="count_or_foreach", resource="aws_s3_bucket"),
            T("index", "count.index selects a name", "Modularity", 10, kind="file_contains", text="count.index"),
            T("out", "bucket_ids is exported", "Outputs", 6, kind="output_ref", name="bucket_ids", ref="aws_s3_bucket."),
        ],
        "reference": {
            "versions.tf": (
                "terraform {\n"
                '  required_version = ">= 1.3.0"\n'
                "\n"
                "  required_providers {\n"
                "    aws = {\n"
                '      source  = "hashicorp/aws"\n'
                '      version = "~> 5.0"\n'
                "    }\n"
                "  }\n"
                "}\n"
            ),
            "variables.tf": (
                'variable "bucket_names" {\n'
                '  description = "Names for the demo buckets."\n'
                "  type        = list(string)\n"
                '  default     = ["arena-demo-one", "arena-demo-two"]\n'
                "}\n"
                "\n"
                'variable "aws_region" {\n'
                '  description = "Region for the demo resources."\n'
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
                "  count  = length(var.bucket_names)\n"
                "  bucket = var.bucket_names[count.index]\n"
                f"  {FOCUS_END}\n"
                "}\n"
            ),
            "outputs.tf": (
                'output "bucket_ids" {\n'
                "  value = aws_s3_bucket.this[*].id\n"
                "}\n"
            ),
        },
        "focus": {
            "kind": "resource",
            "file": "main.tf",
            "rtype": "aws_s3_bucket",
            "name": "this",
            "title": "Repeat the bucket",
            "todo": "Add the repetition count and select a name for each instance.",
        },
        "hints": _hints(
            "count is the smallest step from one resource to many. It also reveals why Terraform addresses instances by index, which is useful when you later compare count with for_each.",
            "Complete the bucket resource body. It needs one argument that creates one instance per list entry and one argument that picks the matching name for the current instance.",
            "Use count when the instances are interchangeable and the list order is stable. If each instance has a durable name, for_each is safer.",
            "In the `aws_s3_bucket` resource, add `count` using `length()` over `var.bucket_names`, then set `bucket` by indexing the same list with `count.index`. Keep the resource header unchanged; the existing output shows how all instances are collected.",
        ),
    },
    {
        "id": "tut-for-each-first",
        "title": "Tutorial: Name Instances With for_each",
        "difficulty": "Easy",
        "points": 70,
        "tags": ["terraform", "tutorial", "for_each", "aws", "s3"],
        "scenario": (
            "for_each creates one instance per key in a map or set. Unlike count, "
            "each instance keeps a stable address even when the collection changes. "
            "Create one bucket for every map entry."
        ),
        "constraints": [
            "Keep the aws_s3_bucket resource block.",
            "Use for_each over var.bucket_names.",
            "Read the bucket name from each.value.",
            "Export a map of bucket ids.",
        ],
        "variables": [
            V(
                "bucket_names",
                "map(string)",
                {"logs": "arena-tutorial-logs", "assets": "arena-tutorial-assets"},
            ),
            V("aws_region", "string", "us-east-1"),
        ],
        "expected_resources": ["aws_s3_bucket"],
        "expected_outputs": ["bucket_ids"],
        "allowlist": ["aws_s3_bucket"],
        "tests": [
            T("var", "bucket_names is declared as a map", "Variables", 8, kind="var_defined", name="bucket_names", type="map(string)", validation=False),
            T("res", "the bucket resource exists", "Resources", 10, kind="resource_exists", type="aws_s3_bucket"),
            T("each", "the resource uses per-key iteration", "Modularity", 10, kind="count_or_foreach", resource="aws_s3_bucket"),
            T("value", "each.value supplies the bucket name", "Modularity", 10, kind="file_contains", text="each.value"),
            T("out", "bucket_ids is exported", "Outputs", 6, kind="output_ref", name="bucket_ids", ref="aws_s3_bucket."),
        ],
        "reference": {
            "versions.tf": (
                "terraform {\n"
                '  required_version = ">= 1.3.0"\n'
                "\n"
                "  required_providers {\n"
                "    aws = {\n"
                '      source  = "hashicorp/aws"\n'
                '      version = "~> 5.0"\n'
                "    }\n"
                "  }\n"
                "}\n"
            ),
            "variables.tf": (
                'variable "bucket_names" {\n'
                '  description = "Map of logical name to bucket name."\n'
                "  type        = map(string)\n"
                "  default = {\n"
                '    logs   = "arena-tutorial-logs"\n'
                '    assets = "arena-tutorial-assets"\n'
                "  }\n"
                "}\n"
                "\n"
                'variable "aws_region" {\n'
                '  description = "Region for the demo resources."\n'
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
                "  for_each = var.bucket_names\n"
                "  bucket   = each.value\n"
                f"  {FOCUS_END}\n"
                "}\n"
            ),
            "outputs.tf": (
                'output "bucket_ids" {\n'
                "  value = { for name, bucket in aws_s3_bucket.this : name => bucket.id }\n"
                "}\n"
            ),
        },
        "focus": {
            "kind": "resource",
            "file": "main.tf",
            "rtype": "aws_s3_bucket",
            "name": "this",
            "title": "Create named instances",
            "todo": "Iterate over the map and use the current entry value as the bucket name.",
        },
        "hints": _hints(
            "for_each protects stable addresses. Adding or removing a key changes only that key's instance, while a count list can shift every later index.",
            "Complete the bucket body with a per-key iteration and a reference to the current map value. The output already shows how to reshape the resulting instances into a map.",
            "Use for_each when each instance has a meaningful key, especially when instances may be added or removed over time.",
            "Add `for_each` over the `var.bucket_names` map, then read the current item with `each.value` in the `bucket` argument. Do not use `count.index` here; the input is keyed, and the output already iterates with `name` and `bucket`.",
        ),
    },
    {
        "id": "tut-module-call",
        "title": "Tutorial: Call Your First Module",
        "difficulty": "Easy",
        "points": 71,
        "tags": ["terraform", "tutorial", "modules"],
        "scenario": (
            "A module is a reusable package of Terraform files with inputs and "
            "outputs. Calling one is just a module block: a name, a source and the "
            "inputs the module expects."
        ),
        "constraints": [
            "Create a module block named storage.",
            "Point source at ./modules/storage.",
            "Pass var.bucket_name as bucket_name.",
        ],
        "variables": [V("bucket_name", "string", "arena-tutorial-storage")],
        "expected_outputs": [],
        "allowlist": [],
        "tests": [
            T("source", "the module points at the local module", "Modularity", 14, kind="module_exists", source_contains="./modules/storage"),
            T("name", "the module is named storage", "Modularity", 8, kind="file_contains", text='module "storage"'),
            T("input", "the bucket name is passed into the module", "Modularity", 8, kind="file_contains", text="bucket_name = var.bucket_name"),
        ],
        "reference": {
            "variables.tf": (
                'variable "bucket_name" {\n'
                '  description = "Bucket name passed to the storage module."\n'
                "  type        = string\n"
                '  default     = "arena-tutorial-storage"\n'
                "}\n"
            ),
            "main.tf": (
                'module "storage" {\n'
                f"  {FOCUS_START}\n"
                '  source      = "./modules/storage"\n'
                "  bucket_name = var.bucket_name\n"
                f"  {FOCUS_END}\n"
                "}\n"
            ),
            "modules/storage/main.tf": (
                "# The local module is provided with the scenario.\n"
                'variable "bucket_name" {\n'
                "  type = string\n"
                "}\n"
                "\n"
                'resource "terraform_data" "storage" {\n'
                "  input = var.bucket_name\n"
                "}\n"
            ),
        },
        "focus": {
            "kind": "module",
            "file": "main.tf",
            "block": "module",
            "name": "storage",
            "title": "Complete the module call",
            "todo": "Add the module source and pass the bucket name input.",
        },
        "hints": _hints(
            "Modules are how Terraform code scales beyond a single file. A module call lets you reuse a tested component without copying its resources.",
            "Complete the module block so it loads the local storage module and passes the one input that module expects.",
            "Use a module when a group of resources is reused or when a team needs a stable interface. A local source is ideal while developing the module in the same repository.",
            "Inside `module \"storage\"`, set `source` to the local `./modules/storage` path as a quoted string. Pass `bucket_name = var.bucket_name`; the argument name must match the `variable` block inside the module.",
        ),
    },
    {
        "id": "tut-module-output",
        "title": "Tutorial: Read a Module Output",
        "difficulty": "Easy",
        "points": 72,
        "tags": ["terraform", "tutorial", "modules", "outputs"],
        "scenario": (
            "A module can expose values to its caller through outputs. The caller "
            "reads them with module.<name>.<output>. Wire a module output to a root "
            "output so operators can see it."
        ),
        "constraints": [
            "Keep the module storage call unchanged.",
            "Output bucket_id from output bucket_id.",
            "Reference module.storage.storage_id.",
        ],
        "variables": [V("bucket_name", "string", "arena-tutorial-storage")],
        "expected_outputs": ["bucket_id"],
        "allowlist": [],
        "tests": [
            T("module", "the storage module is called", "Modularity", 10, kind="module_exists", source_contains="./modules/storage"),
            T("out", "bucket_id is exported", "Outputs", 10, kind="output_exists", name="bucket_id"),
            T("ref", "the output reads the module output", "Outputs", 12, kind="output_ref", name="bucket_id", ref="module.storage."),
        ],
        "reference": {
            "variables.tf": (
                'variable "bucket_name" {\n'
                '  description = "Bucket name passed to the storage module."\n'
                "  type        = string\n"
                '  default     = "arena-tutorial-storage"\n'
                "}\n"
            ),
            "main.tf": (
                'module "storage" {\n'
                '  source      = "./modules/storage"\n'
                "  bucket_name = var.bucket_name\n"
                "}\n"
                "\n"
                'output "bucket_id" {\n'
                f"  {FOCUS_START}\n"
                "  value = module.storage.storage_id\n"
                f"  {FOCUS_END}\n"
                "}\n"
            ),
            "modules/storage/main.tf": (
                'variable "bucket_name" {\n'
                "  type = string\n"
                "}\n"
                "\n"
                'resource "terraform_data" "storage" {\n'
                "  input = var.bucket_name\n"
                "}\n"
                "\n"
                'output "storage_id" {\n'
                "  value = terraform_data.storage.id\n"
                "}\n"
            ),
        },
        "focus": {
            "kind": "output",
            "file": "main.tf",
            "block": "output",
            "name": "bucket_id",
            "title": "Wire the module output",
            "todo": "Set the root output value to the module's storage_id output.",
        },
        "hints": _hints(
            "Outputs are the contract between a module and its caller. They prevent a caller from depending on internal resource addresses, which the module should be free to change.",
            "Complete the root output value. The module is already called; the only missing piece is the dotted reference that reaches its exported storage_id.",
            "Use a module output when a caller needs an identifier or setting without knowing how the module implements it.",
            "Inside the existing root `output` block, set `value` to the module output reference. Use the module label from the `module` block and the exported name `storage_id` from the module's `outputs.tf`, joined with dots.",
        ),
    },
    {
        "id": "tut-capstone-compose",
        "title": "Tutorial: Put It All Together",
        "difficulty": "Easy",
        "points": 73,
        "tags": ["terraform", "tutorial", "modules", "for_each", "collections"],
        "scenario": (
            "This final tutorial step combines the ideas so far. Turn a list of "
            "environments into a map, then let a module consume that map with "
            "for_each so each environment gets its own stable instance."
        ),
        "constraints": [
            "Build local.environment_map from var.environments.",
            "Include var.project_name in each generated name.",
            "The module uses local.environment_map with for_each.",
            "Export the module's bucket names.",
        ],
        "variables": [
            V("project_name", "string", "arena"),
            V("environments", "list(string)", ["dev", "prod"]),
        ],
        "expected_outputs": ["bucket_names"],
        "allowlist": [],
        "tests": [
            T("for", "the environment map is built with a for expression", "Expressions", 12, kind="file_contains", text="for env in var.environments"),
            T("arrow", "the map comprehension uses a key/value pair", "Expressions", 8, kind="file_contains", text="=>"),
            T("module", "the storage module uses the generated map", "Modularity", 10, kind="file_contains", text="local.environment_map"),
            T("source", "the local module is called", "Modularity", 8, kind="module_exists", source_contains="./modules/storage"),
            T("out", "bucket_names is exported", "Outputs", 8, kind="output_ref", name="bucket_names", ref="module.storage"),
        ],
        "reference": {
            "variables.tf": (
                'variable "project_name" {\n'
                '  description = "Prefix for generated resource names."\n'
                "  type        = string\n"
                '  default     = "arena"\n'
                "}\n"
                "\n"
                'variable "environments" {\n'
                '  description = "Environments that need storage."\n'
                "  type        = list(string)\n"
                '  default     = ["dev", "prod"]\n'
                "}\n"
            ),
            "main.tf": (
                "locals {\n"
                f"  {FOCUS_START}\n"
                '  environment_map = { for env in var.environments : env => "${var.project_name}-${env}" }\n'
                f"  {FOCUS_END}\n"
                "}\n"
                "\n"
                'module "storage" {\n'
                '  source      = "./modules/storage"\n'
                "  for_each    = local.environment_map\n"
                "  bucket_name = each.value\n"
                "}\n"
                "\n"
                'output "bucket_names" {\n'
                "  value = { for env, bucket in module.storage : env => bucket.bucket_name }\n"
                "}\n"
            ),
            "modules/storage/main.tf": (
                'variable "bucket_name" {\n'
                "  type = string\n"
                "}\n"
                "\n"
                'resource "terraform_data" "storage" {\n'
                "  input = var.bucket_name\n"
                "}\n"
                "\n"
                'output "bucket_name" {\n'
                "  value = var.bucket_name\n"
                "}\n"
            ),
        },
        "focus": {
            "kind": "top",
            "file": "main.tf",
            "block": "locals",
            "title": "Build the module input map",
            "todo": "Turn the environment list into a map of stable bucket names.",
        },
        "hints": _hints(
            "This is the shape of a reusable environment pattern: a caller supplies a small list, a local derives stable keys, and a module creates one instance per key.",
            "Complete the environment_map local. Every environment should become a key whose value is a project-prefixed bucket name. The module call and output below are already wired.",
            "Use this composition when several environments need the same component and you want adding an environment to be a one-line change.",
            "Inside `locals`, add `environment_map` as a braced `for` expression over `var.environments`. Use the loop variable as both the map key and the environment name in the value, and build each value from `var.project_name` plus that name. The module call already consumes `local.environment_map`.",
        ),
    },
]


__all__ = ["TUTORIAL_SPECS", "LEVEL", "LEVEL_NAME"]
