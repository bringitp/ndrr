# ndrr

   
チャットサイトを作ることを考える。実装部分の大枠を考えたい。実装をリストにせよ。
部屋をつくることができるサイトで、部屋の上限人数は２０人。使われなくなった部屋は廃棄される。部屋主は部屋名の変更、部屋の人数の変更、部屋にいる人を部屋から追い出す機能がある。

なおユーザ認証はCognitoまたはKeycloakを用いることとする。
ログインしたユーザは自身の名前を変更する機能を持つ。

SMSの料金はCognitoを使う場合ここに従う(https://aws.amazon.com/jp/sns/sms-pricing/) 
1通あたり１円のように読める・・・が・・・？ (Base Price + Carrier Price )   

![image](https://github.com/bringitp/ndrr/assets/141851166/aa9709a4-6e16-42eb-9a7b-4d02350c96c2)  
SMSは使わない

---

## 0. ユーザ認証基盤 (15点)
- LINE認証かGoogleアカウントの認証OAuth 2.0を使う

## 1. ユーザ認証とアカウント管理 (15点)
- ユーザー登録とログイン機能
- ユーザー名の変更機能
- ユーザーのアイコン変更機能
- 退会処理

## 2. 固定部屋機能 (5点)
- 部屋の活動状態の管理

## 3. 部屋管理機能 (20点)
- 部屋の作成、編集、削除機能
- 部屋のリスト表示
- 部屋の上限人数制限 (最大20人)
- 部屋の状態 (アクティブ、非アクティブ) の管理
- 部屋の活動状態の管理と誰も居ない部屋の廃棄機能

## 4. 部屋内チャット機能 (30点)
- リアルタイムチャット機能の実装
- テキストメッセージの送受信
- メッセージの表示と読了管理
- 部屋内でのみ可能な1対1チャット
- 部屋内でのみ可能な1対1チャットの拒否リスト（ユーザ認証基盤での永続管理)
- 部屋チャットでの相手の無視機能
- 部屋チャットで画像投稿処理
- 30分以上無言であれば部屋チャットからの追い出し処理

## 5. 部屋主の機能 (15点)
- 部屋主の特権である部屋名変更機能の実装
- 部屋主の特権である部屋の人数変更機能の実装
- 部屋主の特権である部屋からのユーザーの追放機能の実装
- 部屋主の特権を他者に委任
  
## 5. 通知とアラート (10点)
- 新しいメッセージの通知
- 部屋への招待や変更に関する通知

## 6. セキュリティとプライバシー (15点)
- データ暗号化とセキュリティ対策
- セッション管理とトークンベースの認証

## 7. 拡張性とスケーラビリティ (5点)
- 定期バックアップ

## 9. UI/UX デザイン (15点)
- ユーザーフローの設計
- 部屋リスト、チャット画面のデザイン

## 10. モバイル対応 (5点)
- レスポンシブデザインの導入
- ✗モバイルアプリの開発 (必要であれば)

## 11. 法的およびコンプライアンス要件 (10点)
- ユーザーデータの保護と適切な処理

## 13. デプロイと運用 (5点)
- サーバーのセットアップとデプロイ
- ログとエラートラッキングの設定
- システムのモニタリングとスケーリング戦略
- 
## 14. SPAM対策 (5点)
- SPAM判定ロジックの実装（リーベンシュタイン距離の短いものを短時間に連続投稿を行った場合/NGワードを含んでいた場合)
- SPAM行為を行うユーザに対する認証基盤での点数加点
- SPAM行為を行うユーザの部屋からの追放

---
