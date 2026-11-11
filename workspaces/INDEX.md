# Terraform Arena - Challenge Index

117 challenges, ordered from level 0 (HCL basics) to level 5 (capstones).

| # | Level | Difficulty | Points | Challenge | Focus | Folder |
| --- | --- | --- | --- | --- | --- | --- |
| 001 | Level 0 - HCL Foundations | Easy | 40 | Your First HCL Block | Complete the locals block | `001-intro-hcl-blocks` |
| 002 | Level 0 - HCL Foundations | Easy | 45 | Arguments and Variable Blocks | Complete the variable block | `002-intro-hcl-arguments` |
| 003 | Level 0 - HCL Foundations | Easy | 45 | Strings and Interpolation | Complete the greeting output | `003-intro-hcl-strings` |
| 004 | Level 0 - HCL Foundations | Easy | 50 | Format HCL by Hand | Fix the formatting | `004-intro-hcl-formatting` |
| 005 | Level 0 - HCL Foundations | Easy | 50 | Lists and Maps | Complete the collections | `005-intro-hcl-collections` |
| 006 | Level 0 - HCL Foundations | Easy | 50 | Provider and Version Blocks | Complete the provider block | `006-intro-provider-block` |
| 007 | Level 0 - HCL Foundations | Easy | 55 | Split a Configuration Across Files | Complete the bucket resource | `007-intro-file-layout` |
| 008 | Level 1 - Terraform Language | Easy | 50 | Sensitive Output | Mark the output as sensitive | `008-lang-sensitive-output` |
| 009 | Level 1 - Terraform Language | Easy | 55 | Compose Tags With merge() | Complete the locals block | `009-lang-functions-merge` |
| 010 | Level 1 - Terraform Language | Easy | 55 | Conditional Expressions | Complete the bucket name expression | `010-lang-conditional-environment` |
| 011 | Level 1 - Terraform Language | Easy | 55 | Explicit depends_on | Add the explicit dependency | `011-lang-depends-on` |
| 012 | Level 1 - Terraform Language | Easy | 55 | Locals for Common Tags | Complete the shared tags locals block | `012-lang-locals-common-tags` |
| 013 | Level 1 - Terraform Language | Easy | 55 | Protect a Bucket With prevent_destroy | Complete the lifecycle block | `013-lang-lifecycle-protect` |
| 014 | Level 1 - Terraform Language | Easy | 60 | Discover an AMI With a Data Source | Complete the aws_ami data source | `014-lang-data-sources` |
| 015 | Level 1 - Terraform Language | Easy | 60 | Variable Validation | Complete the validation block for bucket_name | `015-lang-variables-validation` |
| 016 | Level 1 - Terraform Language | Medium | 90 | Create Subnets With count | Complete the aws_subnet block | `016-lang-count-subnets` |
| 017 | Level 1 - Terraform Language | Medium | 95 | Create Subnets With for_each | Complete the aws_subnet block | `017-lang-for-each-subnets` |
| 018 | Level 2 - First Resources | Easy | 40 | Create a Docker Network | Complete the docker_network resource | `018-docker-network` |
| 019 | Level 2 - First Resources | Easy | 40 | Create a Docker Volume | Complete the docker_volume resource | `019-docker-volume` |
| 020 | Level 2 - First Resources | Easy | 45 | Pull a Docker Image | Complete the docker_image resource | `020-docker-image` |
| 021 | Level 2 - First Resources | Easy | 50 | Provision ACM Certificate | Complete the aws_acm_certificate resource | `021-provision-acm-certificate` |
| 022 | Level 2 - First Resources | Easy | 50 | Provision ALB Listener | Complete the aws_lb_listener resource | `022-provision-lb-listener` |
| 023 | Level 2 - First Resources | Easy | 50 | Provision ALB Target Group | Complete the aws_lb_target_group resource | `023-provision-target-group` |
| 024 | Level 2 - First Resources | Easy | 50 | Provision API Gateway Stage | Complete the aws_apigatewayv2_stage resource | `024-provision-api-stage` |
| 025 | Level 2 - First Resources | Easy | 50 | Provision AWS Backup Plan | Complete the aws_backup_plan resource | `025-provision-backup-plan` |
| 026 | Level 2 - First Resources | Easy | 50 | Provision AWS Backup Vault | Complete the aws_backup_vault resource | `026-provision-backup-vault` |
| 027 | Level 2 - First Resources | Easy | 50 | Provision Application Load Balancer | Complete the aws_lb resource | `027-provision-application-load-balancer` |
| 028 | Level 2 - First Resources | Easy | 50 | Provision Auto Scaling Group | Complete the aws_autoscaling_group resource | `028-provision-autoscaling-group` |
| 029 | Level 2 - First Resources | Easy | 50 | Provision CloudFront Distribution | Complete the aws_cloudfront_distribution resource | `029-provision-cloudfront` |
| 030 | Level 2 - First Resources | Easy | 50 | Provision CloudWatch CPU Alarm | Complete the aws_cloudwatch_metric_alarm resource | `030-provision-metric-alarm` |
| 031 | Level 2 - First Resources | Easy | 50 | Provision CloudWatch Log Group | Complete the aws_cloudwatch_log_group resource | `031-provision-log-group` |
| 032 | Level 2 - First Resources | Easy | 50 | Provision EBS Volume | Complete the aws_ebs_volume resource | `032-provision-ebs-volume` |
| 033 | Level 2 - First Resources | Easy | 50 | Provision EC2 Instance | Complete the aws_instance resource | `033-provision-ec2-instance` |
| 034 | Level 2 - First Resources | Easy | 50 | Provision EC2 Key Pair | Complete the aws_key_pair resource | `034-provision-key-pair` |
| 035 | Level 2 - First Resources | Easy | 50 | Provision EC2 Launch Template | Complete the aws_launch_template resource | `035-provision-launch-template` |
| 036 | Level 2 - First Resources | Easy | 50 | Provision ECS Cluster | Complete the aws_ecs_cluster resource | `036-provision-ecs-cluster` |
| 037 | Level 2 - First Resources | Easy | 50 | Provision ECS Task Definition | Complete the aws_ecs_task_definition resource | `037-provision-ecs-task-definition` |
| 038 | Level 2 - First Resources | Easy | 50 | Provision EFS File System | Complete the aws_efs_file_system resource | `038-provision-efs-file-system` |
| 039 | Level 2 - First Resources | Easy | 50 | Provision Elastic IP | Complete the aws_eip resource | `039-provision-elastic-ip` |
| 040 | Level 2 - First Resources | Easy | 50 | Provision EventBridge Schedule Rule | Complete the aws_cloudwatch_event_rule resource | `040-provision-eventbridge-rule` |
| 041 | Level 2 - First Resources | Easy | 50 | Provision HTTP API Gateway | Complete the aws_apigatewayv2_api resource | `041-provision-http-api` |
| 042 | Level 2 - First Resources | Easy | 50 | Provision IAM Policy | Complete the aws_iam_policy resource | `042-provision-iam-policy` |
| 043 | Level 2 - First Resources | Easy | 50 | Provision IAM Role | Complete the aws_iam_role resource | `043-provision-iam-role` |
| 044 | Level 2 - First Resources | Easy | 50 | Provision Internet Gateway | Complete the aws_internet_gateway resource | `044-provision-internet-gateway` |
| 045 | Level 2 - First Resources | Easy | 50 | Provision KMS Customer Key | Complete the aws_kms_key resource | `045-provision-kms-key` |
| 046 | Level 2 - First Resources | Easy | 50 | Provision Lambda Invoke Permission | Complete the aws_lambda_permission resource | `046-provision-lambda-permission` |
| 047 | Level 2 - First Resources | Easy | 50 | Provision NAT Gateway | Complete the aws_nat_gateway resource | `047-provision-nat-gateway` |
| 048 | Level 2 - First Resources | Easy | 50 | Provision Public Subnet | Complete the aws_subnet resource | `048-provision-public-subnet` |
| 049 | Level 2 - First Resources | Easy | 50 | Provision RDS Subnet Group | Complete the aws_db_subnet_group resource | `049-provision-db-subnet-group` |
| 050 | Level 2 - First Resources | Easy | 50 | Provision Route 53 A Record | Complete the aws_route53_record resource | `050-provision-route53-record` |
| 051 | Level 2 - First Resources | Easy | 50 | Provision Route 53 Hosted Zone | Complete the aws_route53_zone resource | `051-provision-route53-zone` |
| 052 | Level 2 - First Resources | Easy | 50 | Provision S3 Bucket | Complete the aws_s3_bucket resource | `052-provision-s3-bucket` |
| 053 | Level 2 - First Resources | Easy | 50 | Provision S3 Encryption Configuration | Complete the aws_s3_bucket_server_side_encryption_configuration resource | `053-provision-s3-encryption` |
| 054 | Level 2 - First Resources | Easy | 50 | Provision S3 Lifecycle Policy | Complete the aws_s3_bucket_lifecycle_configuration resource | `054-provision-s3-lifecycle` |
| 055 | Level 2 - First Resources | Easy | 50 | Provision S3 Public Access Block | Complete the aws_s3_bucket_public_access_block resource | `055-provision-s3-public-access-block` |
| 056 | Level 2 - First Resources | Easy | 50 | Provision S3 Versioning Configuration | Complete the aws_s3_bucket_versioning resource | `056-provision-s3-versioning` |
| 057 | Level 2 - First Resources | Easy | 50 | Provision SNS Topic | Complete the aws_sns_topic resource | `057-provision-sns-topic` |
| 058 | Level 2 - First Resources | Easy | 50 | Provision SSM Secure Parameter | Complete the aws_ssm_parameter resource | `058-provision-ssm-parameter` |
| 059 | Level 2 - First Resources | Easy | 50 | Provision Secrets Manager Secret | Complete the aws_secretsmanager_secret resource | `059-provision-secretsmanager-secret` |
| 060 | Level 2 - First Resources | Easy | 50 | Provision Security Group | Complete the aws_security_group resource | `060-provision-security-group` |
| 061 | Level 2 - First Resources | Easy | 50 | Provision VPC | Complete the aws_vpc resource | `061-provision-vpc` |
| 062 | Level 2 - First Resources | Easy | 50 | Provision VPC Route Table | Complete the aws_route_table resource | `062-provision-route-table` |
| 063 | Level 2 - First Resources | Easy | 55 | Run an Nginx Container | Complete the docker_container resource | `063-docker-container` |
| 064 | Level 3 - Real Infrastructure | Easy | 55 | Set CloudWatch Log Retention | Complete the aws_cloudwatch_log_group resource | `064-harden-cloudwatch-retention` |
| 065 | Level 3 - Real Infrastructure | Easy | 60 | Encrypted EBS Volume | Complete the aws_ebs_volume resource | `065-harden-ebs-encryption` |
| 066 | Level 3 - Real Infrastructure | Easy | 60 | Encrypted EFS File System | Complete the aws_efs_file_system resource | `066-harden-efs-encryption` |
| 067 | Level 3 - Real Infrastructure | Easy | 60 | Rotating KMS Customer Key | Complete the aws_kms_key resource | `067-harden-kms-rotation` |
| 068 | Level 3 - Real Infrastructure | Medium | 70 | Provision Lambda Function | Complete the aws_lambda_function resource | `068-provision-lambda-function` |
| 069 | Level 3 - Real Infrastructure | Medium | 70 | Provision SQS Queue | Complete the aws_sqs_queue resource | `069-provision-sqs-queue` |
| 070 | Level 3 - Real Infrastructure | Medium | 80 | Enable S3 Default Encryption | Complete the aws_s3_bucket_server_side_encryption_configuration resource | `070-harden-s3-encryption` |
| 071 | Level 3 - Real Infrastructure | Medium | 80 | Provision Cognito User Pool | Complete the aws_cognito_user_pool resource | `071-provision-cognito-user-pool` |
| 072 | Level 3 - Real Infrastructure | Medium | 80 | Provision DynamoDB Table | Complete the aws_dynamodb_table resource | `072-provision-dynamodb-table` |
| 073 | Level 3 - Real Infrastructure | Medium | 80 | Provision RDS PostgreSQL Instance | Complete the aws_db_instance resource | `073-provision-rds-instance` |
| 074 | Level 3 - Real Infrastructure | Medium | 80 | Provision Step Functions State Machine | Complete the aws_stepfunctions_state_machine resource | `074-provision-stepfunctions` |
| 075 | Level 3 - Real Infrastructure | Medium | 80 | Provision WAF Web ACL | Complete the aws_wafv2_web_acl resource | `075-provision-waf-web-acl` |
| 076 | Level 3 - Real Infrastructure | Medium | 80 | Two Containers on One Network | Complete the shared Docker network | `076-docker-multi-container` |
| 077 | Level 3 - Real Infrastructure | Medium | 85 | Secure a Secrets Manager Secret | Complete the aws_secretsmanager_secret resource | `077-harden-secretsmanager` |
| 078 | Level 3 - Real Infrastructure | Medium | 90 | Cap Lambda Timeout and Concurrency | Complete the aws_lambda_function resource | `078-harden-lambda-limits` |
| 079 | Level 3 - Real Infrastructure | Medium | 90 | Deny S3 Requests Without TLS | Complete the aws_s3_bucket_policy resource | `079-harden-s3-tls-policy` |
| 080 | Level 3 - Real Infrastructure | Medium | 90 | Enforce IMDSv2 on EC2 | Complete the aws_launch_template resource | `080-harden-ec2-imdsv2` |
| 081 | Level 3 - Real Infrastructure | Medium | 90 | Harden a DynamoDB Table | Complete the aws_dynamodb_table resource | `081-harden-dynamodb` |
| 082 | Level 3 - Real Infrastructure | Medium | 90 | Lock Down S3 Public Access | Complete the aws_s3_bucket_public_access_block resource | `082-harden-s3-public-access` |
| 083 | Level 3 - Real Infrastructure | Medium | 90 | Security Group Without Public SSH | Complete the aws_security_group resource | `083-harden-sg-no-ssh` |
| 084 | Level 3 - Real Infrastructure | Medium | 100 | Enable VPC Flow Logs | Complete the aws_flow_log resource | `084-harden-vpc-flow-logs` |
| 085 | Level 3 - Real Infrastructure | Medium | 100 | SQS Queue With Dead-Letter Queue | Complete the main queue | `085-harden-sqs-dlq` |
| 086 | Level 3 - Real Infrastructure | Medium | 100 | Versioning + Lifecycle Expiry | Complete the aws_s3_bucket_versioning resource | `086-harden-s3-versioning-lifecycle` |
| 087 | Level 4 - Composition | Medium | 95 | CPU Alarm to SNS | Complete the aws_cloudwatch_metric_alarm resource | `087-wire-cloudwatch-alarm-sns` |
| 088 | Level 4 - Composition | Medium | 100 | AWS Backup Vault + Plan | Complete the aws_backup_plan resource | `088-wire-backup-vault-plan` |
| 089 | Level 4 - Composition | Medium | 100 | Fan Out SNS to SQS | Complete the aws_sns_topic_subscription resource | `089-wire-sqs-sns` |
| 090 | Level 4 - Composition | Medium | 100 | IAM Role + Policy + Attachment | Complete the aws_iam_role_policy_attachment resource | `090-wire-iam-role-policy` |
| 091 | Level 4 - Composition | Medium | 110 | KMS Key + Alias + S3 Encryption | Complete the aws_s3_bucket_server_side_encryption_configuration resource | `091-wire-kms-s3` |
| 092 | Level 4 - Composition | Medium | 110 | RDS Instance in a Subnet Group | Complete the aws_db_instance resource | `092-wire-rds-subnet-group` |
| 093 | Level 4 - Composition | Hard | 120 | CloudFront HTTPS-Only Distribution | Complete the aws_cloudfront_distribution resource | `093-harden-cloudfront-https` |
| 094 | Level 4 - Composition | Medium | 120 | EC2 Instance + Security Group + EIP | Complete the aws_instance resource | `094-wire-ec2-sg-eip` |
| 095 | Level 4 - Composition | Hard | 120 | Encrypt S3 With a Customer KMS Key | Complete the aws_s3_bucket_server_side_encryption_configuration resource | `095-harden-s3-kms` |
| 096 | Level 4 - Composition | Hard | 120 | Least-Privilege IAM Policy | Complete the aws_iam_policy resource | `096-harden-iam-least-privilege` |
| 097 | Level 4 - Composition | Hard | 120 | Secrets Manager + RDS | Complete the aws_db_instance resource | `097-wire-secrets-rds` |
| 098 | Level 4 - Composition | Medium | 120 | Wire an ALB to a Target Group | Complete the aws_lb_listener resource | `098-wire-alb-target-listener` |
| 099 | Level 4 - Composition | Hard | 130 | ALB HTTPS Listener + Redirect | Complete the HTTPS listener | `099-harden-alb-https` |
| 100 | Level 4 - Composition | Hard | 130 | Harden an RDS Instance | Complete the aws_db_instance resource | `100-harden-rds` |
| 101 | Level 4 - Composition | Hard | 130 | Scheduled EventBridge to Lambda | Complete the scheduled function | `101-wire-eventbridge-lambda` |
| 102 | Level 4 - Composition | Medium | 140 | Build a Public VPC Foundation | Complete the aws_subnet resource | `102-wire-vpc-public-foundation` |
| 103 | Level 4 - Composition | Hard | 140 | Lambda Reading a DynamoDB Table | Complete the aws_lambda_function resource | `103-wire-lambda-dynamodb` |
| 104 | Level 4 - Composition | Hard | 150 | HTTP API Gateway to Lambda | Complete the aws_apigatewayv2_integration resource | `104-wire-apigw-lambda` |
| 105 | Level 4 - Composition | Hard | 150 | Route 53 + ACM + CloudFront | Complete the aws_cloudfront_distribution resource | `105-wire-route53-cloudfront-acm` |
| 106 | Level 4 - Composition | Hard | 160 | ECS Fargate Service Behind an ALB | Complete the aws_ecs_service resource | `106-wire-ecs-alb-service` |
| 107 | Level 5 - Modules & Capstones | Medium | 75 | Refactor With a moved Block | Complete the moved block | `107-refactor-moved-block` |
| 108 | Level 5 - Modules & Capstones | Medium | 75 | Workspace-Aware Naming | Complete the workspace-aware locals block | `108-state-workspaces` |
| 109 | Level 5 - Modules & Capstones | Medium | 80 | Call a Local Module | Complete the module call | `109-mod-local-module` |
| 110 | Level 5 - Modules & Capstones | Medium | 80 | Import Existing Resources | Complete the import block | `110-import-block` |
| 111 | Level 5 - Modules & Capstones | Medium | 90 | Remote State in S3 + DynamoDB | Complete the S3 backend configuration | `111-state-s3-backend` |
| 112 | Level 5 - Modules & Capstones | Easy | 100 | Docker Nginx Sandbox | Complete the Nginx container | `112-docker-nginx-sandbox` |
| 113 | Level 5 - Modules & Capstones | Hard | 100 | Module for_each | Complete the for_each module call | `113-mod-module-for-each` |
| 114 | Level 5 - Modules & Capstones | Easy | 100 | Secure S3 Bucket Provisioning | Complete the S3 bucket resource | `114-secure-s3-bucket` |
| 115 | Level 5 - Modules & Capstones | Medium | 150 | Highly Available VPC Foundation | Complete the public subnet definition | `115-ha-vpc-foundation` |
| 116 | Level 5 - Modules & Capstones | Hard | 250 | Auto Scaling Web Tier | Complete the Auto Scaling group | `116-autoscaling-web-tier` |
| 117 | Level 5 - Modules & Capstones | Hard | 300 | Serverless Item API | Complete the Lambda function | `117-serverless-item-api` |
