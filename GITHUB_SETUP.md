# GitHub連携ガイド

## 1. GitHubリポジトリの作成

1. GitHubにログインして、https://github.com/new にアクセス
2. リポジトリ名を入力（例: `eigo-learning-app`）
3. 説明を追加（オプション）
4. **Public** または **Private** を選択
5. **「Initialize this repository with a README」のチェックを外す**（既にREADMEがあるため）
6. 「Create repository」をクリック

## 2. ローカルリポジトリとGitHubを接続

GitHubでリポジトリを作成したら、以下のコマンドを実行してください：

```bash
# GitHubリポジトリのURLを追加（YOUR_USERNAMEとYOUR_REPO_NAMEを置き換えてください）
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# またはSSHを使用する場合
# git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git

# ブランチ名をmainに変更（GitHubのデフォルトに合わせる）
git branch -M main

# コードをGitHubにプッシュ
git push -u origin main
```

## 3. 認証について

### HTTPSを使用する場合
- 初回プッシュ時にGitHubのユーザー名とパスワード（またはPersonal Access Token）の入力が求められます
- パスワードの代わりにPersonal Access Tokenを使用することを推奨します
- トークンの作成: https://github.com/settings/tokens

### SSHを使用する場合
- SSH鍵を設定する必要があります
- 設定方法: https://docs.github.com/ja/authentication/connecting-to-github-with-ssh

## 4. 今後の作業フロー

```bash
# 変更をステージング
git add .

# コミット
git commit -m "変更内容の説明"

# GitHubにプッシュ
git push
```

## 5. ブランチの使用（オプション）

```bash
# 新しいブランチを作成
git checkout -b feature/新機能名

# 変更をコミット
git add .
git commit -m "新機能を追加"

# ブランチをプッシュ
git push -u origin feature/新機能名
```

