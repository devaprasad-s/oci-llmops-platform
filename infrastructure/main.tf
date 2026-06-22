terraform {
  required_providers {
    oci = {
      source = "oracle/oci"
    }
  }
}

provider "oci" {
  auth   = "InstancePrincipal"
  region = "us-ashburn-1"
}
resource "oci_core_instance" "jenkins_runner" {
  availability_domain = "rWgG:US-ASHBURN-AD-3"
  compartment_id      = var.compartment_ocid
  shape               = "VM.Standard.E2.1.Micro"
  display_name        = "jenkins-node"
  create_vnic_details {
    assign_public_ip = true
    subnet_id        = var.subnet_ocid
  }
  source_details {
    #Required
    source_id               = "ocid1.image.oc1.iad.aaaaaaaa5m2iw4g2glbqb2pzua2kyumj56j2zvzhusmbkqumcluf4oxh3dia"
    source_type             = "image"
    boot_volume_size_in_gbs = 50
  }
  extended_metadata = {
    ssh_authorized_keys = var.ssh_public_key
  }
}
resource "oci_core_instance" "ai_engine" {
  availability_domain = "rWgG:US-ASHBURN-AD-3"
  compartment_id      = var.compartment_ocid
  shape               = "VM.Standard.A1.Flex"
  display_name        = "ai-node"
  shape_config {
    ocpus         = 2
    memory_in_gbs = 12
  }
  create_vnic_details {
    assign_public_ip = true
    subnet_id        = var.subnet_ocid
  }
  source_details {
    #Required
    source_id               = "ocid1.image.oc1.iad.aaaaaaaaioyy7je3vndsccly24frkfptl5lggvyupubg74awcf2gmua7k3ra"
    source_type             = "image"
    boot_volume_size_in_gbs = 100
  }
  extended_metadata = {
    ssh_authorized_keys = var.ssh_public_key
  }
}
