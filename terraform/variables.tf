variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "ap-northeast-1"
}

variable "env" {
  description = "Environment name (e.g. dev, stg, prod)"
  type        = string
  default     = "dev"
}

variable "system_name" {
  description = "System name used for resource naming"
  type        = string
  default     = "fastapi-mangum-lambda"
}

variable "lambda_memory_mb" {
  description = "Lambda function memory in MB"
  type        = number
  default     = 512
}

variable "lambda_timeout_sec" {
  description = "Lambda function timeout in seconds"
  type        = number
  default     = 30
}

locals {
  prefix = "${var.env}-${var.system_name}"
}
