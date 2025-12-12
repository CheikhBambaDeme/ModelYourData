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
├── terraform/                # Infrastructure as Code
│   ├── main.tf               # Main Terraform configuration
│   ├── variables.tf          # Variable definitions
│   ├── outputs.tf            # Output definitions
│   └── terraform.tfvars      # Variable values (not committed)
│
└── .github/
    └── workflows/
        └── deploy.yml        # CI/CD pipeline
```

---

## Deployment Tutorial

This tutorial explains how to reproduce the deployment from scratch.

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
git clone https://github.com/YOUR_USERNAME/ModelYourData.git
cd ModelYourData
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
cd terraform

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

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', "localhost,127.0.0.1,0.0.0.0,20.250.42.186,'THE-IP-OF-THE-VM    '").split(',')

# Example:
# ALLOWED_HOSTS = ['20.xxx.xxx.xxx', 'localhost', '127.0.0.1']
```

Or use environment variables (recommended):
```python
import os

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
```

### Step 7: Create Docker Hub Repository

1. Go to [Docker Hub](https://hub.docker.com/)
2. Click **Create Repository**
3. Name it `modelyourdata`
4. Set visibility to **Public**

> **Alternative**: You can skip Steps 7-9 and use the existing public image `lacrevette/django-cloud` (lacrevette is my user name(Cheikh DEME)) instead of building your own. WE RECOMMAND THIS !!!

### Step 8: Create Docker Hub Access Token

1. Go to Docker Hub → **Account Settings** → **Security**
2. Click **New Access Token**
3. Name it "GitHub Actions"
4. Copy the token (shown only once!)

### Step 9: Configure GitHub Secrets

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**

Add these secrets:

| Secret Name | Value |
|-------------|-------|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | Access token from Step 8 |
| `VM_HOST` | Public IP from Terraform output |
| `VM_USERNAME` | `azureuser` |
| `VM_SSH_PRIVATE_KEY` | Content of `~/.ssh/azure_vm_key` |
| `DJANGO_SECRET_KEY` | Generate with: `openssl rand -base64 50` |

### Step 10: Update GitHub Actions Workflow

In `.github/workflows/deploy.yml`, update the Docker image name:

```yaml
env:
  DOCKER_IMAGE: lacrevette/django-cloud
```

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
# Go to: https://github.com/YOUR_USERNAME/ModelYourData/actions

# Access your website
curl http://YOUR_VM_PUBLIC_IP

# Or open in browser
# http://YOUR_VM_PUBLIC_IP
```

### Step 13: (Optional) SSH into VM for Debugging

```bash
# Connect to VM
ssh -i ~/.ssh/azure_vm_key azureuser@YOUR_VM_PUBLIC_IP

# Check container status
docker ps

# View container logs
docker logs django_app
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
cd terraform
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
