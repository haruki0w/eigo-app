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

class Answer(BaseModel):
    english: str
    japanese: str

class Phrase(BaseModel):
    english: str
    japanese: str
    audio: Optional[str] = None
    answers: Optional[List[Answer]] = None

class SituationResponse(BaseModel):
    data: List[Phrase]

# シチュエーション別のフレーズデータ
PHRASES = {
    "meeting-friend": [
        {"english": "Hey! How are you?", "japanese": "やあ！元気？", "answers": [
            {"english": "I'm good, thanks!", "japanese": "元気だよ、ありがとう。"},
            {"english": "Pretty good. How about you?", "japanese": "なかなか良いよ。あなたは？"},
            {"english": "Not bad at all.", "japanese": "悪くないよ。"}
        ]},
        {"english": "Long time no see!", "japanese": "久しぶり！"},
        {"english": "What have you been up to?", "japanese": "最近どうしてた？", "answers": [
            {"english": "I've been busy with work.", "japanese": "仕事で忙しかったよ。"},
            {"english": "I've been studying English.", "japanese": "英語を勉強してたよ。"},
            {"english": "Just the usual.", "japanese": "いつも通りだよ。"}
        ]},
        {"english": "It's great to see you!", "japanese": "会えて嬉しいよ！"},
        {"english": "How have you been?", "japanese": "調子はどう？", "answers": [
            {"english": "I've been great, thanks.", "japanese": "とても元気だよ、ありがとう。"},
            {"english": "Can't complain.", "japanese": "文句ないよ。"},
            {"english": "Doing well.", "japanese": "順調だよ。"}
        ]},
        {"english": "What's new?", "japanese": "何か新しいことある？", "answers": [
            {"english": "Not much, same as always.", "japanese": "特にないよ、いつも通り。"},
            {"english": "I started a new hobby.", "japanese": "新しい趣味を始めたよ。"},
            {"english": "I got a new job.", "japanese": "新しい仕事を始めたよ。"},
            {"english": "I'm happy I recently earned a new certification in IT.", "japanese": "最近新しい資格が取得できてうれしいよ。"}
        ]},
        {"english": "How's everything?", "japanese": "全て順調？", "answers": [
            {"english": "Everything's good.", "japanese": "全部順調だよ。"},
            {"english": "Things are going well.", "japanese": "うまくいってるよ。"},
            {"english": "So far, so good.", "japanese": "今のところ順調だよ。"}
        ]},
        {"english": "How's it going?", "japanese": "最近どう？", "answers": [
            {"english": "Pretty good!", "japanese": "かなり良いよ！"},
            {"english": "Going well, thanks.", "japanese": "順調だよ、ありがとう。"},
            {"english": "All good here.", "japanese": "こっちは問題ないよ。"}
        ]},
    ],
    "self-introduction": [
        {"english": "Hi, I'm Haruki.", "japanese": "こんにちは、はるきです。"},
        {"english": "Nice to meet you.", "japanese": "はじめまして。"},
        {"english": "I'm from Setagaya, Tokyo.", "japanese": "東京都の世田谷区から来ました。"},
        {"english": "I work as a IT engineer.", "japanese": "ITエンジニアとして働いています。"},
        {"english": "I played baseball for 10 years.", "japanese": "私は野球を10年間やっていました。"},
        {"english": "In my job as an IT engineer, I use Nuxt (Vue) for the frontend and Python and Java for the backend.", "japanese": "ITエンジニアの仕事ではフロントエンドはVueのNuxt、バックエンドはPython、Javaを使用しています。"},
        {"english": "I like baseball.", "japanese": "野球が好きです。"},
        {"english": "I'm 33 years old.", "japanese": "33歳です。"},
        {"english": "I live in Setagaya, Tokyo.", "japanese": "東京都の世田谷区に住んでいます。"},
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
        {"english": "What do you think?", "japanese": "どう思う？", "answers": [
            {"english": "I think it's a good idea.", "japanese": "いい考えだと思う。"},
            {"english": "It might work, but I'm not sure.", "japanese": "うまくいくかもしれないけど、よくわからない。"},
            {"english": "I don't think that's right.", "japanese": "それは正しくないと思う。"}
        ]},
        {"english": "What's your opinion?", "japanese": "あなたの意見は？", "answers": [
            {"english": "In my opinion, we should wait.", "japanese": "私の意見では、待つべきだ。"},
            {"english": "I believe it's worth trying.", "japanese": "試してみる価値があると思う。"},
            {"english": "I think we need more information.", "japanese": "もっと情報が必要だと思う。"}
        ]},
        {"english": "How do you feel about that?", "japanese": "それについてどう感じる？", "answers": [
            {"english": "I'm okay with it.", "japanese": "それで大丈夫だよ。"},
            {"english": "I'm not comfortable with that.", "japanese": "それは気が進まない。"},
            {"english": "I'm excited about it.", "japanese": "それにワクワクしている。"}
        ]},
        {"english": "What are your thoughts?", "japanese": "あなたの考えは？", "answers": [
            {"english": "My thoughts are similar to yours.", "japanese": "私の考えはあなたと似ている。"},
            {"english": "I have a different perspective.", "japanese": "私は違う見方をしている。"},
            {"english": "I haven't decided yet.", "japanese": "まだ決めていない。"}
        ]},
        {"english": "Do you agree?", "japanese": "賛成？", "answers": [
            {"english": "Yes, I agree.", "japanese": "はい、賛成です。"},
            {"english": "I partly agree.", "japanese": "一部は賛成です。"},
            {"english": "No, I disagree.", "japanese": "いいえ、反対です。"}
        ]},
        {"english": "What's your take on this?", "japanese": "これについてどう思う？", "answers": [
            {"english": "My take is that it's promising.", "japanese": "私の見方では、有望だと思う。"},
            {"english": "I think it's risky.", "japanese": "リスクがあると思う。"},
            {"english": "It seems reasonable.", "japanese": "妥当だと思う。"}
        ]},
        {"english": "I'd like to hear your view.", "japanese": "あなたの意見を聞きたいです。", "answers": [
            {"english": "Sure, I think we should proceed.", "japanese": "もちろん、進めるべきだと思う。"},
            {"english": "I feel we should wait.", "japanese": "待つべきだと感じる。"},
            {"english": "I think we need more data.", "japanese": "もっとデータが必要だと思う。"}
        ]},
    ],
    "ordering": [
        {"english": "I'd like to order...", "japanese": "...を注文したいです。"},
        {"english": "Can I have a [item], please?", "japanese": "[アイテム]をください。"},
        {"english": "I'll have the [item].", "japanese": "[アイテム]にします。"},
        {"english": "Could I get a menu?", "japanese": "メニューをいただけますか？", "answers": [
            {"english": "Of course. Here you are.", "japanese": "もちろんです。どうぞ。"},
            {"english": "Sure, just a moment.", "japanese": "はい、少々お待ちください。"}
        ]},
        {"english": "What do you recommend?", "japanese": "おすすめは何ですか？", "answers": [
            {"english": "I recommend the chef's special.", "japanese": "シェフのおすすめをおすすめします。"},
            {"english": "The pasta is very popular.", "japanese": "パスタがとても人気です。"}
        ]},
        {"english": "I'd like a coffee, please.", "japanese": "コーヒーをください。"},
        {"english": "Can I have the check, please?", "japanese": "お会計をお願いします。", "answers": [
            {"english": "Certainly. I'll bring it right away.", "japanese": "かしこまりました。すぐにお持ちします。"},
            {"english": "Sure, just a minute.", "japanese": "はい、少々お待ちください。"}
        ]},
        {"english": "I'll have the same.", "japanese": "同じものをください。"},
        {"english": "Could I have some water?", "japanese": "お水をいただけますか？", "answers": [
            {"english": "Yes, I'll bring some water.", "japanese": "はい、お水をお持ちします。"},
            {"english": "Still or sparkling?", "japanese": "炭酸なしと炭酸あり、どちらがよろしいですか？"}
        ]},
        {"english": "Is this dish spicy?", "japanese": "この料理は辛いですか？", "answers": [
            {"english": "It's mildly spicy.", "japanese": "少し辛いです。"},
            {"english": "Yes, it's quite spicy.", "japanese": "はい、かなり辛いです。"},
            {"english": "No, not at all.", "japanese": "いいえ、全く辛くありません。"}
        ]},
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

