variable "compartment_ocid" {
  description = "The OCID of the tenancy or compartment"
  type        = string
}

variable "subnet_ocid" {
  description = "The OCID of the regional public subnet"
  type        = string
}

variable "ssh_public_key" {
  description = "Public SSH key for instance access"
  type        = string
}
