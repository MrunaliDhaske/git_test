# variables.tf


variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}


# variables.tf

variable "table_name" {
  description = "Name of the DynamoDB table"
  type        = string
  default     = "weatherfc"
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "Weather_lambda"
}

variable "api_key" {
  description = "OpenWeatherMap API Key"
  type        = string
  default     = "1152748302afb1a2fbff5b475a6e9a08" # Replace with your OpenWeatherMap API key
}

variable "city" {
  description = "City for weather data"
  type        = string
  default     = "Mumbai"
}
