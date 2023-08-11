### データベーステーブルとカラム

#### ユーザ認証基盤

**users テーブル**
- user_id (Primary Key)
- username
- email
- password_hash (ハッシュ化されたパスワード)
- oauth_provider (LINE or Google)
- oauth_id (外部プロバイダーのユーザーID)
- profile_picture (アイコンのURLなど)
- registration_date
- last_login_date

**user_sessions テーブル**
- session_id (Primary Key)
- user_id (Foreign Key: users.user_id)
- access_token
- refresh_token
- expiration_date

#### 部屋機能

**rooms テーブル**
- room_id (Primary Key)
- room_name
- max_users
- status (active or inactive)
- created_by (Foreign Key: users.user_id)
- creation_date

**room_users テーブル**
- room_user_id (Primary Key)
- room_id (Foreign Key: rooms.room_id)
- user_id (Foreign Key: users.user_id)
- join_date

#### チャット機能

**messages テーブル**
- message_id (Primary Key)
- room_id (Foreign Key: rooms.room_id)
- sender_id (Foreign Key: users.user_id)
- receiver_id (Foreign Key: users.user_id)
- content
- timestamp
- read_status

**blocked_users テーブル**
- block_id (Primary Key)
- blocking_user_id (Foreign Key: users.user_id)
- blocked_user_id (Foreign Key: users.user_id)

**images テーブル**
- image_id (Primary Key)
- room_id (Foreign Key: rooms.room_id)
- sender_id (Foreign Key: users.user_id)
- image_url
- timestamp

#### 部屋主の機能

(部屋テーブルとユーザーテーブルを使用)

#### 通知とアラート

**notifications テーブル**
- notification_id (Primary Key)
- user_id (Foreign Key: users.user_id)
- message
- timestamp

#### セキュリティとプライバシー

(ユーザーテーブルとセッションテーブルを使用)

#### SPAM対策

**spam_users テーブル**
- spam_id (Primary Key)
- user_id (Foreign Key: users.user_id)
- spam_points
- last_spam_activity

**banned_users テーブル**
- ban_id (Primary Key)
- user_id (Foreign Key: users.user_id)
- ban_start_date
- ban_end_date

**spam_messages テーブル**
- spam_message_id (Primary Key)
- user_id (Foreign Key: users.user_id)
- message
- timestamp

#### その他のテーブル

(その他、アプリケーションの要件に応じてテーブルを追加することができます。)
