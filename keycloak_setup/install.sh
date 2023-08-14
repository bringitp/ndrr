#!/bin/bash

# KeycloakのバージョンとURL
KEYCLOAK_VERSION="21.0.0"
KEYCLOAK_URL="https://github.com/keycloak/keycloak/releases/download/${KEYCLOAK_VERSION}/keycloak-${KEYCLOAK_VERSION}.zip"

# WildFlyのホームディレクトリ
WILDFLY_HOME="/path/to/your/wildfly/home"

# Keycloakのダウンロードと展開
curl -L -o "keycloak-${KEYCLOAK_VERSION}.zip" "${KEYCLOAK_URL}"
unzip -q "keycloak-${KEYCLOAK_VERSION}.zip"
rm "keycloak-${KEYCLOAK_VERSION}.zip"

# Keycloak Serverをコンテナとして起動
docker run --name keycloak -p 8180:8180 \
    -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin \
    quay.io/keycloak/keycloak:latest \
    start-dev --http-port 8180 --http-relative-path /auth --proxy=reencrypt  # --proxy=reencrypt に変更


# Keycloakが起動するまで待機
sleep 30

# Keycloakにユーザーとロールを作成
docker exec keycloak /opt/jboss/keycloak/bin/kcadm.sh config credentials --server http://localhost:8180/auth --realm master --user admin --password admin
docker exec keycloak /opt/jboss/keycloak/bin/kcadm.sh create roles -r master -s name=user
docker exec keycloak /opt/jboss/keycloak/bin/kcadm.sh create users -r master -s username=testuser -s enabled=true
docker exec keycloak /opt/jboss/keycloak/bin/kcadm.sh set-password -r master --username testuser --new-password testpassword
docker exec keycloak /opt/jboss/keycloak/bin/kcadm.sh add-roles -r master --uusername testuser --rolename user

# WildFlyにKeycloakのアダプターをインストール
unzip -q keycloak-${KEYCLOAK_VERSION}/adapters/keycloak-oidc/keycloak-wildfly-adapter-dist-${KEYCLOAK_VERSION}.zip -d ${WILDFLY_HOME}

# WildFlyを起動してKeycloakアダプターをインストール
${WILDFLY_HOME}/bin/standalone.sh &
sleep 20
${WILDFLY_HOME}/bin/jboss-cli.sh -c --file=${WILDFLY_HOME}/bin/adapter-install.cli
${WILDFLY_HOME}/bin/jboss-cli.sh -c --command=:reload

# keycloak.confファイルのフルパス（適切に変更してください）
KEYCLOAK_CONF_PATH="/path/to/your/keycloak.conf"

# keycloak.confファイルの特定の行をコメントアウト
sed -i 's/^proxy = reencrypt/# proxy = reencrypt/' "${KEYCLOAK_CONF_PATH}"

# ... 既存のコード ...

echo "Keycloak and WildFly setup completed."