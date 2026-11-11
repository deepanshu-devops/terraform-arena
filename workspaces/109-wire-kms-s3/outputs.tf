output "key_arn" {
  value = aws_kms_key.this.arn
}

output "bucket_id" {
  value = aws_s3_bucket.this.id
}
