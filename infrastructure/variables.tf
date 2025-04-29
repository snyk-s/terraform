
variable "aws_ami_image" {
  description = "The AWS AMI to use"
  type        = string
  default     = "ami-0a474b3a85d51a5e5"
}

variable "aws_region" {
  description = "The AWS region to deploy resources"
  type        = string
  default     = "ca-central-1"
}

variable "aws_instance_type" {
  description = "The AWS instance type to use"
  type        = string
  default     = "t2.small"
}

variable "iam_role_name" {
  default = "SSM_CW_Enabled"
}

variable "t_key_name" {
  default = "appops-kuma-ca1-v-key"
}
