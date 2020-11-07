variable "listenid" {
    type = string
}
resource "aws_globalaccelerator_endpoint_group" "gaepg" {
  listener_arn = var.listenid

    dynamic "endpoint_configuration" {
        for_each = toset(range(var.epcount))
        content {
            endpoint_id = aws_eip.ep[endpoint_configuration.key].id
            weight      = 100
        }
    }
}

