import subprocess
from config import TOKEN  # config.py ファイルからトークンをインポート

#url = "http://localhost:7777/room/1/messages"
url = "https://ron-the-rocker.net/ndrr/api/room/1/messages"
headers = {
    "Authorization": f"Bearer {TOKEN}"
}

# abコマンドを実行するためのコマンドラインを構築
ab_command = f"ab -n 1000 -c 10 -H 'Authorization: {headers['Authorization']}' {url}"

try:
    # abコマンドを実行し、結果を取得
    result = subprocess.check_output(ab_command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
    
    # 結果を出力
    print(result)
except subprocess.CalledProcessError as e:
    print("Error:", e.returncode)
    print("Error:", e.output)
