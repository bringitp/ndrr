from textblob import TextBlob

def calculate_sentiment_score(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def judge_good_or_evil(score):
    if score >= 0.2:
        return "良い会話"
    elif score <= -0.2:
        return "悪い会話"
    else:
        return "普通の会話"

movie_dialogues = [
    "こんにちは。映画好きのあなた、最近どんな映画を観ましたか？",
    "映画って、人生のさまざまなエモーションを味わえる素晴らしい娯楽ですよね。",
    # 他の映画の会話も続く...
]

evil_dialogues = [
    "こんばんは！夏の夜、何をしていますか？ ちょっと退屈そうなんですけど。私と話すのが面白くなるか心配ですね。",
    "夜風が気持ちいいですね。あなたはどんな風に夏を楽しんでいますか？ まさか、ただ寝ているだけですか？もっと面白いことしてるのかしら？",
    # 他の悪い会話も続く...
]

print("映画の会話:")
for dialogue in movie_dialogues:
    score = calculate_sentiment_score(dialogue)
    judgment = judge_good_or_evil(score)
    print(f"スコア: {score:.2f}, 判定: {judgment}")

print("\n悪い会話:")
for dialogue in evil_dialogues:
    score = calculate_sentiment_score(dialogue)
    judgment = judge_good_or_evil(score)
    print(f"スコア: {score:.2f}, 判定: {judgment}")