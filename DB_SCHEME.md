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
| カラム名        | データ型       | 制約                                 | 説明                                      |
|---------------|--------------|-------------------------------------|-----------------------------------------|
| id            | INT          | PRIMARY KEY, AUTO_INCREMENT         | 部屋ID                                    |
| name          | VARCHAR(50)  | NOT NULL                            | 部屋名（50文字以下）                        |
| owner_id      | INT          | NOT NULL                            | 部屋主のユーザーID                           |
| max_capacity  | INT          | NOT NULL, DEFAULT 20                | 部屋の最大人数（デフォルト20人）                 |
| status        | ENUM         | NOT NULL, DEFAULT 'active'          | 部屋の状態（'active', 'inactive' など）        |
| last_activity| TIMESTAMP    | NOT NULL, DEFAULT CURRENT_TIMESTAMP | 最終アクティビティのタイムスタンプ               |

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
