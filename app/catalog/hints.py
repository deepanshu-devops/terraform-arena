"""Public hints for every challenge.

A hint answers four questions in order:

* ``why``  - why the concept matters outside this exercise
* ``what`` - what the learner is expected to complete
* ``when`` - when the pattern is the right tool in real configurations
* ``how``  - how to approach the focused block without revealing the solution

Hand-authored hints live beside the tutorial scenarios.  Every other spec gets
a useful fallback assembled from its tags, focus block, constraints and expected
resources, so a challenge can never ship without hints.
"""
from __future__ import annotations

from typing import Any

HINT_KEYS = ("why", "what", "when", "how")

HINT_LABELS = {
    "why": "Why it matters",
    "what": "What to do",
    "when": "When to use it",
    "how": "How to approach it",
}

# Concept tags are checked before service tags, so a challenge tagged
# ["aws", "s3", "variables"] gets the variables explanation rather than a
# generic cloud-storage one.
_CONCEPT_HINTS: dict[str, dict[str, str]] = {
    "syntax": {
        "why": (
            "Terraform reads a configuration as blocks and arguments. Learning the "
            "shape of a block first makes every later resource, module and provider "
            "feel familiar instead of magical."
        ),
        "when": (
            "Use this mental model whenever you open an unfamiliar .tf file: identify "
            "the block type, its labels, then the arguments inside its body."
        ),
    },
    "hcl": {
        "why": (
            "HCL is the language Terraform evaluates. Small syntax mistakes here turn "
            "into confusing plan errors later, so slow, deliberate practice pays off."
        ),
        "when": (
            "Reach for this whenever you add a new block or argument by hand rather "
            "than copying generated code."
        ),
    },
    "variables": {
        "why": (
            "Input variables separate configuration from implementation. They let one "
            "module serve dev, staging and production without editing the resource "
            "code, and they give reviewers one obvious place to inspect change."
        ),
        "when": (
            "Use a variable when a value differs by environment, comes from a caller, "
            "or must be supplied securely at apply time. Keep truly stable constants "
            "in locals instead."
        ),
    },
    "collections": {
        "why": (
            "Lists and maps let Terraform describe repeated infrastructure without "
            "copy-pasting blocks. They are the foundation for count, for_each and "
            "module inputs."
        ),
        "when": (
            "Use a list when order matters or every item is equivalent. Use a map when "
            "each item needs a stable name you can look up or iterate by key."
        ),
    },
    "strings": {
        "why": (
            "Names, ARNs, URLs and tags are strings. String interpolation and built-in "
            "functions keep generated values consistent and avoid hardcoded fragments "
            "scattered through a configuration."
        ),
        "when": (
            "Use interpolation or string functions when a value is composed from other "
            "values. Prefer direct references for plain values."
        ),
    },
    "expressions": {
        "why": (
            "Expressions turn values into the shape the next block needs. They are how "
            "Terraform avoids hardcoding derived values and how modules adapt to their "
            "inputs."
        ),
        "when": (
            "Use an expression when a value is derived rather than literal, especially "
            "when it should update automatically as inputs change."
        ),
    },
    "functions": {
        "why": (
            "Built-in functions keep transformations declarative. They make naming, "
            "tagging and collection manipulation repeatable instead of relying on "
            "manually maintained strings."
        ),
        "when": (
            "Use functions when you need to transform a value in place: join a list, "
            "change case, merge maps, build a formatted name, or choose a fallback."
        ),
    },
    "conditionals": {
        "why": (
            "A conditional expression lets one configuration express a small policy "
            "difference without duplicating a whole file. That is often the cleanest "
            "way to handle environment-specific settings."
        ),
        "when": (
            "Use a conditional when a value has two clear branches. If the branches "
            "affect whole resources or many arguments, separate configuration or a "
            "module is usually easier to maintain."
        ),
    },
    "for_each": {
        "why": (
            "for_each creates one instance per stable key. Adding or removing an entry "
            "changes only that instance, whereas an index-based list can shift every "
            "later instance when the order changes."
        ),
        "when": (
            "Use for_each when each instance has a durable identity, usually from a map "
            "or a set of strings. Use count for identical instances where position is "
            "the identity."
        ),
    },
    "count": {
        "why": (
            "count is the simplest way to create a repeated resource from a collection. "
            "It teaches how Terraform addresses instances and why changing list order "
            "can be risky."
        ),
        "when": (
            "Use count when instances are interchangeable and their position is stable. "
            "Prefer for_each when each instance has a meaningful name."
        ),
    },
    "locals": {
        "why": (
            "Locals give a name to derived values and shared fragments. They remove "
            "repetition without making a value a user-facing input."
        ),
        "when": (
            "Use locals for values computed from variables, constants reused in several "
            "places, or a common map such as tags. Do not use a local for something the "
            "caller must be able to change."
        ),
    },
    "outputs": {
        "why": (
            "Outputs are the public surface of a configuration or module. They let "
            "callers and operators consume values without reaching into internal "
            "resource addresses."
        ),
        "when": (
            "Export an identifier, endpoint or name when another configuration, a "
            "module consumer, or an operator needs it. Mark secrets sensitive."
        ),
    },
    "modules": {
        "why": (
            "Modules package a group of resources behind a small input/output "
            "contract. They turn copy-pasted infrastructure into something a team can "
            "version, review and reuse."
        ),
        "when": (
            "Use a module when the same group of resources appears more than once, when "
            "a team needs a supported interface, or when you want to test a component "
            "independently."
        ),
    },
    "validation": {
        "why": (
            "Validation catches bad input before Terraform plans changes. A clear rule "
            "and message are much cheaper than debugging a partially applied "
            "configuration."
        ),
        "when": (
            "Use validation for durable invariants such as name formats, allowed "
            "environments and required length ranges. Do not duplicate the provider's "
            "entire schema."
        ),
    },
    "providers": {
        "why": (
            "Providers tell Terraform which API to call and how to authenticate. Pinning "
            "the provider and keeping settings in variables makes a configuration "
            "portable and reproducible."
        ),
        "when": (
            "Configure a provider once per module and pass credentials through the "
            "environment or a secure mechanism, never through committed literals."
        ),
    },
    "files": {
        "why": (
            "Splitting a configuration by purpose makes reviews and ownership easier. "
            "Terraform loads every .tf file in a directory as one module, so the file "
            "layout is for humans, not the engine."
        ),
        "when": (
            "Use separate files for variables, outputs and resources once a module "
            "grows beyond a few blocks. Keep tightly related blocks together."
        ),
    },
    "formatting": {
        "why": (
            "Consistent formatting reduces review noise and makes structural mistakes "
            "visible. terraform fmt is part of the normal Terraform workflow."
        ),
        "when": (
            "Run terraform fmt before every commit, and treat indentation or alignment "
            "changes as formatting rather than behaviour."
        ),
    },
    "state": {
        "why": (
            "State is Terraform's record of what it manages. A remote, locked and "
            "encrypted backend protects that record when more than one person or "
            "automation runs Terraform."
        ),
        "when": (
            "Use a remote backend for any shared or production configuration. Local "
            "state is fine only for short-lived experiments."
        ),
    },
}

# Service tags make the fallback hints concrete for the large generated
# resource catalogue.
_SERVICE_HINTS: dict[str, dict[str, str]] = {
    "s3": {
        "why": "S3 is usually the first shared service in an AWS configuration. Bucket settings, versioning, encryption and public-access blocks are common review findings.",
        "when": "Use S3 when you need durable object storage for assets, logs, backups or static content, and lock down access from the start.",
    },
    "ec2": {
        "why": "EC2 teaches the core lifecycle of compute: image, instance type, networking, storage and safe replacement.",
        "when": "Use EC2 when you need a virtual machine you control directly, or as a building block inside an autoscaling or container platform.",
    },
    "vpc": {
        "why": "A VPC is the network boundary for most AWS resources. CIDR planning, subnets and routing decisions affect everything deployed inside it.",
        "when": "Design a VPC when you need isolated networking, predictable address space or control over public and private traffic.",
    },
    "networking": {
        "why": "Networking resources decide what can talk to what. Getting the boundaries right is a security and reliability concern, not just a connectivity detail.",
        "when": "Use explicit network resources when traffic paths, address ranges or isolation boundaries must be reviewed and versioned.",
    },
    "iam": {
        "why": "IAM is the main authorization boundary in AWS. Least-privilege policies prevent one compromised workload from becoming an account-wide incident.",
        "when": "Create IAM resources when a workload or operator needs narrowly scoped permissions, and prefer roles and temporary credentials over long-lived keys.",
    },
    "security": {
        "why": "Security settings are easiest to review when they are explicit in code. A default that looks harmless in a console can become a production finding.",
        "when": "Make security controls explicit whenever a resource exposes data, identity or network access.",
    },
    "lambda": {
        "why": "Lambda packages compute as a small, event-driven unit. The code artifact, execution role and trigger are the contract to get right.",
        "when": "Use Lambda for short-lived event handlers or glue code where managing a server would add cost and operational noise.",
    },
    "rds": {
        "why": "Managed databases carry availability, backup and network requirements. Terraform makes those choices reviewable before a database is created.",
        "when": "Use a managed database service when you need backups, failover and patching handled by the provider rather than by an operator.",
    },
    "dynamodb": {
        "why": "DynamoDB performance and cost depend on key design. Encoding that design in Terraform makes the access pattern explicit.",
        "when": "Use DynamoDB for predictable key-based access at scale, especially when operational overhead must stay low.",
    },
    "cloudwatch": {
        "why": "Observability resources turn an invisible system into something you can alert on. Metrics, logs and alarms belong with the infrastructure they monitor.",
        "when": "Add monitoring whenever a resource has a failure mode that an operator must notice quickly.",
    },
    "alb": {
        "why": "A load balancer is the stable entry point in front of changing compute. Listeners and target groups define how traffic reaches the application.",
        "when": "Use a load balancer when traffic must be distributed, health-checked or terminated before reaching backend instances.",
    },
    "route53": {
        "why": "DNS is the public name of the system. Managing records in Terraform keeps the name, certificate and endpoint changes together.",
        "when": "Use Route 53 when a service needs a stable hostname or when DNS changes should be reviewed with the rest of the stack.",
    },
    "sqs": {
        "why": "Queues decouple producers from consumers and absorb bursts. Visibility timeouts and retention settings are part of the reliability contract.",
        "when": "Use a queue when work can be processed asynchronously or when two components should not fail together.",
    },
    "sns": {
        "why": "Topics provide fan-out messaging. Subscriptions decide who receives events and in what format.",
        "when": "Use SNS when one event should notify several consumers or when you need a simple pub/sub boundary.",
    },
    "kms": {
        "why": "Encryption keys are a security boundary. Key policies and rotation settings determine who can protect and recover data.",
        "when": "Use a customer-managed key when you need control over encryption policy, rotation or cross-account access.",
    },
    "secretsmanager": {
        "why": "Secrets should live in a managed secret store, not in code or state. Rotation and access policy are easier to audit there.",
        "when": "Use a secret store for credentials and API keys that applications read at runtime.",
    },
    "cloudfront": {
        "why": "A CDN changes latency, caching and the public attack surface. Origin and cache settings are part of the application contract.",
        "when": "Use CloudFront when content is served globally or when you need TLS, caching and origin protection in front of HTTP services.",
    },
    "api-gateway": {
        "why": "API Gateway is the front door for HTTP APIs. Routes, stages and integrations decide how requests reach backend compute.",
        "when": "Use an API gateway when you need a managed public API surface, throttling or request routing.",
    },
    "ecs": {
        "why": "Container services need a cluster, task definition and service wiring. Codifying them makes image and capacity changes reviewable.",
        "when": "Use ECS when you want managed container orchestration without adopting Kubernetes.",
    },
    "docker": {
        "why": "The Docker provider gives a fast local sandbox for learning Terraform's resource lifecycle without cloud credentials.",
        "when": "Use local container resources for practice and integration tests, not as a replacement for production orchestration.",
    },
    "backend": {
        "why": "A shared backend protects state from loss and concurrent writes. That is a prerequisite for team use.",
        "when": "Move to a remote backend as soon as more than one person or pipeline can run Terraform.",
    },
}


def _pick(mapping: dict[str, dict[str, str]], tags: list[str]) -> dict[str, str] | None:
    for tag in tags:
        if tag in mapping:
            return mapping[tag]
    return None


def _fallback_why(spec: dict, tags: list[str]) -> str:
    selected = _pick(_CONCEPT_HINTS, tags) or _pick(_SERVICE_HINTS, tags)
    if selected:
        return selected["why"]
    resources = spec.get("expected_resources") or []
    subject = resources[0] if resources else "this Terraform pattern"
    return (
        f"`{subject}` is a real building block in production configurations. "
        "The exercise isolates one decision so you can recognise the same shape "
        "when it appears inside a larger module."
    )


def _fallback_when(spec: dict, tags: list[str]) -> str:
    selected = _pick(_CONCEPT_HINTS, tags) or _pick(_SERVICE_HINTS, tags)
    if selected:
        return selected["when"]
    return (
        "Use this pattern when the requirement is part of a reusable configuration "
        "that another person or environment must be able to reproduce."
    )


def _fallback_what(spec: dict, focus: dict[str, Any]) -> str:
    file_name = focus.get("file", "main.tf")
    title = focus.get("title") or "Complete the graded block"
    todo = focus.get("todo") or title
    text = f"Complete the marked TODO in `{file_name}`. {todo}"
    constraints = spec.get("constraints") or []
    if constraints:
        text += " Use the visible constraints as your checklist before you run the tests."
    return text


def _fallback_how(spec: dict, focus: dict[str, Any]) -> str:
    file_name = focus.get("file", "main.tf")
    return (
        f"Open `{file_name}` and work inside the single TODO region. Change one "
        "requirement at a time: add the named block, argument or reference, then run "
        "the tests. When a check fails, match its wording to the constraints and fix "
        "only the block it names."
    )


def build_hints(spec: dict, focus: dict[str, Any] | None = None) -> dict[str, str]:
    """Return complete, public hints for a spec.

    Custom hints in the spec override the generated text key by key, so a
    tutorial can explain one section in depth without repeating the others.
    """
    focus = focus or {}
    tags = [str(tag).lower() for tag in spec.get("tags", [])]
    generated = {
        "why": _fallback_why(spec, tags),
        "what": _fallback_what(spec, focus),
        "when": _fallback_when(spec, tags),
        "how": _fallback_how(spec, focus),
    }

    custom = spec.get("hints") or {}
    if isinstance(custom, str):
        custom = {"why": custom}
    for key in HINT_KEYS:
        value = custom.get(key)
        if isinstance(value, str) and value.strip():
            generated[key] = value.strip()
    return generated


__all__ = ["HINT_KEYS", "HINT_LABELS", "build_hints"]
