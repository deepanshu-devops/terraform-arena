output "bucket_id" {
  description = "Bucket id."
  value       = aws_s3_bucket.this.id
}

output "bucket_arn" {
  description = "Bucket ARN."
  value       = aws_s3_bucket.this.arn
}

output "bucket_region" {
  description = "Bucket region."
  value       = aws_s3_bucket.this.region
}
