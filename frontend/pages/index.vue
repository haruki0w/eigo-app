<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-4xl mx-auto">
      <header class="text-center mb-12">
        <h1 class="text-5xl font-bold text-indigo-600 mb-4">
          🌍 英語学習アプリ
        </h1>
        <p class="text-xl text-gray-600 mb-4">
          1か月で日常会話ができるようになる！
        </p>
        <ProgressBar />
      </header>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="situation in situations"
          :key="situation.id"
          @click="selectSituation(situation)"
          class="bg-white rounded-xl shadow-lg p-6 cursor-pointer transform transition-all hover:scale-105 hover:shadow-xl relative"
        >
          <div class="text-4xl mb-4">{{ situation.emoji }}</div>
          <h2 class="text-xl font-semibold text-gray-800 mb-2">
            {{ situation.title }}
          </h2>
          <p class="text-gray-600 text-sm mb-3">{{ situation.description }}</p>
          <SituationProgress :situation-id="situation.id" />
        </div>
      </div>

      <div v-if="selectedSituation" class="mt-8">
        <SituationPractice :situation="selectedSituation" @back="selectedSituation = null" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { getProgress } = useProgress()

interface Phrase {
  english: string
  japanese: string
  audio?: string
}

interface Situation {
  id: string
  title: string
  description: string
  emoji: string
  phrases: Phrase[]
}

const situations = ref<Situation[]>([
  {
    id: 'meeting-friend',
    title: '友達とあった時',
    description: '挨拶と会話の始め方',
    emoji: '👋',
    phrases: []
  },
  {
    id: 'self-introduction',
    title: '自分の自己紹介',
    description: '自分を紹介する表現',
    emoji: '👤',
    phrases: []
  },
  {
    id: 'recent-update',
    title: '近況の報告',
    description: '最近の出来事を伝える',
    emoji: '📢',
    phrases: []
  },
  {
    id: 'asked-opinion',
    title: 'あなたの考えを聞かれたとき',
    description: '意見を述べる表現',
    emoji: '💭',
    phrases: []
  },
  {
    id: 'ask-opinion',
    title: '相手の考えを聞きたいとき',
    description: '相手の意見を尋ねる',
    emoji: '❓',
    phrases: []
  },
  {
    id: 'ordering',
    title: '注文したいとき',
    description: 'レストラン・カフェでの注文',
    emoji: '🍽️',
    phrases: []
  }
])

const selectedSituation = ref<Situation | null>(null)

const selectSituation = async (situation: Situation) => {
  // バックエンドからフレーズを取得
  try {
    const response = await $fetch<{ data: Phrase[] }>(`/api/situations/${situation.id}`)
    situation.phrases = response.data
  } catch (error) {
    console.error('Error fetching phrases:', error)
    // エラー時は空配列を設定
    situation.phrases = []
  }
  selectedSituation.value = situation
}
</script>

