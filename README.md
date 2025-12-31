# 英語学習アプリ

1か月で日常会話ができるようになる英語学習アプリです。

## 機能

- 6つのシチュエーション別学習
  - 友達とあった時
  - 自分の自己紹介
  - 近況の報告
  - あなたの考えを聞かれたとき
  - 相手の考えを聞きたいとき
  - 注文したいとき（レストラン、カフェなど）

- 音声機能
  - ネイティブ音声の再生
  - 発音練習（音声認識）
  - 発音の正確度チェック

## 技術スタック

- **フロントエンド**: Nuxt 3 + Tailwind CSS
- **バックエンド**: Python FastAPI
- **音声**: Web Speech API（ブラウザネイティブ、無料）

## セットアップ

### 前提条件

- Node.js 18以上
- Python 3.8以上
- npm または yarn

### フロントエンド

```bash
# frontendディレクトリに移動
cd frontend

# 依存関係のインストール
npm install

# 開発サーバーの起動
npm run dev
```

ブラウザで `http://localhost:3000` を開きます。

### バックエンド

```bash
# バックエンドディレクトリに移動
cd backend

# 仮想環境の作成（推奨）
python -m venv venv

# 仮想環境の有効化
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

# サーバーの起動
uvicorn main:app --reload
```

APIサーバーは `http://localhost:8000` で起動します。

### 環境変数（オプション）

`.env` ファイルを作成して、APIのベースURLを設定できます：

```
API_BASE_URL=http://localhost:8000
```

## 使い方

1. ホーム画面で学習したいシチュエーションを選択
2. フレーズを学習
3. 音声を聞いて発音を確認
4. 録音機能で発音練習
5. 正確度を確認して上達を目指す

