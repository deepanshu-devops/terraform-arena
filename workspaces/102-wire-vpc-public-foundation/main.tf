provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "this" {
  cidr_block = var.vpc_cidr
  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_subnet" "this" {
  # TODO - Complete the aws_subnet resource.
  # Add the arguments and nested blocks required for aws_subnet.
}

resource "aws_internet_gateway" "this" {
  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
  vpc_id = aws_vpc.this.id
}

resource "aws_route_table" "this" {
  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
  vpc_id = aws_vpc.this.id
}

resource "aws_route" "this" {
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.this.id
}

resource "aws_route_table_association" "this" {
  subnet_id      = aws_subnet.this.id
  route_table_id = aws_route_table.this.id
}
