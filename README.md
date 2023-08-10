# ndrr

   
チャットサイトを作ることを考える。実装部分の大枠を考えたい。実装をリストにせよ。
部屋をつくることができるサイトで、部屋の上限人数は２０人。使われなくなった部屋は廃棄される。部屋主は部屋名の変更、部屋の人数の変更、部屋にいる人を部屋から追い出す機能がある。

なおユーザ認証はCognitoまたはKeycloakを用いることとする。
ログインしたユーザは自身の名前を変更する機能を持つ。
   
---

## 1. ユーザ認証とアカウント管理 (15点)
- CognitoまたはKeycloakを使用してユーザー認証を実装
- ユーザー登録とログイン機能
- ユーザー名の変更機能

## 2. 部屋管理機能 (20点)
- 部屋の作成、編集、削除機能
- 部屋のリスト表示
- 部屋の上限人数制限 (最大20人)
- 部屋の状態 (アクティブ、非アクティブ) の管理
- 部屋の活動状態の管理と廃棄機能

## 3. 部屋内チャット機能 (20点)
- リアルタイムチャット機能の実装
- テキストメッセージの送受信
- メッセージの表示と読了管理

## 4. 部屋主の機能 (15点)
- 部屋主の特権である部屋名変更機能の実装
- 部屋主の特権である部屋の人数変更機能の実装
- 部屋主の特権である部屋からのユーザーの追放機能の実装

## 5. 通知とアラート (10点)
- 新しいメッセージの通知
- 部屋への招待や変更に関する通知

## 6. ユーザー間のつながり (10点)
- ✗フレンド追加/承認機能 (部屋の共有など)
- ✗ユーザー検索機能

## 7. セキュリティとプライバシー (15点)
- データ暗号化とセキュリティ対策
- セッション管理とトークンベースの認証

## 8. 拡張性とスケーラビリティ (10点)
- ✗部屋数やユーザー数の増加に対応するアーキテクチャ
- ✗サーバークラスタリングと負荷分散

## 9. UI/UX デザイン (5点)
- ユーザーフローの設計
- 部屋リスト、チャット画面のデザイン

## 10. モバイル対応 (5点)
- レスポンシブデザインの導入
- ✗モバイルアプリの開発 (必要であれば)

## 11. 国際化と多言語対応 (5点)
- ✗多言語サポート
- ✗ローカライズされたテキストとエラーメッセージ

## 12. 法的およびコンプライアンス要件 (10点)
- ユーザーデータの保護と適切な処理
- ✗個人情報保護法などの法的要件の遵守

## 13. デプロイと運用 (5点)
- サーバーのセットアップとデプロイ
- ログとエラートラッキングの設定
- システムのモニタリングとスケーリング戦略

## 14. SPAM対策 (15点)
- SPAM判定ロジックの実装
- SPAM行為を行うユーザに対する認証基盤での点数加点

---
