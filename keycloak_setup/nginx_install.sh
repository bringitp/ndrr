#!/bin/bash

# Install Nginx
sudo apt-get update
sudo apt-get install nginx -y

# Create a directory for the website
sudo mkdir -p /var/www/ron-the-rocker.net
echo "Hello, this is index.html" | sudo tee /var/www/ron-the-rocker.net/index.html

# Create a server block configuration
sudo tee /etc/nginx/sites-available/ron-the-rocker.net <<'EOF'
server {
    listen 80;
    server_name ron-the-rocker.net www.ron-the-rocker.net;

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name ron-the-rocker.net www.ron-the-rocker.net;

    ssl_certificate /etc/letsencrypt/live/ron-the-rocker.net/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ron-the-rocker.net/privkey.pem;

    location / {
        proxy_pass http://localhost:8180;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
    }

    location /ndrr {
        proxy_pass http://localhost:7777;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
    }
}
EOF
# Enable the server block
sudo ln -s /etc/nginx/sites-available/ron-the-rocker.net /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Start Nginx service
sudo systemctl start nginx

# Install Certbot
sudo apt-get install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d ron-the-rocker.net -d www.ron-the-rocker.net

echo "Nginx installed, configured, and SSL certificate obtained. Access https://ron-the-rocker.net/ to see the secure website."

