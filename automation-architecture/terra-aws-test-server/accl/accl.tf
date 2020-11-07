variable "region" {
    type = string
}
provider "aws" {
  profile    = "default"
  region     = var.region
}

resource "aws_globalaccelerator_accelerator" "aga" {
  name            = "Example"
  ip_address_type = "IPV4"
  enabled         = true
}

output "dns-ip" {
    value = {
      "dns" = aws_globalaccelerator_accelerator.aga.dns_name
      "ip"  = aws_globalaccelerator_accelerator.aga.ip_sets[*].ip_addresses
    }
}


resource "aws_globalaccelerator_listener" "galisten" {
  accelerator_arn = aws_globalaccelerator_accelerator.aga.id
  client_affinity = "SOURCE_IP"
  protocol        = "TCP"
  port_range {
    from_port = 80
    to_port   = 80
  }
}

output "listenid" {
    value = aws_globalaccelerator_listener.galisten.id
}
