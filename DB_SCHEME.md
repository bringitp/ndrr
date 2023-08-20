## テーブル名はMySQLに準拠するために小文字で統一することとする。  

```sql

-- users テーブル
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
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
INSERT INTO users (username, password_hash, email, avatar, trip, privilege, ng_list)
VALUES
    ('ユーザー1', 'hashed_password_1', 'user1@example.com', NULL, 'trip1', 'user', NULL),
    ('ユーザー2', 'hashed_password_2', 'user2@example.com', NULL, 'trip2', 'user', NULL),
    ('ユーザー3', 'hashed_password_3', 'user3@example.com', NULL, 'trip3', 'user', NULL),
    ('ユーザー4', 'hashed_password_4', 'user4@example.com', NULL, 'trip4', 'user', NULL),
    ('ユーザー5', 'hashed_password_5', 'user5@example.com', NULL, 'trip5', 'user', NULL),
    ('ユーザー6', 'hashed_password_6', 'user6@example.com', NULL, 'trip6', 'user', NULL),
    ('ユーザー7', 'hashed_password_7', 'user7@example.com', NULL, 'trip7', 'user', NULL),
    ('ユーザー8', 'hashed_password_8', 'user8@example.com', NULL, 'trip8', 'user', NULL),
    ('ユーザー9', 'hashed_password_9', 'user9@example.com', NULL, 'trip9', 'user', NULL),
    ('ユーザー10', 'hashed_password_10', 'user10@example.com', NULL, 'trip10', 'user', NULL);

-- user_sessions テーブルのダミーデータ
INSERT INTO user_sessions (session_id, user_id, access_token, refresh_token, expiration_date)
VALUES
    ('session1', 1, 'access_token_1', 'refresh_token_1', '2023-08-11 12:00:00'),
    ('session2', 2, 'access_token_2', 'refresh_token_2', '2023-08-11 12:30:00'),
    ('session3', 3, 'access_token_3', 'refresh_token_3', '2023-08-11 13:00:00'),
    ('session4', 4, 'access_token_4', 'refresh_token_4', '2023-08-11 13:30:00'),
    ('session5', 5, 'access_token_5', 'refresh_token_5', '2023-08-11 14:00:00'),
    ('session6', 6, 'access_token_6', 'refresh_token_6', '2023-08-11 14:30:00'),
    ('session7', 7, 'access_token_7', 'refresh_token_7', '2023-08-11 15:00:00'),
    ('session8', 8, 'access_token_8', 'refresh_token_8', '2023-08-11 15:30:00'),
    ('session9', 9, 'access_token_9', 'refresh_token_9', '2023-08-11 16:00:00'),
    ('session10', 10, 'access_token_10', 'refresh_token_10', '2023-08-11 16:30:00');

-- rooms テーブルのダミーデータ
INSERT INTO rooms (name, owner_id, max_capacity, status, last_activity)
VALUES
    ('部屋1', 1, 10, 'active', '2023-08-11 12:00:00'),
    ('部屋2', 2, 10, 'active', '2023-08-11 12:30:00'),
    ('部屋3', 3, 15, 'active', '2023-08-11 13:00:00'),
    ('部屋4', 4, 15, 'active', '2023-08-11 13:30:00'),
    ('部屋5', 5, 20, 'inactive', '2023-08-11 14:00:00'),
    ('部屋6', 6, 20, 'inactive', '2023-08-11 14:30:00'),
    ('部屋7', 7, 10, 'active', '2023-08-11 15:00:00'),
    ('部屋8', 8, 10, 'active', '2023-08-11 15:30:00'),
    ('部屋9', 9, 15, 'active', '2023-08-11 16:00:00'),
    ('部屋10', 10, 15, 'active', '2023-08-11 16:30:00');


-- room_members テーブルのダミーデータ
INSERT INTO room_members (room_id, user_id, joined_at)
VALUES
    (1, 1, '2023-08-11 12:00:00'),
    (1, 2, '2023-08-11 12:05:00'),
    (1, 3, '2023-08-11 12:10:00'),
    (2, 2, '2023-08-11 12:30:00'),
    (2, 3, '2023-08-11 12:35:00'),
    (3, 1, '2023-08-11 13:00:00'),
    (3, 3, '2023-08-11 13:05:00'),
    (3, 5, '2023-08-11 13:10:00'),
    (4, 4, '2023-08-11 13:30:00'),
    (5, 5, '2023-08-11 14:00:00');

-- messages テーブルのダミーデータ
INSERT INTO messages (room_id, sender_id, content, sent_at)
VALUES
    (1, 1, 'こんにちは！', '2023-08-11 12:01:00'),
    (1, 2, 'やあ、元気？', '2023-08-11 12:03:00'),
    (1, 1, '元気だよ！', '2023-08-11 12:06:00'),
    (2, 2, 'この部屋楽しいね', '2023-08-11 12:31:00'),
    (2, 3, '本当だ！', '2023-08-11 12:32:00'),
    (3, 1, 'みんなおはよう！', '2023-08-11 13:02:00'),
    (3, 3, 'おはよう！', '2023-08-11 13:04:00'),
    (4, 4, '今日の天気はどうかな？', '2023-08-11 13:32:00'),
    (5, 5, 'みんな元気かな', '2023-08-11 14:03:00'),
    (5, 4, '元気だよ！', '2023-08-11 14:05:00');

-- blocked_users テーブルのダミーデータ
INSERT INTO blocked_users (blocking_user_id, blocked_user_id)
VALUES
    (1, 2),
    (1, 3),
    (2, 3),
    (3, 5),
    (4, 5),
    (5, 1),
    (5, 2),
    (5, 3),
    (5, 4),
    (5, 6);

-- images テーブルのダミーデータ
INSERT INTO images (room_id, sender_id, image_url, timestamp)
VALUES
    (1, 1, 'image_url_1.jpg', '2023-08-11 12:02:00'),
    (1, 2, 'image_url_2.jpg', '2023-08-11 12:04:00'),
    (2, 2, 'image_url_3.jpg', '2023-08-11 12:32:00'),
    (3, 1, 'image_url_4.jpg', '2023-08-11 13:03:00'),
    (3, 3, 'image_url_5.jpg', '2023-08-11 13:05:00'),
    (4, 4, 'image_url_6.jpg', '2023-08-11 13:33:00'),
    (5, 5, 'image_url_7.jpg', '2023-08-11 14:04:00'),
    (5, 4, 'image_url_8.jpg', '2023-08-11 14:06:00'),
    (6, 6, 'image_url_9.jpg', '2023-08-11 14:34:00'),
    (7, 7, 'image_url_10.jpg', '2023-08-11 15:01:00');

-- spam_users テーブルのダミーデータ
INSERT INTO spam_users (user_id, spam_points, last_spam_activity)
VALUES
    (1, 3, '2023-08-10 15:00:00'),
    (2, 5, '2023-08-10 16:00:00'),
    (3, 2, '2023-08-10 17:00:00'),
    (4, 7, '2023-08-10 18:00:00'),
    (5, 10, '2023-08-10 19:00:00'),
    (6, 1, '2023-08-10 20:00:00'),
    (7, 4, '2023-08-10 21:00:00'),
    (8, 8, '2023-08-10 22:00:00'),
    (9, 6, '2023-08-10 23:00:00'),
    (10, 9, '2023-08-11 00:00:00');

-- banned_users テーブルのダミーデータ
INSERT INTO banned_users (user_id, ban_start_date, ban_end_date)
VALUES
    (5, '2023-08-11 14:00:00', '2023-08-12 14:00:00'),
    (8, '2023-08-11 15:00:00', '2023-08-13 15:00:00');

-- spam_messages テーブルのダミーデータ
INSERT INTO spam_messages (user_id, message, timestamp)
VALUES
    (3, 'スパムメッセージ1', '2023-08-10 16:00:00'),
    (5, 'スパムメッセージ2', '2023-08-10 17:00:00'),
    (4, 'スパムメッセージ3', '2023-08-10 18:00:00'),
    (7, 'スパムメッセージ4', '2023-08-10 19:00:00'),
    (2, 'スパムメッセージ5', '2023-08-10 20:00:00'),
    (6, 'スパムメッセージ6', '2023-08-10 21:00:00'),
    (10, 'スパムメッセージ7', '2023-08-11 00:00:00');

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
