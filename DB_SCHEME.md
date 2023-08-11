1. ユーザ認証基盤
Table: users
Columns:
- user_id (Primary Key)
- username
- email
- password_hash (ハッシュ化されたパスワード)
- oauth_provider (LINE or Google)
- oauth_id (外部プロバイダーのユーザーID)
- profile_picture (アイコンのURLなど)
- registration_date
- last_login_date

Table: user_sessions
Columns:
- session_id (Primary Key)
- user_id (Foreign Key: users.user_id)
- access_token
- refresh_token
- expiration_date

2. ユーザ認証とアカウント管理 (ユーザー登録とログイン機能など)
(既存のテーブルを使用)

3. 固定部屋機能
Table: rooms
Columns:
- room_id (Primary Key)
- room_name
- max_users
- status (active or inactive)
- created_by (Foreign Key: users.user_id)
- creation_date

Table: room_users
Columns:
- room_user_id (Primary Key)
- room_id (Foreign Key: rooms.room_id)
- user_id (Foreign Key: users.user_id)
- join_date

4. 部屋内チャット機能
Table: messages
Columns:
- message_id (Primary Key)
- room_id (Foreign Key: rooms.room_id)
- sender_id (Foreign Key: users.user_id)
- receiver_id (Foreign Key: users.user_id)
- content
- timestamp
- read_status

Table: blocked_users
Columns:
- block_id (Primary Key)
- blocking_user_id (Foreign Key: users.user_id)
- blocked_user_id (Foreign Key: users.user_id)

Table: images
Columns:
- image_id (Primary Key)
- room_id (Foreign Key: rooms.room_id)
- sender_id (Foreign Key: users.user_id)
- image_url
- timestamp

5. 部屋主の機能
(部屋テーブルとユーザーテーブルを使用)

6. 通知とアラート
Table: notifications
Columns:
- notification_id (Primary Key)
- user_id (Foreign Key: users.user_id)
- message
- timestamp

7. セキュリティとプライバシー
(ユーザーテーブルとセッションテーブルを使用)

8. 拡張性とスケーラビリティ
(データベースバックアップ戦略に関するテーブルなどが必要)

9. UI/UX デザイン
(データベースには関連しない)

10. モバイル対応
(データベースには関連しない)

11. 法的およびコンプライアンス要件
(データベースには関連しない)

12. デプロイと運用
(データベースには関連しない)

13. SPAM対策
Table: spam_users
Columns:
- spam_id (Primary Key)
- user_id (Foreign Key: users.user_id)
- spam_points
- last_spam_activity

Table: banned_users
Columns:
- ban_id (Primary Key)
- user_id (Foreign Key: users.user_id)
- ban_start_date
- ban_end_date

Table: spam_messages
Columns:
- spam_message_id (Primary Key)
- user_id (Foreign Key: users.user_id)
- message
- timestamp

14. その他のテーブル
(その他、アプリケーションの要件に応じてテーブルを追加することができます。)
