import os
import subprocess

# 環境変数からデータベース接続文字列を取得
dbserver = os.environ.get("dbserver")

if not dbserver:
    print("Error: dbserver environment variable is not set.")
    exit(1)

# バックアップファイルの名前
backup_filename = "database_backup.sql"

# バックアップコマンドの生成
backup_command = [
    "mysqldump",
   # "--defaults-file=/path/to/my.cnf",  # MySQLの設定ファイルのパス
    "--databases",  # データベースを指定
    "ndrr",  # データベース名
    "--result-file=" + backup_filename  # バックアップファイルの名前を指定
]

# バックアップの実行
backup_process = subprocess.Popen(
    backup_command,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# バックアップ結果の取得
backup_output, backup_error = backup_process.communicate()

# バックアップファイルの書き込み
if backup_process.returncode == 0:
    with open(backup_filename, "wb") as backup_file:
        backup_file.write(backup_output)
        print("Backup saved as", backup_filename)
else:
    print("Backup failed. Error:", backup_error.decode("utf-8"))
