terraform {
  backend "s3" {
    bucket = "terraform-spontansolutions"
    key    = "aws-devops-cost-optimization-project/terraform.tfstate"
    region = "us-east-1"
  }
}
