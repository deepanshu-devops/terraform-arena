provider "aws" {
  region = var.aws_region
}

resource "aws_route53_zone" "this" {
  name = "example.com"
}

resource "aws_acm_certificate" "this" {
  domain_name       = "example.com"
  validation_method = "DNS"
}

resource "aws_cloudfront_distribution" "this" {
  # TODO - Complete the aws_cloudfront_distribution resource.
  # Add the arguments and nested blocks required for aws_cloudfront_distribution.
}

resource "aws_route53_record" "this" {
  name    = "www.example.com"
  type    = "A"
  zone_id = aws_route53_zone.this.zone_id
  alias {
    name    = aws_cloudfront_distribution.this.domain_name
    zone_id = aws_cloudfront_distribution.this.hosted_zone_id
  }
}
