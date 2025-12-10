# terraform/main.tf

# Configure the Azure Provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
  required_version = ">= 1.0"
}

# Configure the Microsoft Azure Provider
# Uses Azure CLI authentication - run 'az login' before terraform commands
provider "azurerm" {
  features {}
  
  # Uses Azure CLI authentication by default
  # No Service Principal needed - just run 'az login' first
  subscription_id = var.subscription_id
}

# Create a Resource Group
# A Resource Group is a container that holds related resources for an Azure solution
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location

  tags = {
    environment = "production"
    project     = var.project_name
  }
}

# Create a Public IP Address
# This gives your VM a public IP that users can access
resource "azurerm_public_ip" "main" {
  name                = "${var.project_name}-public-ip"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  allocation_method   = "Static"  # Static IP doesn't change on VM restart
  sku                 = "Standard"

  tags = {
    environment = "production"
    project     = var.project_name
  }
}

# Create a Network Security Group (NSG)
# NSG acts as a virtual firewall for your VM
resource "azurerm_network_security_group" "main" {
  name                = "${var.project_name}-nsg"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  # Allow SSH access (port 22) - restricted to your IP for security
  security_rule {
    name                       = "SSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = var.ssh_source_address  # Your IP address
    destination_address_prefix = "*"
  }

  # Allow HTTP access (port 80) - open to everyone
  security_rule {
    name                       = "HTTP"
    priority                   = 1002
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"  # Allow from anywhere
    destination_address_prefix = "*"
  }

  tags = {
    environment = "production"
    project     = var.project_name
  }
}

# Create a Network Interface
# This connects the VM to the network
resource "azurerm_network_interface" "main" {
  name                = "${var.project_name}-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.main.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.main.id
  }

  tags = {
    environment = "production"
    project     = var.project_name
  }
}

# Associate NSG with Network Interface
resource "azurerm_network_interface_security_group_association" "main" {
  network_interface_id      = azurerm_network_interface.main.id
  network_security_group_id = azurerm_network_security_group.main.id
}

# Create a Virtual Network (required even if we're keeping it simple)
resource "azurerm_virtual_network" "main" {
  name                = "${var.project_name}-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  tags = {
    environment = "production"
    project     = var.project_name
  }
}

# Create a Subnet within the Virtual Network
resource "azurerm_subnet" "main" {
  name                 = "${var.project_name}-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
}

# Create the Virtual Machine
resource "azurerm_linux_virtual_machine" "main" {
  name                = "${var.project_name}-vm"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  
  # VM Size - Standard_B1s is good for learning (low cost)
  # You can upgrade later if needed
  size                = var.vm_size
  
  # Admin username for SSH access
  admin_username      = var.admin_username
  
  # Network interface
  network_interface_ids = [
    azurerm_network_interface.main.id,
  ]

  # SSH key authentication (more secure than password)
  admin_ssh_key {
    username   = var.admin_username
    public_key = var.ssh_public_key
  }

  # OS Disk configuration
  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"  # Standard HDD (cheaper)
  }

  # Ubuntu 22.04 LTS image
  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts-gen2"
    version   = "latest"
  }

  # Custom data script to install Docker on first boot
  custom_data = base64encode(<<-EOF
    #!/bin/bash
    
    # Update system packages
    apt-get update
    apt-get upgrade -y
    
    # Install Docker
    apt-get install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
    
    # Start and enable Docker
    systemctl start docker
    systemctl enable docker
    
    # Add the admin user to the docker group
    usermod -aG docker ${var.admin_username}
    
    # Create app directory
    mkdir -p /home/${var.admin_username}/app
    chown ${var.admin_username}:${var.admin_username} /home/${var.admin_username}/app
    
    echo "Docker installation complete!"
  EOF
  )

  tags = {
    environment = "production"
    project     = var.project_name
  }
}
