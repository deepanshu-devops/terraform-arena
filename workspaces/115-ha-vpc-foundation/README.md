# 115 - Highly Available VPC Foundation

**Level:** Level 5 - Modules & Capstones  
**Difficulty:** Medium  
**Points:** 150  
**Tags:** aws, vpc, networking, count, for_each

## Scenario

Your platform team is standardising network foundations. Build a reusable VPC with two public subnets spread across distinct availability zones, an internet gateway, a public route table with a default route, and associations for every subnet. Everything must be parameterized so the same code can be reused per environment.

## What to complete

- File: `main.tf`
- Task: Complete the public subnet definition
- Create one subnet per CIDR, spread them across AZs, make them public and tag them.

## Constraints

- Provider: AWS (hashicorp/aws) with region from var.aws_region.
- vpc_cidr must default to 10.0.0.0/16 and be validated as a CIDR.
- Create exactly one aws_vpc with DNS support and DNS hostnames enabled.
- Create at least two aws_subnet resources across distinct AZs (use count/for_each, not copy-paste).
- Subnet CIDRs must be derived from variables (cidrsubnet or a CIDR list) — no magic literals.
- Public subnets must set map_public_ip_on_launch = true.
- Attach one internet gateway and one route table with a 0.0.0.0/0 default route to the gateway.
- Create a route table association for every public subnet.
- Tag VPC, subnets, gateway and route table with Project, Environment, ManagedBy = "terraform".
- Outputs: vpc_id, public_subnet_ids, internet_gateway_id.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `vpc_cidr` | `string` | `10.0.0.0/16` |
| `public_subnet_cidrs` | `list(string)` | `['10.0.1.0/24', '10.0.2.0/24']` |
| `availability_zones` | `list(string)` | `['us-east-1a', 'us-east-1b']` |
| `aws_region` | `string` | `us-east-1` |
| `project_name` | `string` | `terraform-practice` |
| `environment` | `string` | `dev` |

## Expected resources

- `aws_vpc`
- `aws_subnet`
- `aws_internet_gateway`
- `aws_route_table`
- `aws_route_table_association`

## Expected outputs

- `vpc_id`
- `public_subnet_ids`
- `internet_gateway_id`

## How to test

```powershell
python judge.py test 115 --dir workspaces/115-ha-vpc-foundation
```

> Hidden test details are only revealed after a submission.
