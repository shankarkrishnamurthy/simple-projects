module "my-regions-1" {
    source = "./shared"

    region = "us-west-1"
    epcount  = 1
    userdata = var.userdata
    listenid = module.accelerator.listenid
}

module "my-regions-2" {
    source = "./shared"

    region = "eu-west-3"
    epcount  = 1
    userdata = var.userdata
    listenid = module.accelerator.listenid
}

module "my-regions-3" {
    source = "./shared"

    region = "ap-southeast-1"
    epcount  = 1
    userdata = var.userdata
    listenid = module.accelerator.listenid
}


module "accelerator" {
    source = "./accl"
    region = "eu-west-1"
}

output "global-accelerator" {
    value = module.accelerator.dns-ip
}
