import requests
from config import TOKEN  # config.py ファイルからトークンをインポート
#url = "http://localhost:7777/rooms/1/messages"
url = "https://ron-the-rocker.net/ndrr/api/rooms/1/messages"
headers = {
    "Authorization": f"Bearer {TOKEN}"
   ,"Content-Type": "application/json"
}
movie_dialogues = [
"映画はまるで魔法のようなもの。その画面に触れるたび、新たな世界が広がっていく。",
"映画の中で泣いたり笑ったりすることで、心がふっと軽くなる瞬間がある。",
"映画の世界に入ると、現実が遠く感じられ、想像力が解き放たれる。",
"映画館の暗闇が、新たな冒険への扉を開けてくれる。",
"映画は言葉だけでなく、視覚や音楽を通じて感情を奮い立たせてくれる。",
"映画の中では、遠くの場所や過去の時代にも旅することができる。",
"映画は、感動を分かち合う手段であり、心を結ぶ架け橋でもある。",
"映画の一場面が、人生に新たな輝きを与えてくれることがある。",
"映画は、喜怒哀楽のエモーションを、画面を通じて共有してくれる友達のような存在。",
"映画の世界での冒険が、現実の日常に鮮やかな色彩を添えてくれる。",
]

for dialogue in movie_dialogues:
    data = {
        "message_content": dialogue
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        print("Request failed with status code:", response.status_code)
        print("Error response:", response.text)
    else:
        try:
            response_json = response.json()
            print("Response:", response.status_code, response_json)
        except requests.exceptions.JSONDecodeError:
            print("Response does not contain valid JSON data.")
    
    # リアルな対話感を演出するために少し待機
