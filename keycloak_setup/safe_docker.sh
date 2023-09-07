#!/bin/bash

# バックアップディレクトリの作成
backup_dir="./custom_sql"

if [ "$1" == "start" ]; then
  # コンテナが起動していないことを確認して、コンテナを起動
  if [ "$(docker ps -q -f name=mysql)" ]; then
    echo "MySQLコンテナはすでに起動しています。"
  else
    echo "MySQLコンテナを起動します..."
    docker-compose up -d
  fi
elif [ "$1" == "stop" ]; then
  # データベースのバックアップを作成
  mysqldump -h 127.0.0.1 -P 3307 -u root -ppassword keycloak > "$backup_dir/keycloak.sql"
  mysqldump -h 127.0.0.1 -P 3307 -u root -ppassword ndrr > "$backup_dir/ndrr.sql"

  # Docker Composeを使用してコンテナを停止および削除
  docker-compose down -v
  # バックアップ完了メッセージを表示
  echo "データベースのバックアップが作成され、コンテナが停止および削除されました。"
else
  echo "無効な引数です。'start' または 'stop' を指定してください。"
  exit 1
fi
