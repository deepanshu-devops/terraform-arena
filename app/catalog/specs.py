"""Catalog specs: 100+ Terraform practice scenarios.

Scenarios are original but follow the themes that recur in Terraform
interviews and hands-on labs: S3 security, VPC design, EC2 hardening, RDS,
DynamoDB, Lambda, IAM least privilege, modules, state backends and Docker.

Specs are compiled into Challenge objects by ``app.declarative``.
"""
from __future__ import annotations

_MISSING = object()

TAG_TAGS = {
    "Project": "var.project_name",
    "Environment": "var.environment",
    "ManagedBy": '"terraform"',
}


# ---------------------------------------------------------------------------
# Spec helpers
# ---------------------------------------------------------------------------
def V(name: str, type_: str, default=_MISSING, validation: bool = False) -> dict:
    d = {"name": name, "type": type_, "validation": validation}
    if default is not _MISSING:
        d["default"] = default
    return d


def T(id: str, title: str, category: str, weight: int, **check) -> dict:
    return {"id": id, "title": title, "category": category, "weight": weight, "check": check}


def A(name, ref=None, equals=None, max=None, min=None, present=False) -> dict:
    if ref is not None:
        return {"kind": "attr_ref", "attr": name, "ref": ref}
    if equals is not None:
        return {"kind": "attr_equals", "attr": name, "value": equals}
    if max is not None:
        return {"kind": "attr_number_max", "attr": name, "value": max}
    if min is not None:
        return {"kind": "attr_number_min", "attr": name, "value": min}
    return {"kind": "attr_present", "attr": name}


def N(path, attr=None, value=None, max=None) -> dict:
    if value is not None:
        return {"kind": "nested_path", "path": path, "attr": attr, "value": value}
    if max is not None:
        return {"kind": "nested_path_max", "path": path, "attr": attr, "value": max}
    return {"kind": "nested_path_present", "path": path}


def O(name, ref) -> dict:
    return {"name": name, "ref": ref}


def R(
    type_,
    human,
    slug,
    service,
    use_case,
    vars,
    attrs,
    outputs,
    tags=True,
    extra=None,
    difficulty="Easy",
    scenario=None,
    checks=None,
    points=50,
    provider="aws",
    data_allow=None,
):
    return {
        "type": type_,
        "human": human,
        "slug": slug,
        "service": service,
        "use_case": use_case,
        "vars": vars,
        "attrs": attrs,
        "outputs": outputs,
        "tags": tags,
        "extra": extra or [],
        "difficulty": difficulty,
        "scenario": scenario,
        "checks": checks or [],
        "points": points,
        "provider": provider,
        "data_allow": data_allow or ["aws_region", "aws_caller_identity"],
    }


# ---------------------------------------------------------------------------
# Resource matrix -> "Provision ..." challenges
# ---------------------------------------------------------------------------
RESOURCES = [
    R(
        "aws_s3_bucket", "S3 Bucket", "s3-bucket", "S3",
        "durable object storage for application assets",
        vars=[V("bucket_name", "string")],
        attrs=[A("bucket", ref="var.bucket_name"), A("force_destroy", equals="false")],
        outputs=[O("bucket_id", "aws_s3_bucket."), O("bucket_arn", "aws_s3_bucket.")],
        extra=["aws_s3_bucket_versioning", "aws_s3_bucket_public_access_block"],
        tags=True,
    ),
    R(
        "aws_s3_bucket_versioning", "S3 Versioning Configuration", "s3-versioning", "S3",
        "protecting objects from accidental deletion",
        vars=[V("bucket_name", "string")],
        attrs=[A("bucket", ref="var.bucket_name")],
        outputs=[],
        extra=["aws_s3_bucket"],
        checks=[T("status", "Versioning status is Enabled", "Lifecycle", 10, kind="nested_path", resource="aws_s3_bucket_versioning", path=["versioning_configuration"], attr="status", value='"Enabled"')],
        tags=False,
    ),
    R(
        "aws_s3_bucket_server_side_encryption_configuration", "S3 Encryption Configuration", "s3-encryption", "S3",
        "encrypting objects at rest with AES256",
        vars=[V("bucket_name", "string")],
        attrs=[A("bucket", ref="var.bucket_name")],
        outputs=[],
        extra=["aws_s3_bucket"],
        checks=[T("sse", "AES256 is the default algorithm", "Security", 12, kind="nested_path", resource="aws_s3_bucket_server_side_encryption_configuration", path=["rule", "apply_server_side_encryption_by_default"], attr="sse_algorithm", value='"AES256"')],
        tags=False,
    ),
    R(
        "aws_s3_bucket_public_access_block", "S3 Public Access Block", "s3-public-access-block", "S3",
        "preventing accidental public exposure of a bucket",
        vars=[V("bucket_name", "string")],
        attrs=[
            A("bucket", ref="var.bucket_name"),
            A("block_public_acls", equals="true"),
            A("block_public_policy", equals="true"),
            A("ignore_public_acls", equals="true"),
            A("restrict_public_buckets", equals="true"),
        ],
        outputs=[],
        extra=["aws_s3_bucket"],
        tags=False,
    ),
    R(
        "aws_s3_bucket_lifecycle_configuration", "S3 Lifecycle Policy", "s3-lifecycle", "S3",
        "expiring stale objects to control storage cost",
        vars=[V("bucket_name", "string")],
        attrs=[A("bucket", ref="var.bucket_name")],
        outputs=[],
        extra=["aws_s3_bucket"],
        checks=[
            T("rule", "Lifecycle rule is Enabled", "Lifecycle", 8, kind="nested_path", resource="aws_s3_bucket_lifecycle_configuration", path=["rule"], attr="status", value='"Enabled"'),
            T("expiry", "Objects expire within 30 days", "Lifecycle", 10, kind="nested_path_max", resource="aws_s3_bucket_lifecycle_configuration", path=["rule", "expiration"], attr="days", value=30),
        ],
        tags=False,
    ),
    R(
        "aws_ebs_volume", "EBS Volume", "ebs-volume", "EC2",
        "block storage for a single EC2 instance",
        vars=[V("availability_zone", "string", "us-east-1a")],
        attrs=[A("availability_zone", ref="var.availability_zone"), A("size", max=20), A("encrypted", equals="true")],
        outputs=[O("volume_id", "aws_ebs_volume.")],
        tags=True,
    ),
    R(
        "aws_efs_file_system", "EFS File System", "efs-file-system", "EFS",
        "shared POSIX storage for multiple compute nodes",
        vars=[V("file_system_name", "string", "shared-assets")],
        attrs=[A("creation_token", ref="var.file_system_name"), A("encrypted", equals="true")],
        outputs=[O("file_system_id", "aws_efs_file_system.")],
        tags=True,
    ),
    R(
        "aws_vpc", "VPC", "vpc", "VPC",
        "an isolated network boundary for a workload",
        vars=[V("vpc_cidr", "string", "10.0.0.0/16")],
        attrs=[A("cidr_block", ref="var.vpc_cidr"), A("enable_dns_support", equals="true"), A("enable_dns_hostnames", equals="true")],
        outputs=[O("vpc_id", "aws_vpc.")],
        tags=True,
    ),
    R(
        "aws_subnet", "Public Subnet", "public-subnet", "VPC",
        "a public subnet that auto-assigns IPs",
        vars=[V("vpc_id", "string"), V("subnet_cidr", "string", "10.0.1.0/24"), V("availability_zone", "string", "us-east-1a")],
        attrs=[
            A("vpc_id", ref="var.vpc_id"),
            A("cidr_block", ref="var.subnet_cidr"),
            A("availability_zone", ref="var.availability_zone"),
            A("map_public_ip_on_launch", equals="true"),
        ],
        outputs=[O("subnet_id", "aws_subnet.")],
        extra=["aws_vpc"],
        tags=True,
    ),
    R(
        "aws_internet_gateway", "Internet Gateway", "internet-gateway", "VPC",
        "outbound internet connectivity for a VPC",
        vars=[V("vpc_id", "string")],
        attrs=[A("vpc_id", ref="var.vpc_id")],
        outputs=[O("internet_gateway_id", "aws_internet_gateway.")],
        extra=["aws_vpc"],
        tags=True,
    ),
    R(
        "aws_route_table", "VPC Route Table", "route-table", "VPC",
        "routing public subnet traffic",
        vars=[V("vpc_id", "string")],
        attrs=[A("vpc_id", ref="var.vpc_id")],
        outputs=[O("route_table_id", "aws_route_table.")],
        extra=["aws_vpc"],
        tags=True,
    ),
    R(
        "aws_security_group", "Security Group", "security-group", "EC2",
        "stateful firewall rules for an application",
        vars=[V("vpc_id", "string"), V("security_group_name", "string", "app-sg")],
        attrs=[A("name", ref="var.security_group_name"), A("description", equals='"managed by terraform"'), A("vpc_id", ref="var.vpc_id")],
        outputs=[O("security_group_id", "aws_security_group.")],
        extra=["aws_vpc"],
        checks=[
            T("ingress", "At least one ingress rule", "Security", 8, kind="nested_count_min", resource="aws_security_group", block="ingress", min=1),
            T("egress", "At least one egress rule", "Security", 6, kind="nested_count_min", resource="aws_security_group", block="egress", min=1),
        ],
        tags=True,
    ),
    R(
        "aws_eip", "Elastic IP", "elastic-ip", "VPC",
        "a static public IPv4 address",
        vars=[],
        attrs=[A("domain", equals='"vpc"')],
        outputs=[O("eip_id", "aws_eip.")],
        tags=True,
    ),
    R(
        "aws_nat_gateway", "NAT Gateway", "nat-gateway", "VPC",
        "outbound internet for private subnets",
        vars=[V("eip_allocation_id", "string"), V("public_subnet_id", "string")],
        attrs=[A("allocation_id", ref="var.eip_allocation_id"), A("subnet_id", ref="var.public_subnet_id")],
        outputs=[O("nat_gateway_id", "aws_nat_gateway.")],
        tags=True,
    ),
    R(
        "aws_lb", "Application Load Balancer", "application-load-balancer", "ALB",
        "distributing HTTP traffic across targets",
        vars=[V("subnet_ids", "list(string)"), V("security_group_ids", "list(string)")],
        attrs=[
            A("load_balancer_type", equals='"application"'),
            A("subnets", ref="var.subnet_ids"),
            A("security_groups", ref="var.security_group_ids"),
            A("internal", equals="false"),
        ],
        outputs=[O("lb_arn", "aws_lb."), O("lb_dns_name", "aws_lb.")],
        tags=True,
    ),
    R(
        "aws_lb_target_group", "ALB Target Group", "target-group", "ALB",
        "health-checked backend targets",
        vars=[V("vpc_id", "string")],
        attrs=[A("port", equals="80"), A("protocol", equals='"HTTP"'), A("vpc_id", ref="var.vpc_id")],
        outputs=[O("target_group_arn", "aws_lb_target_group.")],
        extra=["aws_vpc"],
        checks=[T("hc", "HTTP health check on /", "Lifecycle", 8, kind="nested_path", resource="aws_lb_target_group", path=["health_check"], attr="path", value='"/"')],
        tags=True,
    ),
    R(
        "aws_lb_listener", "ALB Listener", "lb-listener", "ALB",
        "accepting HTTP traffic on port 80",
        vars=[V("lb_arn", "string"), V("target_group_arn", "string")],
        attrs=[A("load_balancer_arn", ref="var.lb_arn"), A("port", equals="80"), A("protocol", equals='"HTTP"')],
        outputs=[O("listener_arn", "aws_lb_listener.")],
        extra=["aws_lb", "aws_lb_target_group"],
        checks=[T("forward", "Default action forwards to a target group", "Resources", 10, kind="file_contains", text="target_group_arn")],
        tags=False,
    ),
    R(
        "aws_cloudfront_distribution", "CloudFront Distribution", "cloudfront", "CloudFront",
        "a global CDN in front of an origin",
        vars=[V("origin_domain_name", "string", "example.com"), V("certificate_arn", "string")],
        attrs=[A("enabled", equals="true")],
        outputs=[O("domain_name", "aws_cloudfront_distribution.")],
        checks=[
            T("https", "Viewer protocol redirects to HTTPS", "Security", 10, kind="nested_path", resource="aws_cloudfront_distribution", path=["default_cache_behavior"], attr="viewer_protocol_policy", value='"redirect-to-https"'),
            T("tls", "Modern TLS minimum", "Security", 8, kind="nested_path", resource="aws_cloudfront_distribution", path=["viewer_certificate"], attr="minimum_protocol_version", value='"TLSv1.2_2021"'),
        ],
        tags=True,
    ),
    R(
        "aws_route53_zone", "Route 53 Hosted Zone", "route53-zone", "Route53",
        "authoritative DNS for a domain",
        vars=[V("domain_name", "string", "example.com")],
        attrs=[A("name", ref="var.domain_name")],
        outputs=[O("zone_id", "aws_route53_zone.")],
        tags=True,
    ),
    R(
        "aws_route53_record", "Route 53 A Record", "route53-record", "Route53",
        "pointing a hostname at an address",
        vars=[V("zone_id", "string"), V("record_name", "string", "app"), V("record_value", "string", "203.0.113.10")],
        attrs=[A("zone_id", ref="var.zone_id"), A("name", ref="var.record_name"), A("type", equals='"A"'), A("ttl", max=300)],
        outputs=[O("fqdn", "aws_route53_record.")],
        extra=["aws_route53_zone"],
        tags=False,
    ),
    R(
        "aws_instance", "EC2 Instance", "ec2-instance", "EC2",
        "a virtual machine for a stateless service",
        vars=[V("ami_id", "string"), V("instance_type", "string", "t2.micro"), V("subnet_id", "string")],
        attrs=[
            A("ami", ref="var.ami_id"),
            A("instance_type", ref="var.instance_type"),
            A("subnet_id", ref="var.subnet_id"),
            A("associate_public_ip_address", equals="false"),
        ],
        outputs=[O("instance_id", "aws_instance.")],
        checks=[T("imds", "IMDSv2 enforced", "Security", 10, kind="nested_path", resource="aws_instance", path=["metadata_options"], attr="http_tokens", value='"required"')],
        tags=True,
    ),
    R(
        "aws_launch_template", "EC2 Launch Template", "launch-template", "EC2",
        "a reusable, hardened instance blueprint",
        vars=[V("ami_id", "string"), V("instance_type", "string", "t2.micro")],
        attrs=[A("image_id", ref="var.ami_id"), A("instance_type", ref="var.instance_type")],
        outputs=[O("launch_template_id", "aws_launch_template.")],
        checks=[T("imds", "IMDSv2 enforced", "Security", 10, kind="nested_path", resource="aws_launch_template", path=["metadata_options"], attr="http_tokens", value='"required"')],
        tags=True,
    ),
    R(
        "aws_autoscaling_group", "Auto Scaling Group", "autoscaling-group", "EC2",
        "elastic capacity across subnets",
        vars=[V("asg_min", "number", 1), V("asg_max", "number", 2), V("asg_desired", "number", 1), V("subnet_ids", "list(string)")],
        attrs=[
            A("min_size", ref="var.asg_min"),
            A("max_size", ref="var.asg_max"),
            A("desired_capacity", ref="var.asg_desired"),
            A("vpc_zone_identifier", ref="var.subnet_ids"),
        ],
        outputs=[O("asg_name", "aws_autoscaling_group.")],
        tags=False,
    ),
    R(
        "aws_key_pair", "EC2 Key Pair", "key-pair", "EC2",
        "SSH access material for instances",
        vars=[V("key_name", "string", "app-key"), V("public_key", "string")],
        attrs=[A("key_name", ref="var.key_name"), A("public_key", ref="var.public_key")],
        outputs=[O("key_name", "aws_key_pair.")],
        tags=True,
    ),
    R(
        "aws_ecs_cluster", "ECS Cluster", "ecs-cluster", "ECS",
        "a logical boundary for container services",
        vars=[V("cluster_name", "string", "app-cluster")],
        attrs=[A("name", ref="var.cluster_name")],
        outputs=[O("cluster_arn", "aws_ecs_cluster.")],
        tags=True,
    ),
    R(
        "aws_ecs_task_definition", "ECS Task Definition", "ecs-task-definition", "ECS",
        "a small Fargate task blueprint",
        vars=[V("family", "string", "app-task"), V("container_image", "string", "nginx:alpine")],
        attrs=[A("family", ref="var.family"), A("cpu", max=256), A("memory", max=512), A("network_mode", equals='"awsvpc"')],
        outputs=[O("task_definition_arn", "aws_ecs_task_definition.")],
        tags=False,
    ),
    R(
        "aws_db_instance", "RDS PostgreSQL Instance", "rds-instance", "RDS",
        "a small managed relational database",
        vars=[V("db_engine", "string", "postgres"), V("db_name", "string", "appdb"), V("db_username", "string", "appuser"), V("db_password", "string")],
        attrs=[
            A("engine", ref="var.db_engine"),
            A("instance_class", equals='"db.t3.micro"'),
            A("allocated_storage", max=20),
            A("storage_encrypted", equals="true"),
            A("skip_final_snapshot", equals="true"),
            A("publicly_accessible", equals="false"),
        ],
        outputs=[O("db_endpoint", "aws_db_instance.")],
        extra=["aws_db_subnet_group"],
        tags=True,
        difficulty="Medium",
        points=80,
    ),
    R(
        "aws_db_subnet_group", "RDS Subnet Group", "db-subnet-group", "RDS",
        "database placement across private subnets",
        vars=[V("subnet_group_name", "string", "app-db-subnets"), V("subnet_ids", "list(string)")],
        attrs=[A("name", ref="var.subnet_group_name"), A("subnet_ids", ref="var.subnet_ids")],
        outputs=[O("subnet_group_name", "aws_db_subnet_group.")],
        tags=True,
    ),
    R(
        "aws_dynamodb_table", "DynamoDB Table", "dynamodb-table", "DynamoDB",
        "on-demand key-value storage",
        vars=[V("table_name", "string", "items")],
        attrs=[A("billing_mode", equals='"PAY_PER_REQUEST"'), A("hash_key", equals='"id"')],
        outputs=[O("table_arn", "aws_dynamodb_table."), O("table_name", "aws_dynamodb_table.")],
        checks=[
            T("attr", "Attribute id is a string", "Resources", 8, kind="nested_path", resource="aws_dynamodb_table", path=["attribute"], attr="type", value='"S"'),
            T("sse", "Encryption enabled", "Security", 8, kind="nested_path", resource="aws_dynamodb_table", path=["server_side_encryption"], attr="enabled", value="true"),
            T("pitr", "Point-in-time recovery enabled", "Security", 8, kind="nested_path", resource="aws_dynamodb_table", path=["point_in_time_recovery"], attr="enabled", value="true"),
        ],
        tags=True,
        difficulty="Medium",
        points=80,
    ),
    R(
        "aws_lambda_function", "Lambda Function", "lambda-function", "Lambda",
        "an event-driven Python function",
        vars=[V("lambda_role_arn", "string"), V("lambda_runtime", "string", "python3.12"), V("lambda_memory", "number", 128)],
        attrs=[
            A("role", ref="var.lambda_role_arn"),
            A("runtime", ref="var.lambda_runtime"),
            A("handler", equals='"handler.lambda_handler"'),
            A("filename", equals='"lambda.zip"'),
            A("memory_size", ref="var.lambda_memory"),
        ],
        outputs=[O("lambda_arn", "aws_lambda_function.")],
        tags=True,
        difficulty="Medium",
        points=70,
    ),
    R(
        "aws_lambda_permission", "Lambda Invoke Permission", "lambda-permission", "Lambda",
        "allowing API Gateway to invoke a function",
        vars=[V("lambda_function_name", "string")],
        attrs=[
            A("action", equals='"lambda:InvokeFunction"'),
            A("principal", equals='"apigateway.amazonaws.com"'),
            A("function_name", ref="var.lambda_function_name"),
        ],
        outputs=[O("statement_id", "aws_lambda_permission.")],
        extra=["aws_lambda_function"],
        tags=False,
    ),
    R(
        "aws_apigatewayv2_api", "HTTP API Gateway", "http-api", "API Gateway",
        "a lightweight HTTP front door",
        vars=[V("api_name", "string", "items-api")],
        attrs=[A("name", ref="var.api_name"), A("protocol_type", equals='"HTTP"')],
        outputs=[O("api_endpoint", "aws_apigatewayv2_api.")],
        tags=True,
    ),
    R(
        "aws_apigatewayv2_stage", "API Gateway Stage", "api-stage", "API Gateway",
        "a deployed stage for an HTTP API",
        vars=[V("api_id", "string"), V("stage_name", "string", "prod")],
        attrs=[A("api_id", ref="var.api_id"), A("name", ref="var.stage_name"), A("auto_deploy", equals="true")],
        outputs=[O("invoke_url", "aws_apigatewayv2_stage.")],
        extra=["aws_apigatewayv2_api"],
        tags=True,
    ),
    R(
        "aws_sqs_queue", "SQS Queue", "sqs-queue", "SQS",
        "a durable work queue with encryption",
        vars=[V("queue_name", "string", "jobs")],
        attrs=[A("name", ref="var.queue_name"), A("sqs_managed_sse_enabled", equals="true"), A("message_retention_seconds", max=345600)],
        outputs=[O("queue_url", "aws_sqs_queue."), O("queue_arn", "aws_sqs_queue.")],
        tags=True,
        difficulty="Medium",
        points=70,
    ),
    R(
        "aws_sns_topic", "SNS Topic", "sns-topic", "SNS",
        "a pub/sub fan-out topic",
        vars=[V("topic_name", "string", "alerts")],
        attrs=[A("name", ref="var.topic_name"), A("fifo_topic", equals="false")],
        outputs=[O("topic_arn", "aws_sns_topic.")],
        tags=True,
    ),
    R(
        "aws_cloudwatch_event_rule", "EventBridge Schedule Rule", "eventbridge-rule", "EventBridge",
        "a scheduled automation trigger",
        vars=[V("rule_name", "string", "nightly-job")],
        attrs=[A("name", ref="var.rule_name"), A("schedule_expression", equals='"rate(5 minutes)"'), A("state", equals='"ENABLED"')],
        outputs=[O("rule_arn", "aws_cloudwatch_event_rule.")],
        tags=True,
    ),
    R(
        "aws_cloudwatch_log_group", "CloudWatch Log Group", "log-group", "CloudWatch",
        "centralized application logs with retention",
        vars=[V("log_group_name", "string", "/app/logs")],
        attrs=[A("name", ref="var.log_group_name"), A("retention_in_days", equals="14")],
        outputs=[O("log_group_arn", "aws_cloudwatch_log_group.")],
        tags=True,
    ),
    R(
        "aws_cloudwatch_metric_alarm", "CloudWatch CPU Alarm", "metric-alarm", "CloudWatch",
        "alerting when CPU stays high",
        vars=[V("alarm_name", "string", "high-cpu")],
        attrs=[
            A("alarm_name", ref="var.alarm_name"),
            A("comparison_operator", equals='"GreaterThanThreshold"'),
            A("evaluation_periods", equals="1"),
            A("threshold", equals="80"),
            A("metric_name", equals='"CPUUtilization"'),
            A("namespace", equals='"AWS/EC2"'),
            A("period", equals="300"),
            A("statistic", equals='"Average"'),
        ],
        outputs=[O("alarm_arn", "aws_cloudwatch_metric_alarm.")],
        tags=True,
    ),
    R(
        "aws_iam_role", "IAM Role", "iam-role", "IAM",
        "a service role with a trust policy",
        vars=[V("role_name", "string", "app-role"), V("trusted_service", "string", "lambda.amazonaws.com")],
        attrs=[A("name", ref="var.role_name"), A("assume_role_policy", present=True)],
        outputs=[O("role_arn", "aws_iam_role.")],
        tags=True,
    ),
    R(
        "aws_iam_policy", "IAM Policy", "iam-policy", "IAM",
        "a scoped permission set",
        vars=[V("policy_name", "string", "app-policy")],
        attrs=[A("name", ref="var.policy_name"), A("policy", present=True)],
        outputs=[O("policy_arn", "aws_iam_policy.")],
        tags=True,
    ),
    R(
        "aws_kms_key", "KMS Customer Key", "kms-key", "KMS",
        "a rotating customer-managed encryption key",
        vars=[],
        attrs=[A("description", equals='"managed by terraform"'), A("enable_key_rotation", equals="true"), A("deletion_window_in_days", equals="7")],
        outputs=[O("key_arn", "aws_kms_key."), O("key_id", "aws_kms_key.")],
        tags=True,
    ),
    R(
        "aws_secretsmanager_secret", "Secrets Manager Secret", "secretsmanager-secret", "Secrets Manager",
        "secure storage for application credentials",
        vars=[V("secret_name", "string", "app/credentials")],
        attrs=[A("name", ref="var.secret_name"), A("recovery_window_in_days", equals="0")],
        outputs=[O("secret_arn", "aws_secretsmanager_secret.")],
        tags=True,
    ),
    R(
        "aws_ssm_parameter", "SSM Secure Parameter", "ssm-parameter", "SSM",
        "encrypted configuration values",
        vars=[V("parameter_name", "string", "/app/config"), V("parameter_value", "string")],
        attrs=[A("name", ref="var.parameter_name"), A("type", equals='"SecureString"'), A("value", ref="var.parameter_value")],
        outputs=[O("parameter_arn", "aws_ssm_parameter.")],
        tags=True,
    ),
    R(
        "aws_wafv2_web_acl", "WAF Web ACL", "waf-web-acl", "WAF",
        "edge protection for public endpoints",
        vars=[V("web_acl_name", "string", "app-waf")],
        attrs=[A("name", ref="var.web_acl_name"), A("scope", equals='"REGIONAL"')],
        outputs=[O("web_acl_arn", "aws_wafv2_web_acl.")],
        checks=[T("allow", "Default action is allow", "Security", 8, kind="nested_path_present", resource="aws_wafv2_web_acl", path=["default_action", "allow"])],
        tags=True,
        difficulty="Medium",
        points=80,
    ),
    R(
        "aws_acm_certificate", "ACM Certificate", "acm-certificate", "ACM",
        "a DNS-validated TLS certificate",
        vars=[V("domain_name", "string", "example.com")],
        attrs=[A("domain_name", ref="var.domain_name"), A("validation_method", equals='"DNS"')],
        outputs=[O("certificate_arn", "aws_acm_certificate.")],
        tags=True,
    ),
    R(
        "aws_backup_vault", "AWS Backup Vault", "backup-vault", "Backup",
        "a vault for recovery points",
        vars=[V("vault_name", "string", "app-vault")],
        attrs=[A("name", ref="var.vault_name")],
        outputs=[O("vault_arn", "aws_backup_vault.")],
        tags=True,
    ),
    R(
        "aws_backup_plan", "AWS Backup Plan", "backup-plan", "Backup",
        "a nightly backup schedule",
        vars=[V("plan_name", "string", "nightly-backup")],
        attrs=[A("name", ref="var.plan_name")],
        outputs=[O("plan_arn", "aws_backup_plan.")],
        checks=[T("schedule", "Nightly cron schedule", "Lifecycle", 8, kind="nested_path", resource="aws_backup_plan", path=["rule"], attr="schedule_expression", value='"cron(0 5 ? * * *)"')],
        tags=True,
    ),
    R(
        "aws_cognito_user_pool", "Cognito User Pool", "cognito-user-pool", "Cognito",
        "managed authentication for an application",
        vars=[V("user_pool_name", "string", "app-users")],
        attrs=[A("name", ref="var.user_pool_name"), A("mfa_configuration", equals='"ON"')],
        outputs=[O("user_pool_arn", "aws_cognito_user_pool.")],
        checks=[T("password", "Password minimum length >= 12", "Security", 8, kind="nested_path", resource="aws_cognito_user_pool", path=["password_policy"], attr="minimum_length", value="12")],
        tags=True,
        difficulty="Medium",
        points=80,
    ),
    R(
        "aws_stepfunctions_state_machine", "Step Functions State Machine", "stepfunctions", "Step Functions",
        "an orchestration workflow for async jobs",
        vars=[V("state_machine_name", "string", "order-flow"), V("role_arn", "string")],
        attrs=[A("name", ref="var.state_machine_name"), A("role_arn", ref="var.role_arn"), A("definition", present=True)],
        outputs=[O("state_machine_arn", "aws_stepfunctions_state_machine.")],
        tags=True,
        difficulty="Medium",
        points=80,
    ),
]


def _attr_test(res, idx, attr):
    t = res["type"]
    kind = attr["kind"]
    if kind == "attr_ref":
        return T(f"a{idx}", f"{attr['attr']} references {attr['ref']}", "Resources", 6, kind="attr_ref", resource=t, attr=attr["attr"], ref=attr["ref"])
    if kind == "attr_equals":
        return T(f"a{idx}", f"{attr['attr']} is set correctly", "Resources", 6, kind="attr_equals", resource=t, attr=attr["attr"], value=attr["value"])
    if kind == "attr_number_max":
        return T(f"a{idx}", f"{attr['attr']} <= {attr['value']}", "Lifecycle", 5, kind="attr_number_max", resource=t, attr=attr["attr"], value=attr["value"])
    if kind == "attr_number_min":
        return T(f"a{idx}", f"{attr['attr']} >= {attr['value']}", "Lifecycle", 5, kind="attr_number_min", resource=t, attr=attr["attr"], value=attr["value"])
    if kind == "nested_path":
        return T(f"a{idx}", f"{'.'.join(attr['path'])} is correct", "Resources", 7, kind="nested_path", resource=t, path=attr["path"], attr=attr["attr"], value=attr["value"])
    if kind == "nested_path_max":
        return T(f"a{idx}", f"{'.'.join(attr['path'])} <= {attr['value']}", "Lifecycle", 6, kind="nested_path_max", resource=t, path=attr["path"], attr=attr["attr"], value=attr["value"])
    if kind == "nested_path_present":
        return T(f"a{idx}", f"{'.'.join(attr['path'])} is present", "Resources", 6, kind="nested_path_present", resource=t, path=attr["path"])
    return T(f"a{idx}", f"{attr['attr']} is present", "Resources", 5, kind="attr_present", resource=t, attr=attr["attr"])


def provision_spec(res):
    tags = res["tags"]
    vars = list(res["vars"])
    names = {v["name"] for v in vars}
    if tags:
        if "environment" not in names:
            vars.append(V("environment", "string", "dev"))
        if "project_name" not in names:
            vars.append(V("project_name", "string", "terraform-practice"))
    if res["provider"] == "aws" and "aws_region" not in names:
        vars.append(V("aws_region", "string", "us-east-1"))

    tests = [
        T("res", f"{res['type']} is provisioned", "Resources", 14, kind="resource_exists", type=res["type"]),
    ]
    for i, attr in enumerate(res["attrs"]):
        tests.append(_attr_test(res, i, attr))
    tests.extend(res["checks"])

    if tags:
        tests.append(T("tags", "Standard tags are applied", "Lifecycle", 8, kind="tagged", resources=[res["type"]], tags=TAG_TAGS))

    for out in res["outputs"]:
        tests.append(T(f"out-{out['name']}", f"Output {out['name']} is exported", "Outputs", 5, kind="output_ref", name=out["name"], ref=out["ref"]))

    for v in vars:
        tests.append(T(f"var-{v['name']}", f"Variable {v['name']} is declared", "Variables", 3, kind="var_defined", name=v["name"], type=v["type"], default=v.get("default"), validation=v.get("validation", False)))

    if res["provider"] == "aws":
        tests.insert(0, T("provider", "AWS provider + region variable", "Providers", 5, kind="required_provider", name="aws"))
        tests.insert(1, T("region", "Provider region references var.aws_region", "Providers", 4, kind="provider_ref", provider="aws", attr="region", ref="var.aws_region"))

    output_names = [o["name"] for o in res["outputs"]]
    human = res["human"]
    scenario = res["scenario"] or (
        f"Your platform team needs {human} for {res['use_case']}. Write a reusable Terraform "
        f"configuration that provisions it, drives every input through variables, applies the "
        f"standard tags, and exports the operational identifiers."
    )

    constraints = [
        f"Provider: {res['provider']} (region from var.aws_region)." if res["provider"] == "aws" else f"Provider: {res['provider']}.",
        f"Create exactly one resource of type {res['type']}.",
        "All configurable values must come from variables declared in variables.tf.",
        "No hardcoded AWS credentials.",
        "Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).",
    ]
    if tags:
        constraints.append('Tag the resource with Project, Environment and ManagedBy = "terraform".')
    if output_names:
        constraints.append("Expose outputs: " + ", ".join(output_names) + ".")
    if res["extra"]:
        constraints.append("Allowed supporting resources: " + ", ".join(res["extra"]) + ".")

    allow = [res["type"]] + res["extra"]
    return {
        "id": f"provision-{res['slug']}",
        "title": f"Provision {human}",
        "difficulty": res["difficulty"],
        "points": res["points"],
        "tags": ["aws", res["service"].lower().replace(" ", "-"), "provisioning"],
        "scenario": scenario,
        "constraints": constraints,
        "variables": vars,
        "expected_resources": [res["type"]],
        "expected_outputs": output_names,
        "allowlist": allow,
        "data_allowlist": res["data_allow"],
        "tests": tests,
        "provision": True,
    }
