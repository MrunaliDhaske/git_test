
resource "aws_s3_bucket" "bucket" {
  bucket = "forweatherdata8349"

}
# # main.tf

# DynamoDB Table
resource "aws_dynamodb_table" "weather" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "timestamp"
  attribute {
    name = "timestamp"
    type = "N"
  }
}





#data archive file
data "archive_file" "zip_the_python_code" {
  type        = "zip"
  source_dir  = "${path.module}/python/"
  output_path = "${path.module}/python/function.zip"
}


# Lambda Function
resource "aws_lambda_function" "weather_lambda" {
  function_name    = var.lambda_function_name
  runtime          = "python3.8"
  handler          = "function.lambda_handler"
  filename         = "${path.module}/python/function.zip" # Updated to use the correct path
  source_code_hash = filebase64("${path.module}/python/function.zip")
  role             = aws_iam_role.lambda_exec.arn
  #   environment = {
  #     variables = {
  #       weatherfc = aws_dynamodb_table.weather.arn,
  #       api_key   = var.api_key,
  #       city      = var.city,
  #     }
  #   }
}

# IAM Role for Lambda Execution
resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      }
    }
  ]
}
EOF
}
resource "aws_iam_policy" "lambda_policy" {
  name        = "lambda_policy"
  description = "policy for lambda function"
  policy      = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*",
            "Effect": "Allow"
        },
        {
            "Action": [
                "dynamodb:BatchGetItem",
                "dynamodb:GetItem",
                "dynamodb:Query",
                "dynamodb:Scan",
                "dynamodb:BatchWriteItem",
                "dynamodb:PutItem",
                "dynamodb:UpdateItem"
            ],
            "Resource": "${aws_dynamodb_table.weather.arn}",
            "Effect": "Allow"
        }
    ]
}
EOF
}


# Attach Policy to Role
resource "aws_iam_role_policy_attachment" "lambda_attach" {
  policy_arn = aws_iam_policy.lambda_policy.arn
  role       = aws_iam_role.lambda_exec.name
}
