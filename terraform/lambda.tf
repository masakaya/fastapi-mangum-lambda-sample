resource "aws_lambda_function" "api" {
  function_name = var.project_name
  description   = "FastAPI + Mangum Lambda handler"

  runtime = "python3.12"
  handler = "src.main.handler"
  role    = aws_iam_role.lambda_exec.arn

  filename         = "${path.module}/placeholder.zip"
  source_code_hash = filebase64sha256("${path.module}/placeholder.zip")

  memory_size = var.lambda_memory_mb
  timeout     = var.lambda_timeout_sec

  environment {
    variables = {
      LOG_LEVEL = "INFO"
    }
  }

  depends_on = [aws_cloudwatch_log_group.lambda_logs]

  lifecycle {
    ignore_changes = [filename, source_code_hash]
  }
}

resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${var.project_name}"
  retention_in_days = 14

}
