export default defineEventHandler(async (event) => {
  const id = getRouterParam(event, 'id')
  
  // バックエンドAPIからデータを取得
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase
  
  try {
    const response = await $fetch(`${apiBase}/api/situations/${id}`)
    return response
  } catch (error) {
    // フォールバック: ローカルデータ
    return {
      data: getLocalPhrases(id)
    }
  }
})

function getLocalPhrases(id: string) {
  const phrases: Record<string, any[]> = {
    'meeting-friend': [
      { english: 'Hey! How are you?', japanese: 'やあ！元気？' },
      { english: 'Long time no see!', japanese: '久しぶり！' },
      { english: 'What have you been up to?', japanese: '最近どうしてた？' },
      { english: 'It\'s great to see you!', japanese: '会えて嬉しいよ！' },
      { english: 'How have you been?', japanese: '調子はどう？' }
    ],
    'self-introduction': [
      { english: 'Hi, I\'m [name].', japanese: 'こんにちは、[名前]です。' },
      { english: 'Nice to meet you.', japanese: 'はじめまして。' },
      { english: 'I\'m from [place].', japanese: '[場所]から来ました。' },
      { english: 'I work as a [job].', japanese: '[職業]として働いています。' },
      { english: 'I enjoy [hobby].', japanese: '[趣味]が好きです。' }
    ],
    'recent-update': [
      { english: 'I\'ve been really busy lately.', japanese: '最近すごく忙しいんだ。' },
      { english: 'I started learning English.', japanese: '英語を学び始めたよ。' },
      { english: 'I went to [place] last weekend.', japanese: '先週末[場所]に行ったんだ。' },
      { english: 'I\'ve been working on a new project.', japanese: '新しいプロジェクトに取り組んでるよ。' },
      { english: 'Not much has changed.', japanese: '特に変わったことはないよ。' }
    ],
    'asked-opinion': [
      { english: 'I think that...', japanese: '私は...だと思います。' },
      { english: 'In my opinion...', japanese: '私の意見では...' },
      { english: 'I believe...', japanese: '...だと信じています。' },
      { english: 'From my perspective...', japanese: '私の視点から見ると...' },
      { english: 'I feel that...', japanese: '...だと感じます。' }
    ],
    'ask-opinion': [
      { english: 'What do you think?', japanese: 'どう思う？' },
      { english: 'What\'s your opinion?', japanese: 'あなたの意見は？' },
      { english: 'How do you feel about that?', japanese: 'それについてどう感じる？' },
      { english: 'What are your thoughts?', japanese: 'あなたの考えは？' },
      { english: 'Do you agree?', japanese: '賛成？' }
    ],
    'ordering': [
      { english: 'I\'d like to order...', japanese: '...を注文したいです。' },
      { english: 'Can I have a [item], please?', japanese: '[アイテム]をください。' },
      { english: 'I\'ll have the [item].', japanese: '[アイテム]にします。' },
      { english: 'Could I get a menu?', japanese: 'メニューをいただけますか？' },
      { english: 'What do you recommend?', japanese: 'おすすめは何ですか？' },
      { english: 'I\'d like a coffee, please.', japanese: 'コーヒーをください。' },
      { english: 'Can I have the check, please?', japanese: 'お会計をお願いします。' }
    ]
  }
  
  return phrases[id] || []
}

