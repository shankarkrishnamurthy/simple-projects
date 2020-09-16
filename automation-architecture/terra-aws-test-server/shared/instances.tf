#
# Description: simple end-to-end terraform infra creation
#       with global accelerator
#
provider "aws" {
  profile    = "default"
  region     = var.region
}

resource "aws_instance" "aginst" {
  count         = var.epcount
  ami           = data.aws_ami.amazon-linux.id
  instance_type = "t2.micro"
  key_name      = "kp-ncal-ramanjaneyu"
  user_data     = var.userdata
}

resource "aws_eip" "ep" {
  count = var.epcount
  instance = element(aws_instance.aginst.*.id,count.index)
  vpc      = true
}

output "eip" {
    value = aws_eip.ep.*.id
}
