
provider "aws" {
  profile    = "default"
  region     = var.region
}

resource "aws_instance" "eg" {
  count         = var.epcount
  ami           = data.aws_ami.amazon-linux.id
  instance_type = "t2.micro"
  key_name      = var.pubkey
  #user_data     = var.userdata
}

output "ip" {
    value = aws_instance.eg[*].public_ip
}
