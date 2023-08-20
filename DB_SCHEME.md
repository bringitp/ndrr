## テーブル名はMySQLに準拠するために小文字で統一することとする。  

```sql

-- users テーブル
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    sub VARCHAR(100) UNIQUE NOT NULL,
    avatar VARCHAR(100),
    trip VARCHAR(32) NOT NULL,
    karma INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    lastlogin_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    lastlogout_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    privilege ENUM('user', 'premium') NOT NULL DEFAULT 'user',
    ng_list TEXT
);

-- user_sessions テーブル
CREATE TABLE user_sessions (
    session_id VARCHAR(64) PRIMARY KEY,
    user_id INT NOT NULL,
    access_token VARCHAR(128) NOT NULL,
    refresh_token VARCHAR(128) NOT NULL,
    expiration_date TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- rooms テーブル
CREATE TABLE rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    owner_id INT NOT NULL,
    max_capacity INT NOT NULL DEFAULT 20,
    status ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
    last_activity TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- room_members テーブル
CREATE TABLE room_members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    user_id INT NOT NULL,
    joined_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- messages テーブル
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    sender_id INT NOT NULL,
    content TEXT NOT NULL,
    toxicity INT NOT NULL,
    sent_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms(id),
    FOREIGN KEY (sender_id) REFERENCES users(id)
);

-- blocked_users テーブル
CREATE TABLE blocked_users (
    block_id INT AUTO_INCREMENT PRIMARY KEY,
    blocking_user_id INT NOT NULL,
    blocked_user_id INT NOT NULL,
    FOREIGN KEY (blocking_user_id) REFERENCES users(id),
    FOREIGN KEY (blocked_user_id) REFERENCES users(id)
);

-- images テーブル
CREATE TABLE images (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    sender_id INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms(id),
    FOREIGN KEY (sender_id) REFERENCES users(id)
);

-- spam_users テーブル
CREATE TABLE spam_users (
    spam_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    spam_points INT NOT NULL,
    last_spam_activity TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- banned_users テーブル
CREATE TABLE banned_users (
    ban_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    ban_start_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ban_end_date TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- spam_messages テーブル
CREATE TABLE spam_messages (
    spam_message_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    spam_type INT NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

```


```sql
-- ダミーデータ
-- users テーブルのダミーデータ
INSERT INTO users (username, sub, avatar, trip, karma, created_at, lastlogin_at, lastlogout_at, privilege, ng_list)
VALUES
    ('user1', 'sub1', 'avatar1.jpg', 'trip1', 100, '2023-08-21 12:00:00', '2023-08-21 12:00:00', '2023-08-21 12:00:00', 'user', NULL),
    ('user2', 'sub2', 'avatar2.jpg', 'trip2', 150, '2023-08-21 13:00:00', '2023-08-21 13:00:00', '2023-08-21 13:00:00', 'user', NULL),
    ('user3', 'sub3', 'avatar3.jpg', 'trip3', 200, '2023-08-21 14:00:00', '2023-08-21 14:00:00', '2023-08-21 14:00:00', 'user', NULL),
    ('user4', 'sub4', 'avatar4.jpg', 'trip4', 50, '2023-08-21 15:00:00', '2023-08-21 15:00:00', '2023-08-21 15:00:00', 'user', NULL),
    ('premiumuser1', 'sub5', 'avatar5.jpg', 'trip5', 300, '2023-08-21 16:00:00', '2023-08-21 16:00:00', '2023-08-21 16:00:00', 'premium', NULL),
    ('premiumuser2', 'sub6', 'avatar6.jpg', 'trip6', 500, '2023-08-21 17:00:00', '2023-08-21 17:00:00', '2023-08-21 17:00:00', 'premium', NULL),
    ('user5', 'sub7', 'avatar7.jpg', 'trip7', 120, '2023-08-21 18:00:00', '2023-08-21 18:00:00', '2023-08-21 18:00:00', 'user', NULL),
    ('premiumuser3', 'sub8', 'avatar8.jpg', 'trip8', 250, '2023-08-21 19:00:00', '2023-08-21 19:00:00', '2023-08-21 19:00:00', 'premium', NULL),
    ('user6', 'sub9', 'avatar9.jpg', 'trip9', 80, '2023-08-21 20:00:00', '2023-08-21 20:00:00', '2023-08-21 20:00:00', 'user', NULL),
    ('user7', 'sub10', 'avatar10.jpg', 'trip10', 70, '2023-08-21 21:00:00', '2023-08-21 21:00:00', '2023-08-21 21:00:00', 'user', NULL);


-- user_sessions テーブルのダミーデータ
INSERT INTO user_sessions (session_id, user_id, access_token, refresh_token, expiration_date)
VALUES
    ('session_id1', 1, 'access_token1', 'refresh_token1', '2023-12-31 23:59:59'),
    ('session_id2', 2, 'access_token2', 'refresh_token2', '2023-12-31 23:59:59'),
    ('session_id3', 3, 'access_token3', 'refresh_token3', '2023-12-31 23:59:59'),
    ('session_id4', 4, 'access_token4', 'refresh_token4', '2023-12-31 23:59:59'),
    ('session_id5', 5, 'access_token5', 'refresh_token5', '2023-12-31 23:59:59'),
    ('session_id6', 6, 'access_token6', 'refresh_token6', '2023-12-31 23:59:59'),
    ('session_id7', 7, 'access_token7', 'refresh_token7', '2023-12-31 23:59:59'),
    ('session_id8', 8, 'access_token8', 'refresh_token8', '2023-12-31 23:59:59'),
    ('session_id9', 9, 'access_token9', 'refresh_token9', '2023-12-31 23:59:59'),
    ('session_id10', 10, 'access_token10', 'refresh_token10', '2023-12-31 23:59:59');

-- rooms テーブルのダミーデータ
INSERT INTO rooms (name, owner_id, max_capacity, status)
VALUES
    ('Room 1', 1, 10, 'active'),
    ('Room 2', 2, 15, 'inactive'),
    ('Room 3', 3, 20, 'active'),
    ('Room 4', 4, 10, 'active'),
    ('Room 5', 5, 10, 'inactive'),
    ('Room 6', 6, 20, 'active'),
    ('Room 7', 7, 15, 'active'),
    ('Room 8', 8, 15, 'inactive'),
    ('Room 9', 9, 20, 'active'),
    ('Room 10', 10, 10, 'active');

-- room_members テーブルのダミーデータ
INSERT INTO room_members (room_id, user_id)
VALUES
    (1, 1),
    (1, 2),
    (2, 2),
    (3, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (6, 7),
    (6, 8),
    (7, 9);

-- messages テーブルのダミーデータ（50件）
INSERT INTO messages (room_id, sender_id, content, toxicity)
VALUES
    (1, 1, 'こんにちは！', 0),
    (1, 2, '今日の天気はいいですね。', 0),
    (1, 3, 'こんにちは！', 0),
    (2, 4, 'どうしたんですか？', 0),
    (2, 5, '元気ですか？', 0),
    (2, 1, 'こんばんは！', 0),
    (3, 2, '新しい映画が公開されましたね。', 0),
    (3, 3, '行ってみたいです。', 0),
    (3, 4, '楽しみですね！', 0),
    (4, 5, '今日は何をして過ごしましたか？', 0),
    (4, 1, '私は友達とカフェに行ってきました。', 0),
    (5, 2, 'おはようございます！', 0),
    (5, 3, 'おはよう！', 0),
    (5, 4, '朝ごはんは何を食べましたか？', 0),
    (6, 5, 'こんにちは！', 0),
    (6, 1, '仕事が忙しいです。', 0),
    (7, 2, '今週末の予定はありますか？', 0),
    (7, 3, '友達と遊びに行く予定です。', 0),
    (8, 4, 'おめでとう！', 0),
    (8, 5, 'どうしたの？', 0),
    (9, 1, '楽しかったですか？', 0),
    (9, 2, 'はい、楽しかったです！', 0),
    (10, 3, '天気がいいので外に出たいです。', 0),
    (10, 4, '私もそう思います。', 0),
    (11, 5, '何か新しいことを始めたいです。', 0),
    (11, 1, '新しい趣味を見つけるのもいいですね。', 0),
    (12, 2, '今日は何を食べたいですか？', 0),
    (12, 3, 'ピザが食べたいです！', 0),
    (13, 4, 'おやつにアイスクリームが食べたいな。', 0),
    (13, 5, '私もアイスクリームが好きです！', 0),
    (14, 1, '昨日のサッカーの試合面白かったですね。', 0),
    (14, 2, 'まさに！', 0),
    (15, 3, '今週末の天気予報はどうですか？', 0),
    (15, 4, '晴れるみたいですよ。', 0),
    (16, 5, 'どこか旅行に行きたいです。', 0),
    (16, 1, '海に行くのもいいですね。', 0),
    (17, 2, '新しいゲームが発売されたようです。', 0),
    (17, 3, '早速プレイしたいです！', 0),
    (18, 4, '今週末の予定を考えていますか？', 0),
    (18, 5, '友達と映画を見に行く予定です。', 0),
    (19, 1, '最近どんな本を読んでいますか？', 0),
    (19, 2, 'ミステリー小説を読んでいます。', 0),
    (20, 3, 'おはようございます！', 0),
    (20, 4, 'おはよう！', 0),
    (21, 5, 'こんにちは！', 0),
    (21, 1, 'こんにちは！', 0),
    (22, 2, '元気ですか？', 0),
    (22, 3, 'お疲れ様です。', 0),
    (23, 4, '今週末の予定はありますか？', 0),
    (23, 5, '友達と遊びに行く予定です。', 0),
    (24, 1, 'どうしたの？', 0),
    (24, 2, '特に何もないです。', 0);

-- blocked_users テーブルのダミーデータ
INSERT INTO blocked_users (blocking_user_id, blocked_user_id)
VALUES
    (1, 2),
    (2, 1),
    (3, 4),
    (4, 3),
    (5, 6),
    (6, 5),
    (7, 8),
    (8, 7),
    (9, 10),
    (10, 9);

-- images テーブルのダミーデータ
INSERT INTO images (room_id, sender_id, image_url)
VALUES
    (1, 1, 'image1.jpg'),
    (1, 2, 'image2.jpg'),
    (2, 3, 'image3.jpg'),
    (3, 4, 'image4.jpg'),
    (4, 5, 'image5.jpg'),
    (5, 6, 'image6.jpg'),
    (6, 7, 'image7.jpg'),
    (7, 8, 'image8.jpg'),
    (8, 9, 'image9.jpg'),
    (9, 10, 'image10.jpg');

-- spam_users テーブルのダミーデータ
INSERT INTO spam_users (user_id, spam_points)
VALUES
    (1, 5),
    (2, 2),
    (3, 10),
    (4, 3),
    (5, 7),
    (6, 1),
    (7, 8),
    (8, 6),
    (9, 4),
    (10, 9);

-- banned_users テーブルのダミーデータ
INSERT INTO banned_users (user_id, ban_end_date)
VALUES
    (3, '2023-08-31 23:59:59'),
    (7, '2023-09-15 23:59:59'),
    (10, '2023-08-25 23:59:59'),
    (2, '2023-09-01 23:59:59'),
    (5, '2023-08-28 23:59:59'),
    (8, '2023-08-30 23:59:59'),
    (4, '2023-09-05 23:59:59'),
    (9, '2023-09-10 23:59:59'),
    (6, '2023-09-20 23:59:59'),
    (1, '2023-08-23 23:59:59');

-- spam_messages テーブルのダミーデータ
INSERT INTO spam_messages (user_id, spam_type, message)
VALUES
    (1, 1, '今すぐクリックしてお得な情報をゲット！'),
    (3, 1, '無料でiPhoneを手に入れるチャンス！'),
    (5, 1, 'すごい割引セール中！見逃すな！'),
    (7, 1, 'お金を稼ぐ方法を教えます。'),
    (8, 2, '今週末のイベントお見逃しなく！'),
    (9, 1, 'あなたの口座情報が漏れています！'),
    (10, 2, '新商品の情報をお届けします。'),
    (1, 1, '豪華なプレゼントが当たるキャンペーン！'),
    (2, 2, '電話をかけてください。'),
    (3, 1, '今すぐ登録して特典をゲット！'),
    (5, 1, '夢のような旅行を格安で実現！'),
    (7, 1, '簡単に稼ぐ方法を伝授します。'),
    (8, 2, '最新のニュースをチェックしよう。'),
    (9, 1, 'あなたの個人情報が漏れています！'),
    (10, 2, '新メニューのお知らせです。'),
    (1, 1, '今すぐサインアップして豪華な特典をGET！'),
    (3, 1, '無料でギフトカードをゲットしよう！'),
    (5, 1, '限定セールがスタートしました！'),
    (7, 1, '驚きの副業がこちら！'),
    (9, 1, 'あなたのアカウントがハッキングされました！'),
    (10, 2, '新商品の詳細をチェックしよう。'),
    (1, 1, '特別なキャンペーンで豪華なプレゼントをGET！'),
    (3, 1, '今すぐ参加して大金をゲット！'),
    (5, 1, 'お得な情報を逃すな！'),
    (7, 1, '簡単に稼げる方法をご紹介！'),
    (8, 2, '週末の天気予報をチェックしよう。'),
    (9, 1, 'あなたのパスワードが漏洩しました！'),
    (10, 2, '新商品のお知らせです。'),
    (1, 1, '今すぐ登録してお得な特典をゲットしよう！'),
    (2, 2, 'おはようございます。'),
    (3, 1, '無料で豪華な商品をプレゼント！'),
    (5, 1, '割引セールを見逃すな！'),
    (6, 2, 'こんにちは！'),
    (8, 2, '週末の予定を考えていますか？'),
    (9, 1, 'あなたの個人情報が流出しました！');


```

#### 0. ユーザ認証基盤 (15点)

**users テーブル**
| カラム名         | データ型       | 制約                                 | 説明                                      |
|----------------|--------------|-------------------------------------|-----------------------------------------|
| id             | INT          | PRIMARY KEY, AUTO_INCREMENT         | ユーザーID                                |
| username       | VARCHAR(50)  | UNIQUE, NOT NULL                    | ユーザー名（ユニークで、50文字以下）           |
| password_hash  | VARCHAR(128) | NOT NULL                            | パスワードハッシュ                          |
| email          | VARCHAR(100) | UNIQUE, NOT NULL                    | メールアドレス                             |
| avatar         | VARCHAR(100) |                                     | アバター画像のファイルパス                     |
| trip           | VARCHAR(32)  | NOT NULL                            | トリップ（ユーザー識別のための文字列）            |
| privilege      | ENUM         | NOT NULL, DEFAULT 'user'            | 特権レベル（'user', 'premium', など）         |
| ng_list        | TEXT         |                                     | 個別チャットの相手のNGリスト                   |

**user_sessions**
| カラム名         | データ型       | 制約                                 | 説明                                      |
|----------------|--------------|-------------------------------------|-----------------------------------------|
| session_id     | VARCHAR(64)  | PRIMARY KEY                         | セッションID                               |
| user_id        | INT          | NOT NULL                            | ユーザーID                                |
| access_token   | VARCHAR(128) | NOT NULL                            | アクセストークン                           |
| refresh_token  | VARCHAR(128) | NOT NULL                            | リフレッシュトークン                         |
| expiration_date| TIMESTAMP    | NOT NULL                            | 有効期限のタイムスタンプ                         |

#### 1. ユーザ認証とアカウント管理 (30点)

(既存のテーブルを使用)

#### 2. 固定部屋機能 (5点)

**rooms テーブル**
| カラム名        | データ型       | 制約                                 | 説明                                      |
|---------------|--------------|-------------------------------------|-----------------------------------------|
| id            | INT          | PRIMARY KEY, AUTO_INCREMENT         | 部屋ID                                    |
| name          | VARCHAR(50)  | NOT NULL                            | 部屋名（50文字以下）                        |
| owner_id      | INT          | NOT NULL                            | 部屋主のユーザーID                           |
| max_capacity  | INT          | NOT NULL, DEFAULT 20                | 部屋の最大人数（デフォルト20人）                 |
| status        | ENUM         | NOT NULL, DEFAULT 'active'          | 部屋の状態（'active', 'inactive' など）        |
| last_activity| TIMESTAMP    | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 最終アクティビティのタイムスタンプ               |

**room_members テーブル**
| カラム名        | データ型       | 制約                                 | 説明                                      |
|---------------|--------------|-------------------------------------|-----------------------------------------|
| member_id     | INT          | PRIMARY KEY, AUTO_INCREMENT         | メンバーID                                |
| room_id       | INT          | NOT NULL                            | 関連する部屋ID                              |
| user_id       | INT          | NOT NULL                            | ユーザーID                                 |
| joined_at     | TIMESTAMP    | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 入室日時                                   |


#### 3. 部屋管理機能 (20点)

(部屋テーブルを使用)

#### 4. 部屋内チャット機能 (30点)

**messages テーブル**
| カラム名        | データ型       | 制約                                 | 説明                                      |
|---------------|--------------|-------------------------------------|-----------------------------------------|
| id            | INT          | PRIMARY KEY, AUTO_INCREMENT         | メッセージID                                |
| room_id       | INT          | NOT NULL                            | 関連する部屋ID                              |
| sender_id     | INT          | NOT NULL                            | 送信者のユーザーID                            |
| content       | TEXT         | NOT NULL                            | メッセージの内容                             |
| sent_at       | TIMESTAMP    | NOT NULL, DEFAULT CURRENT_TIMESTAMP | メッセージ送信のタイムスタンプ                    |

**blocked_users テーブル**
| カラム名           | データ型       | 制約                                 | 説明                                      |
|------------------|--------------|-------------------------------------|-----------------------------------------|
| block_id         | INT          | PRIMARY KEY, AUTO_INCREMENT         | ブロックID                                |
| blocking_user_id | INT          | NOT NULL                            | ブロックするユーザーのユーザーID                  |
| blocked_user_id  | INT          | NOT NULL                            | ブロックされるユーザーのユーザーID                |


**images テーブル**
| カラム名         | データ型       | 制約                                 | 説明                                      |
|----------------|--------------|-------------------------------------|-----------------------------------------|
| image_id       | INT          | PRIMARY KEY, AUTO_INCREMENT         | 画像ID                                    |
| room_id        | INT          | NOT NULL                            | 関連する部屋ID                              |
| sender_id      | INT          | NOT NULL                            | 画像を送信したユーザーのユーザーID              |
| image_url      | VARCHAR(255) | NOT NULL                            | 画像のURL                                 |
| timestamp      | TIMESTAMP    | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 画像のタイムスタンプ                           |


#### 5. 部屋主の機能 (15点)

(部屋テーブルとユーザーテーブルを使用)

#### 6. 通知とアラート (10点)

(通知テーブルを使用)

#### 7. セキュリティとプライバシー (15点)

(ユーザーテーブルとセッションテーブルを使用)

#### 8. 拡張性とスケーラビリティ (5点)

(バックアップ戦略に関するテーブルなどが必要)

#### 9. UI/UX デザイン (15点)

(データベースには関連しない)

#### 10. モバイル対応 (5点)

(データベースには関連しない)

#### 11. 法的およびコンプライアンス要件 (10点)

(データベースには関連しない)

#### 12. デプロイと運用 (5点)

(データベースには関連しない)

#### 13. SPAM対策 (5点)

**spam_users テーブル**
| カラム名            | データ型       | 制約                                 | 説明                                      |
|-------------------|--------------|-------------------------------------|-----------------------------------------|
| spam_id           | INT          | PRIMARY KEY, AUTO_INCREMENT         | SPAMユーザーID                             |
| user_id           | INT          | NOT NULL                            | SPAM行為を行ったユーザーのユーザーID             |
| spam_points       | INT          | NOT NULL                            | SPAM行為のポイント                         |
| last_spam_activity| TIMESTAMP    | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 最後のSPAM活動のタイムスタンプ                |

**banned_users テーブル**
| カラム名           | データ型       | 制約                                 | 説明                                      |
|------------------|--------------|-------------------------------------|-----------------------------------------|
| ban_id           | INT          | PRIMARY KEY, AUTO_INCREMENT         | BANユーザーID                             |
| user_id          | INT          | NOT NULL                            | BANされたユーザーのID

**spam_messages テーブル**
| カラム名            | データ型       | 制約                                 | 説明                                      |
|-------------------|--------------|-------------------------------------|-----------------------------------------|
| spam_message_id  | INT          | PRIMARY KEY, AUTO_INCREMENT         | SPAMメッセージID                           |
| user_id           | INT          | NOT NULL                            | SPAM行為を行ったユーザーのユーザーID             |
| message           | TEXT         | NOT NULL                            | SPAMメッセージの内容                       |
| timestamp         | TIMESTAMP    | NOT NULL, DEFAULT CURRENT_TIMESTAMP | SPAMメッセージのタイムスタンプ               |
