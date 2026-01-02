interface Answer {
  english: string;
  japanese: string;
}

interface Phrase {
  english: string;
  japanese: string;
  answers?: Answer[];
}

export default defineEventHandler(
  async (event): Promise<{ data: Phrase[] }> => {
    const id = getRouterParam(event, "id");

    // バックエンドAPIからデータを取得
    const config = useRuntimeConfig();
    const apiBase = config.public.apiBase;

    try {
      const response = await $fetch<{ data: Phrase[] }>(
        `${apiBase}/api/situations/${id}`
      );
      return response;
    } catch (error) {
      // フォールバック: ローカルデータ
      return {
        data: getLocalPhrases(id),
      };
    }
  }
);

function getLocalPhrases(id?: string): Phrase[] {
  const phrases: Record<string, Phrase[]> = {
    "meeting-friend": [
      {
        english: "Hey! How are you?",
        japanese: "やあ！元気？",
        answers: [
          { english: "I'm good, thanks!", japanese: "元気だよ、ありがとう。" },
          {
            english: "Pretty good. How about you?",
            japanese: "なかなか良いよ。あなたは？",
          },
          { english: "Not bad at all.", japanese: "悪くないよ。" },
        ],
      },
      { english: "Long time no see!", japanese: "久しぶり！" },
      {
        english: "What have you been up to?",
        japanese: "最近どうしてた？",
        answers: [
          {
            english: "I've been busy with work.",
            japanese: "仕事で忙しかったよ。",
          },
          {
            english: "I've been studying English.",
            japanese: "英語を勉強してたよ。",
          },
          { english: "Just the usual.", japanese: "いつも通りだよ。" },
        ],
      },
      { english: "It's great to see you!", japanese: "会えて嬉しいよ！" },
      {
        english: "How have you been?",
        japanese: "調子はどう？",
        answers: [
          {
            english: "I've been great, thanks.",
            japanese: "とても元気だよ、ありがとう。",
          },
          { english: "Can't complain.", japanese: "文句ないよ。" },
          { english: "Doing well.", japanese: "順調だよ。" },
        ],
      },
      {
        english: "How's it going?",
        japanese: "最近どう？",
        answers: [
          { english: "Pretty good!", japanese: "かなり良いよ！" },
          {
            english: "Going well, thanks.",
            japanese: "順調だよ、ありがとう。",
          },
          { english: "All good here.", japanese: "こっちは問題ないよ。" },
        ],
      },
    ],
    "self-introduction": [
      { english: "Hi, I'm Haruki.", japanese: "こんにちは、はるきです。" },
      { english: "Nice to meet you.", japanese: "はじめまして。" },
      {
        english: "I'm from Setagaya, Tokyo.",
        japanese: "東京都の世田谷区から来ました。",
      },
      {
        english: "I work as a IT engineer.",
        japanese: "ITエンジニアとして働いています。",
      },
      {
        english: "I played baseball for 10 years.",
        japanese: "私は野球を10年間やっていました。",
      },
      { english: "I like baseball.", japanese: "野球が好きです。" },
      { english: "I'm 33 years old.", japanese: "33歳です。" },
      {
        english: "I live in Setagaya, Tokyo.",
        japanese: "東京都の世田谷区に住んでいます。",
      },
      {
        english:
          "In my job as an IT engineer, I use Nuxt (Vue) for the frontend and Python and Java for the backend.",
        japanese:
          "ITエンジニアの仕事ではフロントエンドはVueのNuxt、バックエンドはPython、Javaを使用しています。",
      },
    ],
    "recent-update": [
      {
        english: "I've been really busy lately.",
        japanese: "最近すごく忙しいんだ。",
      },
      {
        english: "I started learning English.",
        japanese: "英語を学び始めたよ。",
      },
      {
        english: "I went to [place] last weekend.",
        japanese: "先週末[場所]に行ったんだ。",
      },
      {
        english: "I've been working on a new project.",
        japanese: "新しいプロジェクトに取り組んでるよ。",
      },
      {
        english: "Not much has changed.",
        japanese: "特に変わったことはないよ。",
      },
    ],
    "asked-opinion": [
      { english: "I think that...", japanese: "私は...だと思います。" },
      { english: "In my opinion...", japanese: "私の意見では..." },
      { english: "I believe...", japanese: "...だと信じています。" },
      { english: "From my perspective...", japanese: "私の視点から見ると..." },
      { english: "I feel that...", japanese: "...だと感じます。" },
    ],
    "ask-opinion": [
      {
        english: "What do you think?",
        japanese: "どう思う？",
        answers: [
          {
            english: "I think it's a good idea.",
            japanese: "いい考えだと思う。",
          },
          {
            english: "It might work, but I'm not sure.",
            japanese: "うまくいくかもしれないけど、よくわからない。",
          },
          {
            english: "I don't think that's right.",
            japanese: "それは正しくないと思う。",
          },
        ],
      },
      {
        english: "What's your opinion?",
        japanese: "あなたの意見は？",
        answers: [
          {
            english: "In my opinion, we should wait.",
            japanese: "私の意見では、待つべきだ。",
          },
          {
            english: "I believe it's worth trying.",
            japanese: "試してみる価値があると思う。",
          },
          {
            english: "I think we need more information.",
            japanese: "もっと情報が必要だと思う。",
          },
        ],
      },
      {
        english: "How do you feel about that?",
        japanese: "それについてどう感じる？",
        answers: [
          { english: "I'm okay with it.", japanese: "それで大丈夫だよ。" },
          {
            english: "I'm not comfortable with that.",
            japanese: "それは気が進まない。",
          },
          {
            english: "I'm excited about it.",
            japanese: "それにワクワクしている。",
          },
        ],
      },
      {
        english: "What are your thoughts?",
        japanese: "あなたの考えは？",
        answers: [
          {
            english: "My thoughts are similar to yours.",
            japanese: "私の考えはあなたと似ている。",
          },
          {
            english: "I have a different perspective.",
            japanese: "私は違う見方をしている。",
          },
          { english: "I haven't decided yet.", japanese: "まだ決めていない。" },
        ],
      },
      {
        english: "Do you agree?",
        japanese: "賛成？",
        answers: [
          { english: "Yes, I agree.", japanese: "はい、賛成です。" },
          { english: "I partly agree.", japanese: "一部は賛成です。" },
          { english: "No, I disagree.", japanese: "いいえ、反対です。" },
        ],
      },
    ],
    ordering: [
      { english: "I'd like to order...", japanese: "...を注文したいです。" },
      {
        english: "Can I have a [item], please?",
        japanese: "[アイテム]をください。",
      },
      { english: "I'll have the [item].", japanese: "[アイテム]にします。" },
      {
        english: "Could I get a menu?",
        japanese: "メニューをいただけますか？",
        answers: [
          {
            english: "Of course. Here you are.",
            japanese: "もちろんです。どうぞ。",
          },
          {
            english: "Sure, just a moment.",
            japanese: "はい、少々お待ちください。",
          },
        ],
      },
      {
        english: "What do you recommend?",
        japanese: "おすすめは何ですか？",
        answers: [
          {
            english: "I recommend the chef's special.",
            japanese: "シェフのおすすめをおすすめします。",
          },
          {
            english: "The pasta is very popular.",
            japanese: "パスタがとても人気です。",
          },
        ],
      },
      {
        english: "I'd like a coffee, please.",
        japanese: "コーヒーをください。",
      },
      {
        english: "Can I have the check, please?",
        japanese: "お会計をお願いします。",
        answers: [
          {
            english: "Certainly. I'll bring it right away.",
            japanese: "かしこまりました。すぐにお持ちします。",
          },
          {
            english: "Sure, just a minute.",
            japanese: "はい、少々お待ちください。",
          },
        ],
      },
    ],
  };

  return id ? phrases[id] || [] : [];
}
