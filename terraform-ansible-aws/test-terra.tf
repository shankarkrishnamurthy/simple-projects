
provider "aws" {
  profile    = "default"
  region     = var.region
}

resource "aws_instance" "eg" {
  count         = 1
  ami           = var.ami
  instance_type = "t2.micro"
  key_name      = var.pubkey
}

output "ip" {
    value = aws_instance.eg[*].public_ip
}
