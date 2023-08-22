#!/bin/bash

# Install Nginx
sudo apt-get update
sudo apt-get install nginx -y

# Create a directory for the website
sudo mkdir -p /var/www/ron-the-rocker.net
echo "<html lang="ja"><head><meta charset="utf-8"></meta></head>....hello ? 🐟</html>" | sudo tee /var/www/ron-the-rocker.net/index.html
echo "<html lang="ja"><head><meta charset="utf-8"></meta></head>🐟多分メンテ中</html>" | sudo tee /var/www/ron-the-rocker.net/maintenance.html

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
        root /var/www/ron-the-rocker.net;
        index index.html;
        try_files $uri $uri/ =404;
    }

    location /auth {
        proxy_pass http://localhost:8180;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }


#    location /ndrr {
#        proxy_pass http://localhost:7777;
#        proxy_set_header Host $host;
#        proxy_set_header X-Real-IP $remote_addr;
#        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#        proxy_set_header X-Forwarded-Proto $scheme;
#        proxy_set_header Upgrade $http_upgrade;
#        proxy_set_header Connection "Upgrade";
#    }

   location ~ ^/ndrr/rooms/.*/messages {
    rewrite ^/ndrr(.*) $1 break;
    proxy_pass http://localhost:7777;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "Upgrade";
  }

    location /maintenance.html {
        root /var/www/ron-the-rocker.net;
    }

    error_page 502 /maintenance.html;
    location = /maintenance.html {
        root /var/www/ron-the-rocker.net;
        internal;
    }

}

EOF

# Enable the server block
# Remove the existing symlink if it exists
if [ -L /etc/nginx/sites-enabled/ron-the-rocker.net ]; then
    sudo rm /etc/nginx/sites-enabled/ron-the-rocker.net
fi
sudo ln -s /etc/nginx/sites-available/ron-the-rocker.net /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Start Nginx service
sudo systemctl start nginx
sudo systemctl reload nginx

echo "Nginx installed, configured, and running."

