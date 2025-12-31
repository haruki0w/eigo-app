# GitHub認証エラー解決方法

## 問題
`HarukiHirokawa123`というアカウントで認証しようとしているが、`haruki0w`のリポジトリへのアクセス権限がない。

## 解決方法

### 方法1: Windows認証情報マネージャーから削除（推奨）

1. **認証情報の確認と削除**
   ```powershell
   # 保存されているGitHub認証情報を確認
   cmdkey /list
   
   # GitHub関連の認証情報を削除（以下のいずれかが見つかったら削除）
   cmdkey /delete:git:https://github.com
   # または
   cmdkey /delete:LegacyGeneric:target=git:https://github.com
   ```

2. **Personal Access Tokenを作成**
   - GitHubにログイン（`haruki0w`アカウントで）
   - https://github.com/settings/tokens にアクセス
   - 「Generate new token」→「Generate new token (classic)」をクリック
   - Note: `eigo-app` など適当な名前を入力
   - Expiration: 適切な期限を選択（例: 90 days）
   - Select scopes: 最低限 `repo` にチェック
   - 「Generate token」をクリック
   - **トークンをコピー**（後で見れないので注意！）

3. **プッシュ時にトークンを使用**
   ```bash
   git push -u origin main
   ```
   - Username: `haruki0w` を入力
   - Password: **Personal Access Token**を貼り付け

### 方法2: SSH認証に切り替え（より安全）

1. **SSH鍵を生成**（まだ持っていない場合）
   ```bash
   ssh-keygen -t ed25519 -C "h.haruki0w@gmail.com"
   ```

2. **公開鍵をGitHubに登録**
   ```bash
   # 公開鍵を表示
   cat ~/.ssh/id_ed25519.pub
   ```
   - 表示された内容をコピー
   - https://github.com/settings/keys にアクセス
   - 「New SSH key」をクリック
   - コピーした鍵を貼り付け

3. **リモートURLをSSHに変更**
   ```bash
   git remote set-url origin git@github.com:haruki0w/eigo-app.git
   ```

4. **プッシュ**
   ```bash
   git push -u origin main
   ```

### 方法3: GitHub CLIを使用

```bash
# GitHub CLIをインストール（まだの場合）
# https://cli.github.com/

# 認証
gh auth login

# プッシュ
git push -u origin main
```

