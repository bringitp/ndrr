import requests
from config import TOKEN  # config.py ファイルからトークンをインポート
#url = "http://localhost:7777/rooms/1/messages"
url = "https://ron-the-rocker.net/ndrr/api/rooms/1/messages"
headers = {
    "Authorization": f"Bearer {TOKEN}"
   ,"Content-Type": "application/json"
}
movie_dialogues = [
    "こんにちは。映画好きのあなた、最近どんな映画を観ましたか？",
    "映画って、人生のさまざまなエモーションを味わえる素晴らしい娯楽ですよね。",
    "死ね！！！"    
    "私は実は映画の中でのロマンチックなシーンが大好きなんです。",
    "夏の夜に観る映画って最高ですよね。特におすすめの作品はありますか？",
    "映画館の暗闇で映画を観るのは、まるで別世界にいるような気分になります。",
    "映画の音楽って、ストーリーに感情を盛り上げる魔法のような存在ですよね。",
    "映画にはいろんなジャンルがありますが、あなたはどんなジャンルが好きですか？",
    "映画って時間や空間を超えて人々の心を動かす力がありますよね。",
    "映画のキャッチフレーズって、作品の雰囲気を表す重要なポイントだと思います。",
    "夏の夜には、涼しさを感じる映画がピッタリですね。おすすめの涼感映画はありますか？",
    "映画の中で、特別な一瞬を追体験することができるって素敵だと思いませんか？",
    "夜の静寂な時間に、感動的な映画を観るのは心にぴったりですね。",
    "映画の中のドラマやアクション、笑いを共有するのは、楽しみが倍増しますね。",
    "映画は言葉や表情だけでなく、映像や音楽でも感情を伝えてくれます。",
    "夏の夜、友達と映画を観て過ごすのは最高のひとときですよね。",
    "映画のヒーローやヒロインたちは、私たちの憧れや希望を象徴しています。",
    "映画の中の風景や場面って、まるで旅行に行ったような気分にさせてくれます。",
    "映画のワンシーンや名台詞は、人々の記憶に残りやすいですよね。",
    "映画は何度でも繰り返し観ることができるからこそ、その魅力が広がりますね。",
    "映画の世界に引き込まれると、現実が忘れられる瞬間がありますよね。",
    "映画の中のキャラクターたちは、私たちに新たな視点や気づきを与えてくれますね。"
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
