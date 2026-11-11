# Terraform Arena - Challenge Index

125 challenges, ordered from level 0 (HCL basics) to level 5 (capstones).

| # | Level | Difficulty | Points | Challenge | Focus | Folder |
| --- | --- | --- | --- | --- | --- | --- |
| 001 | Level 0 - HCL Foundations | Easy | 40 | Your First HCL Block | Complete the locals block | `001-intro-hcl-blocks` |
| 002 | Level 0 - HCL Foundations | Easy | 45 | Arguments and Variable Blocks | Complete the variable block | `002-intro-hcl-arguments` |
| 003 | Level 0 - HCL Foundations | Easy | 45 | Strings and Interpolation | Complete the greeting output | `003-intro-hcl-strings` |
| 004 | Level 0 - HCL Foundations | Easy | 50 | Format HCL by Hand | Fix the formatting | `004-intro-hcl-formatting` |
| 005 | Level 0 - HCL Foundations | Easy | 50 | Lists and Maps | Complete the collections | `005-intro-hcl-collections` |
| 006 | Level 0 - HCL Foundations | Easy | 50 | Provider and Version Blocks | Complete the provider block | `006-intro-provider-block` |
| 007 | Level 0 - HCL Foundations | Easy | 55 | Split a Configuration Across Files | Complete the bucket resource | `007-intro-file-layout` |
| 008 | Level 0 - HCL Foundations | Easy | 56 | Local Values and References | Add the local values | `008-intro-local-values` |
| 009 | Level 0 - HCL Foundations | Easy | 57 | Conditional Expressions | Add the conditional locals | `009-intro-conditional` |
| 010 | Level 0 - HCL Foundations | Easy | 58 | For Expressions | Transform the names | `010-intro-for-expression` |
| 011 | Level 0 - HCL Foundations | Easy | 59 | Built-in Functions | Normalise the bucket name | `011-intro-functions` |
| 012 | Level 0 - HCL Foundations | Easy | 60 | Optional Values With coalesce | Add the fallback value | `012-intro-null-default` |
| 013 | Level 0 - HCL Foundations | Easy | 61 | Splat Expressions | Extract instance attributes | `013-intro-splat-expression` |
| 014 | Level 0 - HCL Foundations | Easy | 62 | Sensitive Outputs | Complete the sensitive output | `014-intro-sensitive-output` |
| 015 | Level 0 - HCL Foundations | Easy | 63 | Resource Arguments and Tags | Complete the bucket resource | `015-intro-resource-tags` |
| 016 | Level 1 - Terraform Language | Easy | 50 | Sensitive Output | Mark the output as sensitive | `016-lang-sensitive-output` |
| 017 | Level 1 - Terraform Language | Easy | 55 | Compose Tags With merge() | Complete the locals block | `017-lang-functions-merge` |
| 018 | Level 1 - Terraform Language | Easy | 55 | Conditional Expressions | Complete the bucket name expression | `018-lang-conditional-environment` |
| 019 | Level 1 - Terraform Language | Easy | 55 | Explicit depends_on | Add the explicit dependency | `019-lang-depends-on` |
| 020 | Level 1 - Terraform Language | Easy | 55 | Locals for Common Tags | Complete the shared tags locals block | `020-lang-locals-common-tags` |
| 021 | Level 1 - Terraform Language | Easy | 55 | Protect a Bucket With prevent_destroy | Complete the lifecycle block | `021-lang-lifecycle-protect` |
| 022 | Level 1 - Terraform Language | Easy | 60 | Discover an AMI With a Data Source | Complete the aws_ami data source | `022-lang-data-sources` |
| 023 | Level 1 - Terraform Language | Easy | 60 | Variable Validation | Complete the validation block for bucket_name | `023-lang-variables-validation` |
| 024 | Level 1 - Terraform Language | Medium | 90 | Create Subnets With count | Complete the aws_subnet block | `024-lang-count-subnets` |
| 025 | Level 1 - Terraform Language | Medium | 95 | Create Subnets With for_each | Complete the aws_subnet block | `025-lang-for-each-subnets` |
| 026 | Level 2 - First Resources | Easy | 40 | Create a Docker Network | Complete the docker_network resource | `026-docker-network` |
| 027 | Level 2 - First Resources | Easy | 40 | Create a Docker Volume | Complete the docker_volume resource | `027-docker-volume` |
| 028 | Level 2 - First Resources | Easy | 45 | Pull a Docker Image | Complete the docker_image resource | `028-docker-image` |
| 029 | Level 2 - First Resources | Easy | 50 | Provision ACM Certificate | Complete the aws_acm_certificate resource | `029-provision-acm-certificate` |
| 030 | Level 2 - First Resources | Easy | 50 | Provision ALB Listener | Complete the aws_lb_listener resource | `030-provision-lb-listener` |
| 031 | Level 2 - First Resources | Easy | 50 | Provision ALB Target Group | Complete the aws_lb_target_group resource | `031-provision-target-group` |
| 032 | Level 2 - First Resources | Easy | 50 | Provision API Gateway Stage | Complete the aws_apigatewayv2_stage resource | `032-provision-api-stage` |
| 033 | Level 2 - First Resources | Easy | 50 | Provision AWS Backup Plan | Complete the aws_backup_plan resource | `033-provision-backup-plan` |
| 034 | Level 2 - First Resources | Easy | 50 | Provision AWS Backup Vault | Complete the aws_backup_vault resource | `034-provision-backup-vault` |
| 035 | Level 2 - First Resources | Easy | 50 | Provision Application Load Balancer | Complete the aws_lb resource | `035-provision-application-load-balancer` |
| 036 | Level 2 - First Resources | Easy | 50 | Provision Auto Scaling Group | Complete the aws_autoscaling_group resource | `036-provision-autoscaling-group` |
| 037 | Level 2 - First Resources | Easy | 50 | Provision CloudFront Distribution | Complete the aws_cloudfront_distribution resource | `037-provision-cloudfront` |
| 038 | Level 2 - First Resources | Easy | 50 | Provision CloudWatch CPU Alarm | Complete the aws_cloudwatch_metric_alarm resource | `038-provision-metric-alarm` |
| 039 | Level 2 - First Resources | Easy | 50 | Provision CloudWatch Log Group | Complete the aws_cloudwatch_log_group resource | `039-provision-log-group` |
| 040 | Level 2 - First Resources | Easy | 50 | Provision EBS Volume | Complete the aws_ebs_volume resource | `040-provision-ebs-volume` |
| 041 | Level 2 - First Resources | Easy | 50 | Provision EC2 Instance | Complete the aws_instance resource | `041-provision-ec2-instance` |
| 042 | Level 2 - First Resources | Easy | 50 | Provision EC2 Key Pair | Complete the aws_key_pair resource | `042-provision-key-pair` |
| 043 | Level 2 - First Resources | Easy | 50 | Provision EC2 Launch Template | Complete the aws_launch_template resource | `043-provision-launch-template` |
| 044 | Level 2 - First Resources | Easy | 50 | Provision ECS Cluster | Complete the aws_ecs_cluster resource | `044-provision-ecs-cluster` |
| 045 | Level 2 - First Resources | Easy | 50 | Provision ECS Task Definition | Complete the aws_ecs_task_definition resource | `045-provision-ecs-task-definition` |
| 046 | Level 2 - First Resources | Easy | 50 | Provision EFS File System | Complete the aws_efs_file_system resource | `046-provision-efs-file-system` |
| 047 | Level 2 - First Resources | Easy | 50 | Provision Elastic IP | Complete the aws_eip resource | `047-provision-elastic-ip` |
| 048 | Level 2 - First Resources | Easy | 50 | Provision EventBridge Schedule Rule | Complete the aws_cloudwatch_event_rule resource | `048-provision-eventbridge-rule` |
| 049 | Level 2 - First Resources | Easy | 50 | Provision HTTP API Gateway | Complete the aws_apigatewayv2_api resource | `049-provision-http-api` |
| 050 | Level 2 - First Resources | Easy | 50 | Provision IAM Policy | Complete the aws_iam_policy resource | `050-provision-iam-policy` |
| 051 | Level 2 - First Resources | Easy | 50 | Provision IAM Role | Complete the aws_iam_role resource | `051-provision-iam-role` |
| 052 | Level 2 - First Resources | Easy | 50 | Provision Internet Gateway | Complete the aws_internet_gateway resource | `052-provision-internet-gateway` |
| 053 | Level 2 - First Resources | Easy | 50 | Provision KMS Customer Key | Complete the aws_kms_key resource | `053-provision-kms-key` |
| 054 | Level 2 - First Resources | Easy | 50 | Provision Lambda Invoke Permission | Complete the aws_lambda_permission resource | `054-provision-lambda-permission` |
| 055 | Level 2 - First Resources | Easy | 50 | Provision NAT Gateway | Complete the aws_nat_gateway resource | `055-provision-nat-gateway` |
| 056 | Level 2 - First Resources | Easy | 50 | Provision Public Subnet | Complete the aws_subnet resource | `056-provision-public-subnet` |
| 057 | Level 2 - First Resources | Easy | 50 | Provision RDS Subnet Group | Complete the aws_db_subnet_group resource | `057-provision-db-subnet-group` |
| 058 | Level 2 - First Resources | Easy | 50 | Provision Route 53 A Record | Complete the aws_route53_record resource | `058-provision-route53-record` |
| 059 | Level 2 - First Resources | Easy | 50 | Provision Route 53 Hosted Zone | Complete the aws_route53_zone resource | `059-provision-route53-zone` |
| 060 | Level 2 - First Resources | Easy | 50 | Provision S3 Bucket | Complete the aws_s3_bucket resource | `060-provision-s3-bucket` |
| 061 | Level 2 - First Resources | Easy | 50 | Provision S3 Encryption Configuration | Complete the aws_s3_bucket_server_side_encryption_configuration resource | `061-provision-s3-encryption` |
| 062 | Level 2 - First Resources | Easy | 50 | Provision S3 Lifecycle Policy | Complete the aws_s3_bucket_lifecycle_configuration resource | `062-provision-s3-lifecycle` |
| 063 | Level 2 - First Resources | Easy | 50 | Provision S3 Public Access Block | Complete the aws_s3_bucket_public_access_block resource | `063-provision-s3-public-access-block` |
| 064 | Level 2 - First Resources | Easy | 50 | Provision S3 Versioning Configuration | Complete the aws_s3_bucket_versioning resource | `064-provision-s3-versioning` |
| 065 | Level 2 - First Resources | Easy | 50 | Provision SNS Topic | Complete the aws_sns_topic resource | `065-provision-sns-topic` |
| 066 | Level 2 - First Resources | Easy | 50 | Provision SSM Secure Parameter | Complete the aws_ssm_parameter resource | `066-provision-ssm-parameter` |
| 067 | Level 2 - First Resources | Easy | 50 | Provision Secrets Manager Secret | Complete the aws_secretsmanager_secret resource | `067-provision-secretsmanager-secret` |
| 068 | Level 2 - First Resources | Easy | 50 | Provision Security Group | Complete the aws_security_group resource | `068-provision-security-group` |
| 069 | Level 2 - First Resources | Easy | 50 | Provision VPC | Complete the aws_vpc resource | `069-provision-vpc` |
| 070 | Level 2 - First Resources | Easy | 50 | Provision VPC Route Table | Complete the aws_route_table resource | `070-provision-route-table` |
| 071 | Level 2 - First Resources | Easy | 55 | Run an Nginx Container | Complete the docker_container resource | `071-docker-container` |
| 072 | Level 3 - Real Infrastructure | Easy | 55 | Set CloudWatch Log Retention | Complete the aws_cloudwatch_log_group resource | `072-harden-cloudwatch-retention` |
| 073 | Level 3 - Real Infrastructure | Easy | 60 | Encrypted EBS Volume | Complete the aws_ebs_volume resource | `073-harden-ebs-encryption` |
| 074 | Level 3 - Real Infrastructure | Easy | 60 | Encrypted EFS File System | Complete the aws_efs_file_system resource | `074-harden-efs-encryption` |
| 075 | Level 3 - Real Infrastructure | Easy | 60 | Rotating KMS Customer Key | Complete the aws_kms_key resource | `075-harden-kms-rotation` |
| 076 | Level 3 - Real Infrastructure | Medium | 70 | Provision Lambda Function | Complete the aws_lambda_function resource | `076-provision-lambda-function` |
| 077 | Level 3 - Real Infrastructure | Medium | 70 | Provision SQS Queue | Complete the aws_sqs_queue resource | `077-provision-sqs-queue` |
| 078 | Level 3 - Real Infrastructure | Medium | 80 | Enable S3 Default Encryption | Complete the aws_s3_bucket_server_side_encryption_configuration resource | `078-harden-s3-encryption` |
| 079 | Level 3 - Real Infrastructure | Medium | 80 | Provision Cognito User Pool | Complete the aws_cognito_user_pool resource | `079-provision-cognito-user-pool` |
| 080 | Level 3 - Real Infrastructure | Medium | 80 | Provision DynamoDB Table | Complete the aws_dynamodb_table resource | `080-provision-dynamodb-table` |
| 081 | Level 3 - Real Infrastructure | Medium | 80 | Provision RDS PostgreSQL Instance | Complete the aws_db_instance resource | `081-provision-rds-instance` |
| 082 | Level 3 - Real Infrastructure | Medium | 80 | Provision Step Functions State Machine | Complete the aws_stepfunctions_state_machine resource | `082-provision-stepfunctions` |
| 083 | Level 3 - Real Infrastructure | Medium | 80 | Provision WAF Web ACL | Complete the aws_wafv2_web_acl resource | `083-provision-waf-web-acl` |
| 084 | Level 3 - Real Infrastructure | Medium | 80 | Two Containers on One Network | Complete the shared Docker network | `084-docker-multi-container` |
| 085 | Level 3 - Real Infrastructure | Medium | 85 | Secure a Secrets Manager Secret | Complete the aws_secretsmanager_secret resource | `085-harden-secretsmanager` |
| 086 | Level 3 - Real Infrastructure | Medium | 90 | Cap Lambda Timeout and Concurrency | Complete the aws_lambda_function resource | `086-harden-lambda-limits` |
| 087 | Level 3 - Real Infrastructure | Medium | 90 | Deny S3 Requests Without TLS | Complete the aws_s3_bucket_policy resource | `087-harden-s3-tls-policy` |
| 088 | Level 3 - Real Infrastructure | Medium | 90 | Enforce IMDSv2 on EC2 | Complete the aws_launch_template resource | `088-harden-ec2-imdsv2` |
| 089 | Level 3 - Real Infrastructure | Medium | 90 | Harden a DynamoDB Table | Complete the aws_dynamodb_table resource | `089-harden-dynamodb` |
| 090 | Level 3 - Real Infrastructure | Medium | 90 | Lock Down S3 Public Access | Complete the aws_s3_bucket_public_access_block resource | `090-harden-s3-public-access` |
| 091 | Level 3 - Real Infrastructure | Medium | 90 | Security Group Without Public SSH | Complete the aws_security_group resource | `091-harden-sg-no-ssh` |
| 092 | Level 3 - Real Infrastructure | Medium | 100 | Enable VPC Flow Logs | Complete the aws_flow_log resource | `092-harden-vpc-flow-logs` |
| 093 | Level 3 - Real Infrastructure | Medium | 100 | SQS Queue With Dead-Letter Queue | Complete the main queue | `093-harden-sqs-dlq` |
| 094 | Level 3 - Real Infrastructure | Medium | 100 | Versioning + Lifecycle Expiry | Complete the aws_s3_bucket_versioning resource | `094-harden-s3-versioning-lifecycle` |
| 095 | Level 4 - Composition | Medium | 95 | CPU Alarm to SNS | Complete the aws_cloudwatch_metric_alarm resource | `095-wire-cloudwatch-alarm-sns` |
| 096 | Level 4 - Composition | Medium | 100 | AWS Backup Vault + Plan | Complete the aws_backup_plan resource | `096-wire-backup-vault-plan` |
| 097 | Level 4 - Composition | Medium | 100 | Fan Out SNS to SQS | Complete the aws_sns_topic_subscription resource | `097-wire-sqs-sns` |
| 098 | Level 4 - Composition | Medium | 100 | IAM Role + Policy + Attachment | Complete the aws_iam_role_policy_attachment resource | `098-wire-iam-role-policy` |
| 099 | Level 4 - Composition | Medium | 110 | KMS Key + Alias + S3 Encryption | Complete the aws_s3_bucket_server_side_encryption_configuration resource | `099-wire-kms-s3` |
| 100 | Level 4 - Composition | Medium | 110 | RDS Instance in a Subnet Group | Complete the aws_db_instance resource | `100-wire-rds-subnet-group` |
| 101 | Level 4 - Composition | Hard | 120 | CloudFront HTTPS-Only Distribution | Complete the aws_cloudfront_distribution resource | `101-harden-cloudfront-https` |
| 102 | Level 4 - Composition | Medium | 120 | EC2 Instance + Security Group + EIP | Complete the aws_instance resource | `102-wire-ec2-sg-eip` |
| 103 | Level 4 - Composition | Hard | 120 | Encrypt S3 With a Customer KMS Key | Complete the aws_s3_bucket_server_side_encryption_configuration resource | `103-harden-s3-kms` |
| 104 | Level 4 - Composition | Hard | 120 | Least-Privilege IAM Policy | Complete the aws_iam_policy resource | `104-harden-iam-least-privilege` |
| 105 | Level 4 - Composition | Hard | 120 | Secrets Manager + RDS | Complete the aws_db_instance resource | `105-wire-secrets-rds` |
| 106 | Level 4 - Composition | Medium | 120 | Wire an ALB to a Target Group | Complete the aws_lb_listener resource | `106-wire-alb-target-listener` |
| 107 | Level 4 - Composition | Hard | 130 | ALB HTTPS Listener + Redirect | Complete the HTTPS listener | `107-harden-alb-https` |
| 108 | Level 4 - Composition | Hard | 130 | Harden an RDS Instance | Complete the aws_db_instance resource | `108-harden-rds` |
| 109 | Level 4 - Composition | Hard | 130 | Scheduled EventBridge to Lambda | Complete the scheduled function | `109-wire-eventbridge-lambda` |
| 110 | Level 4 - Composition | Medium | 140 | Build a Public VPC Foundation | Complete the aws_subnet resource | `110-wire-vpc-public-foundation` |
| 111 | Level 4 - Composition | Hard | 140 | Lambda Reading a DynamoDB Table | Complete the aws_lambda_function resource | `111-wire-lambda-dynamodb` |
| 112 | Level 4 - Composition | Hard | 150 | HTTP API Gateway to Lambda | Complete the aws_apigatewayv2_integration resource | `112-wire-apigw-lambda` |
| 113 | Level 4 - Composition | Hard | 150 | Route 53 + ACM + CloudFront | Complete the aws_cloudfront_distribution resource | `113-wire-route53-cloudfront-acm` |
| 114 | Level 4 - Composition | Hard | 160 | ECS Fargate Service Behind an ALB | Complete the aws_ecs_service resource | `114-wire-ecs-alb-service` |
| 115 | Level 5 - Modules & Capstones | Medium | 75 | Refactor With a moved Block | Complete the moved block | `115-refactor-moved-block` |
| 116 | Level 5 - Modules & Capstones | Medium | 75 | Workspace-Aware Naming | Complete the workspace-aware locals block | `116-state-workspaces` |
| 117 | Level 5 - Modules & Capstones | Medium | 80 | Call a Local Module | Complete the module call | `117-mod-local-module` |
| 118 | Level 5 - Modules & Capstones | Medium | 80 | Import Existing Resources | Complete the import block | `118-import-block` |
| 119 | Level 5 - Modules & Capstones | Medium | 90 | Remote State in S3 + DynamoDB | Complete the S3 backend configuration | `119-state-s3-backend` |
| 120 | Level 5 - Modules & Capstones | Easy | 100 | Docker Nginx Sandbox | Complete the Nginx container | `120-docker-nginx-sandbox` |
| 121 | Level 5 - Modules & Capstones | Hard | 100 | Module for_each | Complete the for_each module call | `121-mod-module-for-each` |
| 122 | Level 5 - Modules & Capstones | Easy | 100 | Secure S3 Bucket Provisioning | Complete the S3 bucket resource | `122-secure-s3-bucket` |
| 123 | Level 5 - Modules & Capstones | Medium | 150 | Highly Available VPC Foundation | Complete the public subnet definition | `123-ha-vpc-foundation` |
| 124 | Level 5 - Modules & Capstones | Hard | 250 | Auto Scaling Web Tier | Complete the Auto Scaling group | `124-autoscaling-web-tier` |
| 125 | Level 5 - Modules & Capstones | Hard | 300 | Serverless Item API | Complete the Lambda function | `125-serverless-item-api` |
