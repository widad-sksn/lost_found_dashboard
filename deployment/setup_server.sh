#!/bin/bash
# setup_server.sh
# Script to prepare Ubuntu 24.04 for Odoo + Docker + CI/CD

echo "Updating system..."
sudo apt-update && sudo apt-upgrade -y

echo "Installing required packages (curl, git, ufw)..."
sudo apt-install -y curl git ufw apt-transport-https ca-certificates software-properties-common

echo "Installing Docker & Docker Compose..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-update
sudo apt-install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

echo "Enabling and starting Docker..."
sudo systemctl enable docker
sudo systemctl start docker

echo "Setting up UFW Firewall..."
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw --force enable

echo "Server setup complete. Please proceed to configure your .env file and run 'docker compose up -d'."
