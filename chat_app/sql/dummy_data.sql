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

-- メッセージの追加
-- 部屋1のメッセージ
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
    (5, 4, '元気だよ！', '2023-08-11 14:05:00'),
    -- 以下に追加のダミーデータを生成するクエリを追加
    (1, 3, '最近、新しい本を読みました。内容はとても興味深かったです。', '2023-08-11 12:10:00'),
    (2, 1, 'この部屋のみなさん、こんにちは！私も楽しく参加しています。', '2023-08-11 12:35:00'),
    (3, 2, '今日の朝ごはんはトーストとコーヒーでした。みなさんは何を食べましたか？', '2023-08-11 13:10:00'),
    (4, 1, '近くの公園で運動してきました。汗をかいてリフレッシュしました。', '2023-08-11 13:45:00'),
    (5, 3, '最近は映画を見るのが楽しみです。おすすめの映画があれば教えてください！', '2023-08-11 14:10:00'),
    -- 以下にさらに追加のダミーデータを生成するクエリを追加
    (1, 2, '週末の予定はありますか？私は友達とピクニックに行く予定です。', '2023-08-11 15:05:00'),
    (2, 3, 'この部屋のトピックは何ですか？初めて参加しました。', '2023-08-11 15:20:00'),
    (3, 1, '最近ハイキングに行ってきました。自然の中で過ごすのは気分転換になります。', '2023-08-11 15:45:00'),
    (4, 4, '今日は新しいレストランに行ってきました。美味しい料理が楽しめました。', '2023-08-11 16:10:00'),
    (5, 5, 'この部屋ではどのような話題が盛り上がっていますか？', '2023-08-11 16:30:00');


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
