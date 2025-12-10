# terraform/variables.tf

# Azure Authentication
# Uses Azure CLI authentication - run 'az login' before terraform commands
variable "subscription_id" {
  description = "Azure Subscription ID (run: az account show --query id -o tsv)"
  type        = string
}

# Project Configuration
variable "project_name" {
  description = "Name of the project (used for naming resources)"
  type        = string
  default     = "django-cloud"
}

variable "resource_group_name" {
  description = "Name of the Azure Resource Group"
  type        = string
  default     = "django-cloud-rg"
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "switzerlandnorth"  # Change to a region close to you
}

# VM Configuration
variable "vm_size" {
  description = "Size of the Virtual Machine"
  type        = string
  default     = "Standard_B1s"  # 1 vCPU, 1 GB RAM - good for learning
  # Other options:
  # - Standard_B1ms: 1 vCPU, 2 GB RAM
  # - Standard_B2s: 2 vCPU, 4 GB RAM
}

variable "admin_username" {
  description = "Admin username for the VM"
  type        = string
  default     = "azureuser"
}

variable "ssh_public_key" {
  description = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC1/igwpJR3IY61t7f4jDUzlrnTkLFB1QlBnNJaPgv5eroqSCQ+aUK+fBe/ocHOoxS5XuVi0eok0+G4KYKlgZ0jSqK6N6MZDt3NywRLzr3wIHOpY4wp+HUXI/jj3zWgAop/tu6vhlswDI0kCDJGyg27N3NyCI33aJetQch7cD9RqYbuRkXdlNAL+iZyn22lqRscQ/9zr5pYQzLO8LBNP1DAV3pP+cqYBfkIdWqsPUM8uQd5PpotYc03ZTQOtlWu1wcH2CJXJwW2GVdvc14tUAdQWHaHy1z1tR/cSwpIVBtMJF2u685KkR3ZpRrapzC+fMe4Gp67XKJRnRRk+nRb8UCbDzUp9EgXxS3/+2EJZSR/lQnOCWRKvYW7maQH8mfyQX7BwCKfmt3oW0SKeUdNqX3qrmUQvZj78b3r5WO0r32zA/AxXEskPtN+enSsoaRoOu52Jnnnn95PX6XL9grThFacR/vx6v4WxhgHzCWccbW5jsxUMVvKe9g9nQVZedKGuYc1jbYBWVMVf6J/yKwkGTlkVc7sP8lDOhPT2gSLgMETmiUFTswgTXt9Xv9qWwRgT48QsnQI0w5mJc8qw9GgSXJ7D2Ft3MWkgHQazB3dlPqwZfLKK+umFOPPOY+WrMT4NbecZSxXsl4T9VE36gN5WES/ztD4rxv7zL/z6E9jN9pX8w== lacrevette@lacrevette"
  type        = string
}

# Network Configuration
variable "ssh_source_address" {
  description = "IP address allowed to SSH into the VM (your IP)"
  type        = string
  default     = "*"  # WARNING: Open to all. Recommended: set to your specific IP
  # To find your IP: curl ifconfig.me
}
