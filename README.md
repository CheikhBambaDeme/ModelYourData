# ModelYourData

A simple and friendly web tool that helps you make sense of your data without needing any complicated software.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![Azure](https://img.shields.io/badge/Cloud-Azure-0078D4)
![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC)
![Docker](https://img.shields.io/badge/Container-Docker-2496ED)

---

## Table of Contents

1. [Project Description](#project-description)
2. [Features](#features)
3. [Azure Resources](#azure-resources)
4. [Architecture](#architecture)
5. [Repository Structure](#repository-structure)
6. [Deployment Tutorial](#deployment-tutorial)
7. [Technologies Used](#technologies-used)

---

## Project Description

**ModelYourData** is a web application designed to help users explore and visualize their data effortlessly. Simply upload a CSV file and instantly get a clear preview of your dataset along with powerful tools to analyze it.

### What does it do?

- **Upload & Preview**: Upload any CSV file and instantly see your data in a clean, organized table
- **Visualizations**: Generate various types of charts and graphs with one click:
  - Distribution plots
  - Regression lines
  - Clustering results
  - Correlation heatmaps
- **Statistical Analysis**: View quick statistical summaries or run a full mini-EDA (Exploratory Data Analysis)
- **Export**: Download any visualization in various formats for reports, homework, or presentations

### Who is it for?

Whether you're a student working on a project, a researcher analyzing results, or just someone curious about their data, ModelYourData makes data exploration simple and accessible.

---

## Features

| Feature | Description |
|---------|-------------|
| **CSV Upload** | Drag-and-drop or click to upload your data files |
| **Multiple Visualizations** | Distribution plots, regression, clustering, heatmaps |
| **Statistical Summaries** | Quick stats and full EDA reports |
| **Export Options** | Download visualizations in multiple formats |
| **Responsive Design** | Clean green-and-white interface, works on mobile |
| **Real-time Updates** | Instant results without page reloads |

---

## Azure Resources

This project is deployed on Microsoft Azure using the following resources:

| Resource | Type | Purpose |
|----------|------|---------|
| **Resource Group** | `azurerm_resource_group` | Container for all Azure resources |
| **Virtual Machine** | `azurerm_linux_virtual_machine` | Ubuntu 22.04 LTS server hosting the Docker container |
| **Public IP** | `azurerm_public_ip` | Static IP address for public access |
| **Network Security Group** | `azurerm_network_security_group` | Firewall rules (SSH port 22, HTTP port 80) |
| **Virtual Network** | `azurerm_virtual_network` | Network infrastructure |
| **Subnet** | `azurerm_subnet` | Network subnet for the VM |
| **Network Interface** | `azurerm_network_interface` | Connects VM to the network |

### Architecture Diagram

```
                                    ┌─────────────────┐
                                    │     GitHub      │
                                    │   Repository    │
                                    └────────┬────────┘
                                             │
                                             │ git push
                                             ▼
                                    ┌─────────────────┐
                                    │  GitHub Actions │
                                    │    (CI/CD)      │
                                    └────────┬────────┘
                                             │
                        ┌────────────────────┴────────────────────┐
                        │                                         │
                        ▼                                         ▼
               ┌─────────────────┐                      ┌─────────────────┐
               │   Docker Hub    │                      │    Azure VM     │
               │  (Image Store)  │─────── pull ────────▶│   (Ubuntu)      │
               └─────────────────┘                      └────────┬────────┘
                                                                 │
                                                                 │
                                                        ┌────────▼────────┐
                                                        │ Docker Container│
                                                        │  ┌───────────┐  │
                                                        │  │ Gunicorn  │  │
                                                        │  │  Django   │  │
                                                        │  │  App      │  │
                                                        │  └───────────┘  │
                                                        └────────┬────────┘
                                                                 │
                                                                 │ HTTP (Port 80)
                                                                 ▼
                                                        ┌─────────────────┐
                                                        │   Public IP     │
                                                        │  (Static)       │
                                                        └────────┬────────┘
                                                                 │
                                                                 ▼
                                                               Users
```

---

## Architecture

### Deployment Architecture

| Layer | Technology | Description |
|-------|------------|-------------|
| **Infrastructure** | Terraform | Infrastructure as Code (IaC) |
| **Cloud Provider** | Microsoft Azure | IaaS - Virtual Machine |
| **Containerization** | Docker | Application containerization |
| **CI/CD** | GitHub Actions | Automated build and deployment |
| **Web Server** | Gunicorn | Production WSGI server |
| **Framework** | Django | Python web framework |
| **Image Registry** | Docker Hub | Container image storage |

### Request Flow

1. User accesses the website via the public IP address
2. Request hits the Azure VM on port 80
3. Docker container receives the request
4. Gunicorn handles the WSGI request
5. Django processes the request and returns the response

---

## Repository Structure

```
ModelYourData/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── run.sh                    # Production run script (Gunicorn)
├── run_dev.sh                # Development run script
├── README.md                 # This file
├── Dockerfile                # Docker image definition
├── docker-compose.yml        # Docker Compose configuration
├── entrypoint.sh             # Container startup script
├── .dockerignore             # Docker build exclusions
├── .gitignore                # Git exclusions
│
├── modelyourdata/            # Django project settings
│   ├── __init__.py
│   ├── settings.py           # Project configuration
│   ├── urls.py               # Root URL configuration
│   ├── wsgi.py               # WSGI entry point
│   └── asgi.py               # ASGI entry point
│
├── dataanalysis/             # Main application
│   ├── __init__.py
│   ├── admin.py              # Admin configuration
│   ├── apps.py               # App configuration
│   ├── forms.py              # Form definitions
│   ├── models.py             # Database models
│   ├── urls.py               # App URL patterns
│   ├── views.py              # View functions
│   └── utils/                # Utility modules
│       ├── __init__.py
│       └── analysis.py       # Data analysis functions
│
├── templates/                # HTML templates
│   ├── base.html             # Base template
│   └── dataanalysis/
│       ├── landing.html      # Landing page
│       ├── analysis.html     # Analysis page
│       └── error.html        # Error page
│
├── static/                   # Static files
│   ├── css/
│   │   ├── style.css         # Main stylesheet
│   │   └── analysis.css      # Analysis page styles
│   └── js/
│       ├── main.js           # Common utilities
│       ├── upload.js         # Upload functionality
│       └── analysis.js       # Analysis operations
│
├── media/                    # User uploaded files
│   ├── uploads/              # Uploaded CSV files
│   └── results/              # Generated visualizations
│
└── .github/
    └── workflows/
        └── deploy.yml        # CI/CD pipeline
```

---

## Deployment Tutorial

This tutorial explains how to reproduce the deployment from scratch.

> **Note**: The Terraform files are not included in the GitHub repository. They have been sent to you separately via email as a zip file for easier management. Extract the zip to a location of your choice on your machine.

### Prerequisites

Before starting, ensure you have:

- [ ] **Azure Account** with active subscription 
- [ ] **Docker Hub Account** for storing container images
- [ ] **GitHub Account** for repository and CI/CD
- [ ] **Local Tools Installed**:
  - Azure CLI (`az`)
  - Terraform (`terraform`)
  - Docker (`docker`)
  - Git (`git`)

### Step 1: Clone the Repository

```bash
git clone https://github.com/CheikhBambaDeme/ModelYourDataTest.git
cd ModelYourDataTest
```

### Step 2: Generate SSH Key Pair

```bash
# Generate SSH key for Azure VM access
ssh-keygen -t rsa -b 4096 -f ~/.ssh/azure_vm_key -N ""

# View your public key (you'll need this later)
cat ~/.ssh/azure_vm_key.pub
```

### Step 3: Login to Azure

```bash
# Login to Azure (opens browser)
az login

# Get your subscription ID
az account show --query id -o tsv
```

### Step 4: Configure Terraform

```bash
# Navigate to where you extracted the Terraform zip file
cd /path/to/your/terraform-folder

# Edit terraform.tfvars with your values
nano terraform.tfvars
```

**Required values in `terraform.tfvars`:**

```hcl
# Azure Subscription ID
subscription_id = "your-subscription-id"

# Project settings
project_name        = "modelyourdata"
resource_group_name = "modelyourdata-rg"
location            = "westeurope"

# VM settings
vm_size        = "Standard_B1s"
admin_username = "azureuser"

# Paste your SSH public key here
ssh_public_key = "ssh-rsa AAAA... your-key ...== user@host"

# Your IP for SSH access (or "*" for any)
ssh_source_address = "*"
```

### Step 5: Deploy Azure Infrastructure

```bash
# Initialize Terraform
terraform init

# Preview the resources to be created
terraform plan

# Create the resources
terraform apply
# Type 'yes' when prompted

# Note the outputs (especially public_ip_address)
terraform output
```

**Expected outputs:**
```
public_ip_address = "20.xxx.xxx.xxx"
ssh_command = "ssh -i ~/.ssh/azure_vm_key azureuser@20.xxx.xxx.xxx"
website_url = "http://20.xxx.xxx.xxx"
```

### Step 6: Update Django Settings

Add the VM's public IP address to the `ALLOWED_HOSTS` in your Django settings file:

```python
# modelyourdata/settings.py

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', "localhost,127.0.0.1,0.0.0.0,20.250.42.186,'THE-IP-OF-THE-VM '").split(',')

# Example:
# ALLOWED_HOSTS = ['20.xxx.xxx.xxx', 'localhost', '127.0.0.1']
```

Or use environment variables (recommended):
```python
import os

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

### Step 7: Docker Hub Image

This project uses the existing public Docker Hub image: `lacrevette/django-cloud`

No need to create your own repository. The image is already available and configured.

You can view the image at: [https://hub.docker.com/r/lacrevette/django-cloud](https://hub.docker.com/r/lacrevette/django-cloud)

### Step 8: GitHub Actions CI/CD

The CI/CD pipeline is already configured in the repository. You can view the workflow runs at:

[https://github.com/CheikhBambaDeme/ModelYourDataTest/actions](https://github.com/CheikhBambaDeme/ModelYourDataTest/actions)

The pipeline automatically builds and deploys when changes are pushed to the main branch.

### Step 9: Configure GitHub Secrets

Go to the GitHub repository → **Settings** → **Secrets and variables** → **Actions**

Update these two secrets with your new VM information:

| Secret Name | Value |
|-------------|-------|
| `VM_HOST` | Public IP from Terraform output (Step 5) |
| `VM_SSH_PRIVATE_KEY` | Content of `~/.ssh/azure_vm_key` (your private key) |

To get your private key content:
```bash
cat ~/.ssh/azure_vm_key
```

Copy the entire output including `-----BEGIN OPENSSH PRIVATE KEY-----` and `-----END OPENSSH PRIVATE KEY-----` lines.

### Step 10: GitHub Actions Workflow

The workflow file `.github/workflows/deploy.yml` is already configured. No changes needed.

It is set to use the Docker image: `lacrevette/django-cloud`

### Step 11: Deploy!

```bash
# Commit and push your changes
git add .
git commit -m "Configure deployment"
git push origin main
```

This triggers the GitHub Actions workflow which:
1. Builds the Docker image
2. Pushes it to Docker Hub
3. SSHs into the Azure VM
4. Pulls and runs the new container

### Step 12: Verify Deployment

```bash
# Check GitHub Actions (should show green checkmarks)
# Go to: https://github.com/CheikhBambaDeme/ModelYourDataTest/actions

# Access your website
curl http://YOUR_VM_PUBLIC_IP

# Or open in browser
# http://YOUR_VM_PUBLIC_IP
```

---

## Technologies Used

| Category | Technology |
|----------|------------|
| **Backend** | Python 3.11, Django 4.2 |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Data Analysis** | Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn |
| **Web Server** | Gunicorn |
| **Containerization** | Docker |
| **Cloud** | Microsoft Azure (IaaS) |
| **IaC** | Terraform |
| **CI/CD** | GitHub Actions |
| **Image Registry** | Docker Hub |

---

## Notes

- This project uses **SQLite** as the database for simplicity
- The website runs on **HTTP** (no SSL/HTTPS)
- No custom domain is configured (uses Azure public IP)
- The VM size `Standard_B1s` is cost-effective for learning (~$10/month)

---

## Cleanup

To avoid ongoing charges, destroy the Azure resources when done:

```bash
# Navigate to where you extracted the Terraform zip file
cd /path/to/your/terraform-folder
terraform destroy
# Type 'yes' when prompted
```

---

## Authors

School Project - Cloud Computing Assignment
DEME Cheikh
CODO Loth
AKLAMAVO Uriel
AMADOU Raliatou
LONTSIE TSAGUE Cassidy


---

## License

This project is for educational purposes.
