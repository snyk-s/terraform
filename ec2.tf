data "aws_iam_role" "iam_profile_role" {
  name = var.iam_role_name
}

# Deploy an EC2 instance 
resource "aws_instance" "demo-instance" {
  ami                    = var.aws_ami_image
  instance_type          = var.aws_instance_type
  iam_instance_profile   = data.aws_iam_role.iam_profile_role.name
  subnet_id              = "subnet-03447189cbe29523c"
  vpc_security_group_ids = ["sg-05548eb7a24d49ed8"]

  root_block_device {
    volume_type = "gp3"
    volume_size = 50
    encrypted   = true
  }
  key_name = var.t_key_name

  tags = {
    Name                 = "v_test_machine"
    backup_tier          = "none"
    "gfl:application-os" = "linux"
  }
}





