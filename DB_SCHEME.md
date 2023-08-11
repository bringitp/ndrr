## テーブル名はMySQLに準拠するために小文字で統一することとする。  

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
