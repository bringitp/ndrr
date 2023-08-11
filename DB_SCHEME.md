#### 0. ユーザ認証基盤 (15点)

**users テーブル**
- user_id (Primary Key)
- username
- email
- password_hash
- oauth_provider
- oauth_id
- profile_picture
- registration_date
- last_login_date

**user_sessions テーブル**
- session_id (Primary Key)
- user_id (Foreign Key: users.user_id)
- access_token
- refresh_token
- expiration_date

#### 1. ユーザ認証とアカウント管理 (30点)

(既存のテーブルを使用)

#### 2. 固定部屋機能 (5点)

**rooms テーブル**
- room_id (Primary Key)
- room_name
- max_capacity
- active_status
- created_by (Foreign Key: users.user_id)
- created_at
- updated_at

**room_members テーブル**
- member_id (Primary Key)
- room_id (Foreign Key: rooms.room_id)
- user_id (Foreign Key: users.user_id)
- joined_at

#### 3. 部屋管理機能 (20点)

(部屋テーブルを使用)

#### 4. 部屋内チャット機能 (30点)

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