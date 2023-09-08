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

    upstream backend {
        server 127.0.0.1:7777;  # バックエンドサーバーのポート
        server 127.0.0.1:7778;  # 追加のバックエンドサーバーのポート


        # さらに必要な数だけサーバーを追加
    }

  server {
    listen 443 ssl;
    server_name ron-the-rocker.net www.ron-the-rocker.net;

    ssl_certificate /etc/letsencrypt/live/ron-the-rocker.net/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ron-the-rocker.net/privkey.pem;
   
    location / {
        root /var/www/ron-the-rocker.net;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    location /auth {
        proxy_pass http://localhost:8180;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    location ~ ^/ndrr/api { 
       rewrite ^/ndrr/api(.*)?$ $1 break;

        add_header Access-Control-Allow-Origin http://localhost:3000;
        add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
        add_header Access-Control-Allow-Headers 'Origin, Content-Type, Accept, Authorization';

        if ($request_method = 'OPTIONS') {
            add_header Access-Control-Allow-Credentials 'true';
            add_header Access-Control-Max-Age 1728000;
            add_header Content-Type 'text/plain charset=UTF-8';
            add_header Content-Length 0;
            return 204;
        }

        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
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
            try_files $uri $uri/ /index.html;
        }

        location ~ ^/ndrr/api {
            rewrite ^/ndrr/api(.*)?$ $1 break;

            add_header Access-Control-Allow-Origin http://localhost:3000;
            add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
            add_header Access-Control-Allow-Headers 'Origin, Content-Type, Accept, Authorization';

            if ($request_method = 'OPTIONS') {
                add_header Access-Control-Allow-Credentials 'true';
                add_header Access-Control-Max-Age 1728000;
                add_header Content-Type 'text/plain charset=UTF-8';
                add_header Content-Length 0;
                return 204;
            }

            proxy_pass http://backend;  # upstreamで定義したバックエンドへのプロキシ
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

