from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

# "profanity.dict" ファイルから有害な文章を読み込んでラベル付け
with open("/home/ussr/github4me/ndrr/data_set/profanity.dict", "r", encoding="utf-8") as f:
    profanity_sentences = [line.strip() for line in f.readlines()]
    profanity_labels = [1] * len(profanity_sentences)

# "non_profane.dict" ファイルから無害な文章を読み込んでラベル付け
with open("/home/ussr/github4me/ndrr/data_set/neutral.dict", "r", encoding="utf-8") as f:
    non_profanity_sentences = [line.strip() for line in f.readlines()]
    non_profanity_labels = [0] * len(non_profanity_sentences)

# 有害と無害のデータを結合してトレーニングデータを作成
all_sentences = profanity_sentences + non_profanity_sentences
all_labels = profanity_labels + non_profanity_labels

# 形態素解析と TF-IDF 特徴抽出
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(all_sentences)

# データをトレーニング用とテスト用に分割
X_train, X_test, y_train, y_test = train_test_split(X, all_labels, test_size=0.2, random_state=42)

# ロジスティック回帰モデルをトレーニング
model = LogisticRegression()
model.fit(X_train, y_train)

# テストデータでモデルの性能評価
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
