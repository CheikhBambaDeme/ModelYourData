# terraform/terraform.tfvars
# ⚠️ WARNING: This file contains sensitive data. DO NOT commit to Git!

# AUTHENTICATION:
# This setup uses Azure CLI authentication (simpler, no Service Principal needed)
# Just run 'az login' before using terraform commands

# Azure Subscription ID (from Step 7.2)
# Get with: az account show --query id -o tsv
subscription_id = "0db29437-5803-4fb1-a6bd-6d8f217eb482"

# Project settings
project_name        = "django-cloud"
resource_group_name = "django-cloud-rg"
location            = "switzerlandnorth"  # Choose a region close to you

# VM settings
vm_size        = "Standard_B1s"
admin_username = "azureuser"

# Paste your public SSH key here (content of ~/.ssh/azure_vm_key.pub)
ssh_public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC1/igwpJR3IY61t7f4jDUzlrnTkLFB1QlBnNJaPgv5eroqSCQ+aUK+fBe/ocHOoxS5XuVi0eok0+G4KYKlgZ0jSqK6N6MZDt3NywRLzr3wIHOpY4wp+HUXI/jj3zWgAop/tu6vhlswDI0kCDJGyg27N3NyCI33aJetQch7cD9RqYbuRkXdlNAL+iZyn22lqRscQ/9zr5pYQzLO8LBNP1DAV3pP+cqYBfkIdWqsPUM8uQd5PpotYc03ZTQOtlWu1wcH2CJXJwW2GVdvc14tUAdQWHaHy1z1tR/cSwpIVBtMJF2u685KkR3ZpRrapzC+fMe4Gp67XKJRnRRk+nRb8UCbDzUp9EgXxS3/+2EJZSR/lQnOCWRKvYW7maQH8mfyQX7BwCKfmt3oW0SKeUdNqX3qrmUQvZj78b3r5WO0r32zA/AxXEskPtN+enSsoaRoOu52Jnnnn95PX6XL9grThFacR/vx6v4WxhgHzCWccbW5jsxUMVvKe9g9nQVZedKGuYc1jbYBWVMVf6J/yKwkGTlkVc7sP8lDOhPT2gSLgMETmiUFTswgTXt9Xv9qWwRgT48QsnQI0w5mJc8qw9GgSXJ7D2Ft3MWkgHQazB3dlPqwZfLKK+umFOPPOY+WrMT4NbecZSxXsl4T9VE36gN5WES/ztD4rxv7zL/z6E9jN9pX8w== lacrevette@lacrevette"

# Your IP address for SSH access (run: curl ifconfig.me)
# Use "*" to allow SSH from anywhere (less secure)
ssh_source_address = "*"
