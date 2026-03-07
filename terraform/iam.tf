# ==================================================
# Lambda Execution Role
# ==================================================

data "aws_iam_policy_document" "lambda_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_exec" {
  name               = "${local.prefix}-lambda-exec"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json

}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# ==================================================
# GitHub Actions OIDC
# ==================================================

# resource "aws_iam_openid_connect_provider" "github" {
#   url             = "https://token.actions.githubusercontent.com"
#   client_id_list  = ["sts.amazonaws.com"]
#   thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
# }

# data "aws_iam_policy_document" "github_oidc_assume" {
#   statement {
#     actions = ["sts:AssumeRoleWithWebIdentity"]
#     principals {
#       type        = "Federated"
#       identifiers = [aws_iam_openid_connect_provider.github.arn]
#     }
#     condition {
#       test     = "StringEquals"
#       variable = "token.actions.githubusercontent.com:aud"
#       values   = ["sts.amazonaws.com"]
#     }
#     condition {
#       test     = "StringLike"
#       variable = "token.actions.githubusercontent.com:sub"
#       values   = ["repo:masakaya/fastapi-mangum-lambda-sample:ref:refs/heads/main"]
#     }
#   }
# }

# resource "aws_iam_role" "github_actions" {
#   name               = "${local.prefix}-github-actions"
#   assume_role_policy = data.aws_iam_policy_document.github_oidc_assume.json

# }

# data "aws_iam_policy_document" "github_actions_deploy" {
#   statement {
#     sid    = "UpdateLambdaCode"
#     effect = "Allow"
#     actions = [
#       "lambda:UpdateFunctionCode",
#       "lambda:GetFunction",
#       "lambda:GetFunctionConfiguration",
#     ]
#     resources = [aws_lambda_function.api.arn]
#   }
#
#   statement {
#     sid    = "UpdateApiGateway"
#     effect = "Allow"
#     actions = [
#       "apigateway:PutRestApi",
#       "apigateway:CreateDeployment",
#     ]
#     resources = [
#       aws_api_gateway_rest_api.api.arn,
#       "${aws_api_gateway_rest_api.api.arn}/*",
#     ]
#   }
# }

# resource "aws_iam_role_policy" "github_actions_deploy" {
#   name   = "deploy-lambda"
#   role   = aws_iam_role.github_actions.id
#   policy = data.aws_iam_policy_document.github_actions_deploy.json
# }
