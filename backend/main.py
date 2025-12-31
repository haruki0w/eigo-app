from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="英語学習API")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Phrase(BaseModel):
    english: str
    japanese: str
    audio: Optional[str] = None

class SituationResponse(BaseModel):
    data: List[Phrase]

# シチュエーション別のフレーズデータ
PHRASES = {
    "meeting-friend": [
        {"english": "Hey! How are you?", "japanese": "やあ！元気？"},
        {"english": "Long time no see!", "japanese": "久しぶり！"},
        {"english": "What have you been up to?", "japanese": "最近どうしてた？"},
        {"english": "It's great to see you!", "japanese": "会えて嬉しいよ！"},
        {"english": "How have you been?", "japanese": "調子はどう？"},
        {"english": "What's new?", "japanese": "何か新しいことある？"},
        {"english": "How's everything?", "japanese": "全て順調？"},
    ],
    "self-introduction": [
        {"english": "Hi, I'm [name].", "japanese": "こんにちは、[名前]です。"},
        {"english": "Nice to meet you.", "japanese": "はじめまして。"},
        {"english": "I'm from [place].", "japanese": "[場所]から来ました。"},
        {"english": "I work as a [job].", "japanese": "[職業]として働いています。"},
        {"english": "I enjoy [hobby].", "japanese": "[趣味]が好きです。"},
        {"english": "I'm [age] years old.", "japanese": "[年齢]歳です。"},
        {"english": "I live in [city].", "japanese": "[都市]に住んでいます。"},
    ],
    "recent-update": [
        {"english": "I've been really busy lately.", "japanese": "最近すごく忙しいんだ。"},
        {"english": "I started learning English.", "japanese": "英語を学び始めたよ。"},
        {"english": "I went to [place] last weekend.", "japanese": "先週末[場所]に行ったんだ。"},
        {"english": "I've been working on a new project.", "japanese": "新しいプロジェクトに取り組んでるよ。"},
        {"english": "Not much has changed.", "japanese": "特に変わったことはないよ。"},
        {"english": "I've been doing well.", "japanese": "順調にやってるよ。"},
        {"english": "I took up a new hobby.", "japanese": "新しい趣味を始めたんだ。"},
    ],
    "asked-opinion": [
        {"english": "I think that...", "japanese": "私は...だと思います。"},
        {"english": "In my opinion...", "japanese": "私の意見では..."},
        {"english": "I believe...", "japanese": "...だと信じています。"},
        {"english": "From my perspective...", "japanese": "私の視点から見ると..."},
        {"english": "I feel that...", "japanese": "...だと感じます。"},
        {"english": "It seems to me that...", "japanese": "私には...のように思えます。"},
        {"english": "I would say...", "japanese": "...と言えると思います。"},
    ],
    "ask-opinion": [
        {"english": "What do you think?", "japanese": "どう思う？"},
        {"english": "What's your opinion?", "japanese": "あなたの意見は？"},
        {"english": "How do you feel about that?", "japanese": "それについてどう感じる？"},
        {"english": "What are your thoughts?", "japanese": "あなたの考えは？"},
        {"english": "Do you agree?", "japanese": "賛成？"},
        {"english": "What's your take on this?", "japanese": "これについてどう思う？"},
        {"english": "I'd like to hear your view.", "japanese": "あなたの意見を聞きたいです。"},
    ],
    "ordering": [
        {"english": "I'd like to order...", "japanese": "...を注文したいです。"},
        {"english": "Can I have a [item], please?", "japanese": "[アイテム]をください。"},
        {"english": "I'll have the [item].", "japanese": "[アイテム]にします。"},
        {"english": "Could I get a menu?", "japanese": "メニューをいただけますか？"},
        {"english": "What do you recommend?", "japanese": "おすすめは何ですか？"},
        {"english": "I'd like a coffee, please.", "japanese": "コーヒーをください。"},
        {"english": "Can I have the check, please?", "japanese": "お会計をお願いします。"},
        {"english": "I'll have the same.", "japanese": "同じものをください。"},
        {"english": "Could I have some water?", "japanese": "お水をいただけますか？"},
        {"english": "Is this dish spicy?", "japanese": "この料理は辛いですか？"},
    ],
}

@app.get("/")
async def root():
    return {"message": "英語学習API", "version": "1.0.0"}

@app.get("/api/situations/{situation_id}", response_model=SituationResponse)
async def get_situation_phrases(situation_id: str):
    """シチュエーション別のフレーズを取得"""
    phrases = PHRASES.get(situation_id, [])
    return {"data": [Phrase(**phrase) for phrase in phrases]}

@app.get("/api/situations")
async def get_all_situations():
    """全てのシチュエーション一覧を取得"""
    return {
        "situations": [
            {"id": "meeting-friend", "title": "友達とあった時", "emoji": "👋"},
            {"id": "self-introduction", "title": "自分の自己紹介", "emoji": "👤"},
            {"id": "recent-update", "title": "近況の報告", "emoji": "📢"},
            {"id": "asked-opinion", "title": "あなたの考えを聞かれたとき", "emoji": "💭"},
            {"id": "ask-opinion", "title": "相手の考えを聞きたいとき", "emoji": "❓"},
            {"id": "ordering", "title": "注文したいとき", "emoji": "🍽️"},
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

