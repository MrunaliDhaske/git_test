terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region     = "us-east-1"
  access_key = "AKIAXJHD35N7H4K3EP67"
  secret_key = "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"
}

