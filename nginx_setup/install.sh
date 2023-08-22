#!/bin/bash

# Nginxの設定ファイルパス
NGINX_CONF_PATH="/etc/nginx/sites-available/my_custom_config"

# Nginxのリロードコマンド
NGINX_RELOAD_COMMAND="sudo nginx -s reload"

# サイトごとのリバースプロキシ設定
cat > $NGINX_CONF_PATH << EOF
server {
    listen 80;
    server_name ron-the-rocker.net;

    location /auth {
        proxy_pass http://localhost:8180;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /ndrr {
        proxy_pass http://localhost:7777;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # 他の設定オプションやSSL設定などを追加できます
}
EOF

# シンボリックリンクの作成
sudo ln -s $NGINX_CONF_PATH /etc/nginx/sites-enabled/

# Nginxの設定を再読み込み
$NGINX_RELOAD_COMMAND

echo "設定が適用されました。"
