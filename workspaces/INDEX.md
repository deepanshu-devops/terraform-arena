# Terraform Arena - Challenge Index

135 challenges, ordered from level 0 (HCL basics) to level 5 (capstones).

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
| 016 | Level 0 - HCL Foundations | Easy | 64 | Tutorial: Reuse a Value With a Variable | Declare the input variable | `016-tut-variable-first` |
| 017 | Level 0 - HCL Foundations | Easy | 65 | Tutorial: Work With a List | Create the ordered list | `017-tut-list-first` |
| 018 | Level 0 - HCL Foundations | Easy | 66 | Tutorial: Look Up Values in a Map | Create the lookup map | `018-tut-map-first` |
| 019 | Level 0 - HCL Foundations | Easy | 67 | Tutorial: Compose Strings With Functions | Build the derived strings | `019-tut-functions-first` |
| 020 | Level 0 - HCL Foundations | Easy | 68 | Tutorial: Transform a List With for | Derive the collections | `020-tut-for-expression` |
| 021 | Level 0 - HCL Foundations | Easy | 69 | Tutorial: Repeat a Resource With count | Repeat the bucket | `021-tut-count-first` |
| 022 | Level 0 - HCL Foundations | Easy | 70 | Tutorial: Name Instances With for_each | Create named instances | `022-tut-for-each-first` |
| 023 | Level 0 - HCL Foundations | Easy | 71 | Tutorial: Call Your First Module | Complete the module call | `023-tut-module-call` |
| 024 | Level 0 - HCL Foundations | Easy | 72 | Tutorial: Read a Module Output | Wire the module output | `024-tut-module-output` |
| 025 | Level 0 - HCL Foundations | Easy | 73 | Tutorial: Put It All Together | Build the module input map | `025-tut-capstone-compose` |
| 026 | Level 1 - Terraform Language | Easy | 50 | Sensitive Output | Mark the output as sensitive | `026-lang-sensitive-output` |
| 027 | Level 1 - Terraform Language | Easy | 55 | Compose Tags With merge() | Complete the locals block | `027-lang-functions-merge` |
| 028 | Level 1 - Terraform Language | Easy | 55 | Conditional Expressions | Complete the bucket name expression | `028-lang-conditional-environment` |
| 029 | Level 1 - Terraform Language | Easy | 55 | Explicit depends_on | Add the explicit dependency | `029-lang-depends-on` |
| 030 | Level 1 - Terraform Language | Easy | 55 | Locals for Common Tags | Complete the shared tags locals block | `030-lang-locals-common-tags` |
| 031 | Level 1 - Terraform Language | Easy | 55 | Protect a Bucket With prevent_destroy | Complete the lifecycle block | `031-lang-lifecycle-protect` |
| 032 | Level 1 - Terraform Language | Easy | 60 | Discover an AMI With a Data Source | Complete the aws_ami data source | `032-lang-data-sources` |
| 033 | Level 1 - Terraform Language | Easy | 60 | Variable Validation | Complete the validation block for bucket_name | `033-lang-variables-validation` |
| 034 | Level 1 - Terraform Language | Medium | 90 | Create Subnets With count | Complete the aws_subnet block | `034-lang-count-subnets` |
| 035 | Level 1 - Terraform Language | Medium | 95 | Create Subnets With for_each | Complete the aws_subnet block | `035-lang-for-each-subnets` |
| 036 | Level 2 - First Resources | Easy | 40 | Create a Docker Network | Complete the docker_network resource | `036-docker-network` |
| 037 | Level 2 - First Resources | Easy | 40 | Create a Docker Volume | Complete the docker_volume resource | `037-docker-volume` |
| 038 | Level 2 - First Resources | Easy | 45 | Pull a Docker Image | Complete the docker_image resource | `038-docker-image` |
| 039 | Level 2 - First Resources | Easy | 50 | Provision ACM Certificate | Complete the aws_acm_certificate resource | `039-provision-acm-certificate` |
| 040 | Level 2 - First Resources | Easy | 50 | Provision ALB Listener | Complete the aws_lb_listener resource | `040-provision-lb-listener` |
| 041 | Level 2 - First Resources | Easy | 50 | Provision ALB Target Group | Complete the aws_lb_target_group resource | `041-provision-target-group` |
| 042 | Level 2 - First Resources | Easy | 50 | Provision API Gateway Stage | Complete the aws_apigatewayv2_stage resource | `042-provision-api-stage` |
| 043 | Level 2 - First Resources | Easy | 50 | Provision AWS Backup Plan | Complete the aws_backup_plan resource | `043-provision-backup-plan` |
| 044 | Level 2 - First Resources | Easy | 50 | Provision AWS Backup Vault | Complete the aws_backup_vault resource | `044-provision-backup-vault` |
| 045 | Level 2 - First Resources | Easy | 50 | Provision Application Load Balancer | Complete the aws_lb resource | `045-provision-application-load-balancer` |
| 046 | Level 2 - First Resources | Easy | 50 | Provision Auto Scaling Group | Complete the aws_autoscaling_group resource | `046-provision-autoscaling-group` |
| 047 | Level 2 - First Resources | Easy | 50 | Provision CloudFront Distribution | Complete the aws_cloudfront_distribution resource | `047-provision-cloudfront` |
| 048 | Level 2 - First Resources | Easy | 50 | Provision CloudWatch CPU Alarm | Complete the aws_cloudwatch_metric_alarm resource | `048-provision-metric-alarm` |
| 049 | Level 2 - First Resources | Easy | 50 | Provision CloudWatch Log Group | Complete the aws_cloudwatch_log_group resource | `049-provision-log-group` |
| 050 | Level 2 - First Resources | Easy | 50 | Provision EBS Volume | Complete the aws_ebs_volume resource | `050-provision-ebs-volume` |
| 051 | Level 2 - First Resources | Easy | 50 | Provision EC2 Instance | Complete the aws_instance resource | `051-provision-ec2-instance` |
| 052 | Level 2 - First Resources | Easy | 50 | Provision EC2 Key Pair | Complete the aws_key_pair resource | `052-provision-key-pair` |
| 053 | Level 2 - First Resources | Easy | 50 | Provision EC2 Launch Template | Complete the aws_launch_template resource | `053-provision-launch-template` |
| 054 | Level 2 - First Resources | Easy | 50 | Provision ECS Cluster | Complete the aws_ecs_cluster resource | `054-provision-ecs-cluster` |
| 055 | Level 2 - First Resources | Easy | 50 | Provision ECS Task Definition | Complete the aws_ecs_task_definition resource | `055-provision-ecs-task-definition` |
| 056 | Level 2 - First Resources | Easy | 50 | Provision EFS File System | Complete the aws_efs_file_system resource | `056-provision-efs-file-system` |
| 057 | Level 2 - First Resources | Easy | 50 | Provision Elastic IP | Complete the aws_eip resource | `057-provision-elastic-ip` |
| 058 | Level 2 - First Resources | Easy | 50 | Provision EventBridge Schedule Rule | Complete the aws_cloudwatch_event_rule resource | `058-provision-eventbridge-rule` |
| 059 | Level 2 - First Resources | Easy | 50 | Provision HTTP API Gateway | Complete the aws_apigatewayv2_api resource | `059-provision-http-api` |
| 060 | Level 2 - First Resources | Easy | 50 | Provision IAM Policy | Complete the aws_iam_policy resource | `060-provision-iam-policy` |
| 061 | Level 2 - First Resources | Easy | 50 | Provision IAM Role | Complete the aws_iam_role resource | `061-provision-iam-role` |
| 062 | Level 2 - First Resources | Easy | 50 | Provision Internet Gateway | Complete the aws_internet_gateway resource | `062-provision-internet-gateway` |
| 063 | Level 2 - First Resources | Easy | 50 | Provision KMS Customer Key | Complete the aws_kms_key resource | `063-provision-kms-key` |
| 064 | Level 2 - First Resources | Easy | 50 | Provision Lambda Invoke Permission | Complete the aws_lambda_permission resource | `064-provision-lambda-permission` |
| 065 | Level 2 - First Resources | Easy | 50 | Provision NAT Gateway | Complete the aws_nat_gateway resource | `065-provision-nat-gateway` |
| 066 | Level 2 - First Resources | Easy | 50 | Provision Public Subnet | Complete the aws_subnet resource | `066-provision-public-subnet` |
| 067 | Level 2 - First Resources | Easy | 50 | Provision RDS Subnet Group | Complete the aws_db_subnet_group resource | `067-provision-db-subnet-group` |
| 068 | Level 2 - First Resources | Easy | 50 | Provision Route 53 A Record | Complete the aws_route53_record resource | `068-provision-route53-record` |
| 069 | Level 2 - First Resources | Easy | 50 | Provision Route 53 Hosted Zone | Complete the aws_route53_zone resource | `069-provision-route53-zone` |
| 070 | Level 2 - First Resources | Easy | 50 | Provision S3 Bucket | Complete the aws_s3_bucket resource | `070-provision-s3-bucket` |
| 071 | Level 2 - First Resources | Easy | 50 | Provision S3 Encryption Configuration | Complete the aws_s3_bucket_server_side_encryption_configuration resource | `071-provision-s3-encryption` |
| 072 | Level 2 - First Resources | Easy | 50 | Provision S3 Lifecycle Policy | Complete the aws_s3_bucket_lifecycle_configuration resource | `072-provision-s3-lifecycle` |
| 073 | Level 2 - First Resources | Easy | 50 | Provision S3 Public Access Block | Complete the aws_s3_bucket_public_access_block resource | `073-provision-s3-public-access-block` |
| 074 | Level 2 - First Resources | Easy | 50 | Provision S3 Versioning Configuration | Complete the aws_s3_bucket_versioning resource | `074-provision-s3-versioning` |
| 075 | Level 2 - First Resources | Easy | 50 | Provision SNS Topic | Complete the aws_sns_topic resource | `075-provision-sns-topic` |
| 076 | Level 2 - First Resources | Easy | 50 | Provision SSM Secure Parameter | Complete the aws_ssm_parameter resource | `076-provision-ssm-parameter` |
| 077 | Level 2 - First Resources | Easy | 50 | Provision Secrets Manager Secret | Complete the aws_secretsmanager_secret resource | `077-provision-secretsmanager-secret` |
| 078 | Level 2 - First Resources | Easy | 50 | Provision Security Group | Complete the aws_security_group resource | `078-provision-security-group` |
| 079 | Level 2 - First Resources | Easy | 50 | Provision VPC | Complete the aws_vpc resource | `079-provision-vpc` |
| 080 | Level 2 - First Resources | Easy | 50 | Provision VPC Route Table | Complete the aws_route_table resource | `080-provision-route-table` |
| 081 | Level 2 - First Resources | Easy | 55 | Run an Nginx Container | Complete the docker_container resource | `081-docker-container` |
| 082 | Level 3 - Real Infrastructure | Easy | 55 | Set CloudWatch Log Retention | Complete the aws_cloudwatch_log_group resource | `082-harden-cloudwatch-retention` |
| 083 | Level 3 - Real Infrastructure | Easy | 60 | Encrypted EBS Volume | Complete the aws_ebs_volume resource | `083-harden-ebs-encryption` |
| 084 | Level 3 - Real Infrastructure | Easy | 60 | Encrypted EFS File System | Complete the aws_efs_file_system resource | `084-harden-efs-encryption` |
| 085 | Level 3 - Real Infrastructure | Easy | 60 | Rotating KMS Customer Key | Complete the aws_kms_key resource | `085-harden-kms-rotation` |
| 086 | Level 3 - Real Infrastructure | Medium | 70 | Provision Lambda Function | Complete the aws_lambda_function resource | `086-provision-lambda-function` |
| 087 | Level 3 - Real Infrastructure | Medium | 70 | Provision SQS Queue | Complete the aws_sqs_queue resource | `087-provision-sqs-queue` |
| 088 | Level 3 - Real Infrastructure | Medium | 80 | Enable S3 Default Encryption | Complete the aws_s3_bucket_server_side_encryption_configuration resource | `088-harden-s3-encryption` |
| 089 | Level 3 - Real Infrastructure | Medium | 80 | Provision Cognito User Pool | Complete the aws_cognito_user_pool resource | `089-provision-cognito-user-pool` |
| 090 | Level 3 - Real Infrastructure | Medium | 80 | Provision DynamoDB Table | Complete the aws_dynamodb_table resource | `090-provision-dynamodb-table` |
| 091 | Level 3 - Real Infrastructure | Medium | 80 | Provision RDS PostgreSQL Instance | Complete the aws_db_instance resource | `091-provision-rds-instance` |
| 092 | Level 3 - Real Infrastructure | Medium | 80 | Provision Step Functions State Machine | Complete the aws_stepfunctions_state_machine resource | `092-provision-stepfunctions` |
| 093 | Level 3 - Real Infrastructure | Medium | 80 | Provision WAF Web ACL | Complete the aws_wafv2_web_acl resource | `093-provision-waf-web-acl` |
| 094 | Level 3 - Real Infrastructure | Medium | 80 | Two Containers on One Network | Complete the shared Docker network | `094-docker-multi-container` |
| 095 | Level 3 - Real Infrastructure | Medium | 85 | Secure a Secrets Manager Secret | Complete the aws_secretsmanager_secret resource | `095-harden-secretsmanager` |
| 096 | Level 3 - Real Infrastructure | Medium | 90 | Cap Lambda Timeout and Concurrency | Complete the aws_lambda_function resource | `096-harden-lambda-limits` |
| 097 | Level 3 - Real Infrastructure | Medium | 90 | Deny S3 Requests Without TLS | Complete the aws_s3_bucket_policy resource | `097-harden-s3-tls-policy` |
| 098 | Level 3 - Real Infrastructure | Medium | 90 | Enforce IMDSv2 on EC2 | Complete the aws_launch_template resource | `098-harden-ec2-imdsv2` |
| 099 | Level 3 - Real Infrastructure | Medium | 90 | Harden a DynamoDB Table | Complete the aws_dynamodb_table resource | `099-harden-dynamodb` |
| 100 | Level 3 - Real Infrastructure | Medium | 90 | Lock Down S3 Public Access | Complete the aws_s3_bucket_public_access_block resource | `100-harden-s3-public-access` |
| 101 | Level 3 - Real Infrastructure | Medium | 90 | Security Group Without Public SSH | Complete the aws_security_group resource | `101-harden-sg-no-ssh` |
| 102 | Level 3 - Real Infrastructure | Medium | 100 | Enable VPC Flow Logs | Complete the aws_flow_log resource | `102-harden-vpc-flow-logs` |
| 103 | Level 3 - Real Infrastructure | Medium | 100 | SQS Queue With Dead-Letter Queue | Complete the main queue | `103-harden-sqs-dlq` |
| 104 | Level 3 - Real Infrastructure | Medium | 100 | Versioning + Lifecycle Expiry | Complete the aws_s3_bucket_versioning resource | `104-harden-s3-versioning-lifecycle` |
| 105 | Level 4 - Composition | Medium | 95 | CPU Alarm to SNS | Complete the aws_cloudwatch_metric_alarm resource | `105-wire-cloudwatch-alarm-sns` |
| 106 | Level 4 - Composition | Medium | 100 | AWS Backup Vault + Plan | Complete the aws_backup_plan resource | `106-wire-backup-vault-plan` |
| 107 | Level 4 - Composition | Medium | 100 | Fan Out SNS to SQS | Complete the aws_sns_topic_subscription resource | `107-wire-sqs-sns` |
| 108 | Level 4 - Composition | Medium | 100 | IAM Role + Policy + Attachment | Complete the aws_iam_role_policy_attachment resource | `108-wire-iam-role-policy` |
| 109 | Level 4 - Composition | Medium | 110 | KMS Key + Alias + S3 Encryption | Complete the aws_s3_bucket_server_side_encryption_configuration resource | `109-wire-kms-s3` |
| 110 | Level 4 - Composition | Medium | 110 | RDS Instance in a Subnet Group | Complete the aws_db_instance resource | `110-wire-rds-subnet-group` |
| 111 | Level 4 - Composition | Hard | 120 | CloudFront HTTPS-Only Distribution | Complete the aws_cloudfront_distribution resource | `111-harden-cloudfront-https` |
| 112 | Level 4 - Composition | Medium | 120 | EC2 Instance + Security Group + EIP | Complete the aws_instance resource | `112-wire-ec2-sg-eip` |
| 113 | Level 4 - Composition | Hard | 120 | Encrypt S3 With a Customer KMS Key | Complete the aws_s3_bucket_server_side_encryption_configuration resource | `113-harden-s3-kms` |
| 114 | Level 4 - Composition | Hard | 120 | Least-Privilege IAM Policy | Complete the aws_iam_policy resource | `114-harden-iam-least-privilege` |
| 115 | Level 4 - Composition | Hard | 120 | Secrets Manager + RDS | Complete the aws_db_instance resource | `115-wire-secrets-rds` |
| 116 | Level 4 - Composition | Medium | 120 | Wire an ALB to a Target Group | Complete the aws_lb_listener resource | `116-wire-alb-target-listener` |
| 117 | Level 4 - Composition | Hard | 130 | ALB HTTPS Listener + Redirect | Complete the HTTPS listener | `117-harden-alb-https` |
| 118 | Level 4 - Composition | Hard | 130 | Harden an RDS Instance | Complete the aws_db_instance resource | `118-harden-rds` |
| 119 | Level 4 - Composition | Hard | 130 | Scheduled EventBridge to Lambda | Complete the scheduled function | `119-wire-eventbridge-lambda` |
| 120 | Level 4 - Composition | Medium | 140 | Build a Public VPC Foundation | Complete the aws_subnet resource | `120-wire-vpc-public-foundation` |
| 121 | Level 4 - Composition | Hard | 140 | Lambda Reading a DynamoDB Table | Complete the aws_lambda_function resource | `121-wire-lambda-dynamodb` |
| 122 | Level 4 - Composition | Hard | 150 | HTTP API Gateway to Lambda | Complete the aws_apigatewayv2_integration resource | `122-wire-apigw-lambda` |
| 123 | Level 4 - Composition | Hard | 150 | Route 53 + ACM + CloudFront | Complete the aws_cloudfront_distribution resource | `123-wire-route53-cloudfront-acm` |
| 124 | Level 4 - Composition | Hard | 160 | ECS Fargate Service Behind an ALB | Complete the aws_ecs_service resource | `124-wire-ecs-alb-service` |
| 125 | Level 5 - Modules & Capstones | Medium | 75 | Refactor With a moved Block | Complete the moved block | `125-refactor-moved-block` |
| 126 | Level 5 - Modules & Capstones | Medium | 75 | Workspace-Aware Naming | Complete the workspace-aware locals block | `126-state-workspaces` |
| 127 | Level 5 - Modules & Capstones | Medium | 80 | Call a Local Module | Complete the module call | `127-mod-local-module` |
| 128 | Level 5 - Modules & Capstones | Medium | 80 | Import Existing Resources | Complete the import block | `128-import-block` |
| 129 | Level 5 - Modules & Capstones | Medium | 90 | Remote State in S3 + DynamoDB | Complete the S3 backend configuration | `129-state-s3-backend` |
| 130 | Level 5 - Modules & Capstones | Easy | 100 | Docker Nginx Sandbox | Complete the Nginx container | `130-docker-nginx-sandbox` |
| 131 | Level 5 - Modules & Capstones | Hard | 100 | Module for_each | Complete the for_each module call | `131-mod-module-for-each` |
| 132 | Level 5 - Modules & Capstones | Easy | 100 | Secure S3 Bucket Provisioning | Complete the S3 bucket resource | `132-secure-s3-bucket` |
| 133 | Level 5 - Modules & Capstones | Medium | 150 | Highly Available VPC Foundation | Complete the public subnet definition | `133-ha-vpc-foundation` |
| 134 | Level 5 - Modules & Capstones | Hard | 250 | Auto Scaling Web Tier | Complete the Auto Scaling group | `134-autoscaling-web-tier` |
| 135 | Level 5 - Modules & Capstones | Hard | 300 | Serverless Item API | Complete the Lambda function | `135-serverless-item-api` |
