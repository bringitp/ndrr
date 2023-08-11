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
- privileged_user (課金ユーザなどの特権ユーザの状態)

**user_sessions テーブル**
- session_id (Primary Key)
- user_id (Foreign Key: users.user_id)
- access_token
- refresh_token
- expiration_date

**blocked_users テーブル**
- block_id (Primary Key)
- blocking_user_id (Foreign Key: users.user_id)
- blocked_user_id (Foreign Key: users.user_id)

**ng_lists テーブル**
- ng_list_id (Primary Key)
- user_id (Foreign Key: users.user_id)
- blocked_user_id (Foreign Key: users.user_id)

#### ユーザ認証とアカウント管理

(既存のテーブルを使用)

#### 固定部屋機能

(部屋テーブルを使用)

#### 部屋管理機能

(部屋テーブルを使用)

#### 部屋内チャット機能

(メッセージテーブルを使用)

#### 部屋主の機能

(部屋テーブルとユーザーテーブルを使用)

#### 通知とアラート

(通知テーブルを使用)

#### セキュリティとプライバシー

(ユーザーテーブルとセッションテーブルを使用)

#### 拡張性とスケーラビリティ

(バックアップ戦略に関するテーブルなどが必要)

#### UI/UX デザイン

(データベースには関連しない)

#### モバイル対応

(データベースには関連しない)

#### 法的およびコンプライアンス要件

(データベースには関連しない)

#### デプロイと運用

(データベースには関連しない)

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
