#!/bin/bash

# ドメイン名
DOMAIN="ron-the-rocker.net"

# Keycloakのディレクトリ
KEYCLOAK_DIR="/root/keycloak-18.0.0"

# Keycloakのバイナリディレクトリ
KEYCLOAK_BIN_DIR="$KEYCLOAK_DIR/bin"

# パスワード
KEYCLOAK_PASSWORD="your_admin_password"

# Certbotを使ってSSL証明書取得
sudo certbot certonly --standalone -d $DOMAIN

# Keycloakの設定ファイルを編集
sudo sed -i 's/<https-listener name="https".*\/>/<https-listener name="https" socket-binding="https" security-realm="ApplicationRealm"\/>/g' $KEYCLOAK_DIR/standalone/configuration/standalone.xml

# Keycloakサーバー再起動
$KEYCLOAK_BIN_DIR/standalone.sh -Djboss.socket.binding.port-offset=100 &

# 10秒待機（Keycloakが起動するまで）
sleep 10

# KeycloakのセキュリティレルムにSSL証明書情報を設定
$KEYCLOAK_BIN_DIR/kcadm.sh config credentials --server http://localhost:8280/auth --realm master --user admin --password $KEYCLOAK_PASSWORD
$KEYCLOAK_BIN_DIR/kcadm.sh update realms/master -s sslRequired=EXTERNAL

# Keycloakサーバー再起動
$KEYCLOAK_BIN_DIR/jboss-cli.sh --connect command=:shutdown

# リバースプロキシの設定などが必要です

echo "Keycloak setup completed."
