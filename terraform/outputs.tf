output "resource_prefix" {
  description = "Resource prefix (set as RESOURCE_PREFIX in GitHub Actions)"
  value       = local.prefix
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.api.function_name
}

output "api_gateway_url" {
  description = "API Gateway invoke URL"
  value       = "${aws_api_gateway_stage.prod.invoke_url}/"
}

# output "github_actions_role_arn" {
#   description = "IAM role ARN for GitHub Actions OIDC (set as AWS_DEPLOY_ROLE_ARN secret)"
#   value       = aws_iam_role.github_actions.arn
# }
