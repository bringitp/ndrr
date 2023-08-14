#!/bin/bash

# 設定
DOMAIN="ron-the-rocker.net"
NGINX_CONFIG="/etc/nginx/sites-available/keycloak"
INSTALL_DIR="/root"
KEYCLOAK_DIR="${INSTALL_DIR}/keycloak"
KEYCLOAK_VERSION="22.0.1"

# NGINX設定ファイルの作成
echo "server {
    listen 80;
    server_name $DOMAIN;

    location /auth {
        proxy_pass http://localhost:8180/auth;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location / {
        return 301 http://\$host/auth;
    }
}" > "${NGINX_CONFIG}"

# NGINX再起動
systemctl restart nginx

# Keycloakのダウンロードと解凍
cd "${INSTALL_DIR}"
wget "https://github.com/keycloak/keycloak/releases/download/${KEYCLOAK_VERSION}/keycloak-${KEYCLOAK_VERSION}.zip"
unzip "keycloak-${KEYCLOAK_VERSION}.zip"
rm "keycloak-${KEYCLOAK_VERSION}.zip"

# クリーンアップ
cd "${INSTALL_DIR}"
rm -rf "${KEYCLOAK_DIR}"
