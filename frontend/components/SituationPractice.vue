<template>
  <div class="bg-white rounded-xl shadow-xl p-8 mt-8">
    <button
      @click="$emit('back')"
      class="mb-6 text-indigo-600 hover:text-indigo-800 flex items-center gap-2"
    >
      ← 戻る
    </button>

    <h2 class="text-3xl font-bold text-gray-800 mb-6">
      {{ situation.emoji }} {{ situation.title }}
    </h2>

    <div v-if="currentPhrase" class="space-y-6">
      <!-- フレーズ表示 -->
      <div class="bg-indigo-50 rounded-lg p-6">
        <div class="text-center mb-4">
          <div class="flex items-center justify-center gap-2 mb-2">
            <p class="text-2xl font-semibold text-indigo-800">
              {{ currentPhrase.english }}
            </p>
            <span
              v-if="completedPhrases.includes(currentIndex)"
              class="text-green-500 text-xl"
              title="完了済み"
            >
              ✓
            </span>
          </div>
          <p class="text-lg text-gray-600">{{ currentPhrase.japanese }}</p>
        </div>

        <!-- 音声再生ボタン -->
        <div class="flex justify-center gap-4 mb-4">
          <button
            @click="playAudio"
            class="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 flex items-center gap-2"
          >
            🔊 音声を聞く
          </button>
        </div>
      </div>

      <!-- 練習モード -->
      <div class="bg-gray-50 rounded-lg p-6">
        <h3 class="text-xl font-semibold mb-4">練習モード</h3>
        
        <div class="mb-4">
          <button
            @click="toggleRecording"
            :class="[
              'w-full py-4 rounded-lg font-semibold transition-all',
              isRecording
                ? 'bg-red-500 text-white hover:bg-red-600'
                : 'bg-green-500 text-white hover:bg-green-600'
            ]"
          >
            {{ isRecording ? '⏹️ 録音を停止' : '🎤 録音して発音練習' }}
          </button>
        </div>

        <div v-if="transcription" class="mt-4 p-4 bg-white rounded">
          <p class="text-gray-700">
            <strong>あなたの発音:</strong> {{ transcription }}
          </p>
          <div v-if="accuracy !== null" class="mt-2">
            <div class="flex items-center gap-2">
              <span>正確度:</span>
              <div class="flex-1 bg-gray-200 rounded-full h-2">
                <div
                  :style="{ width: accuracy + '%' }"
                  :class="[
                    'h-2 rounded-full',
                    accuracy >= 80 ? 'bg-green-500' : accuracy >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                  ]"
                ></div>
              </div>
              <span class="font-semibold">{{ accuracy }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- ナビゲーション -->
      <div class="flex justify-between items-center">
        <button
          @click="previousPhrase"
          :disabled="currentIndex === 0"
          class="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          ← 前へ
        </button>
        <span class="text-gray-600">
          {{ currentIndex + 1 }} / {{ situation.phrases.length }}
        </span>
        <button
          @click="nextPhrase"
          :disabled="currentIndex === situation.phrases.length - 1"
          class="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          次へ →
        </button>
      </div>
    </div>

    <div v-else class="text-center py-8 text-gray-500">
      フレーズを読み込み中...
    </div>
  </div>
</template>

<script setup lang="ts">
interface Phrase {
  english: string
  japanese: string
  audio?: string
}

interface Situation {
  id: string
  title: string
  emoji: string
  phrases: Phrase[]
}

const props = defineProps<{
  situation: Situation
}>()

const emit = defineEmits<{
  back: []
}>()

const { saveProgress, getProgress } = useProgress()
const currentIndex = ref(0)
const currentPhrase = computed(() => props.situation.phrases[currentIndex.value])
const isRecording = ref(false)
const transcription = ref('')
const accuracy = ref<number | null>(null)
const progress = computed(() => getProgress(props.situation.id))
const completedPhrases = computed(() => progress.value?.completedPhrases || [])
let recognition: any = null
let mediaRecorder: MediaRecorder | null = null

onMounted(() => {
  // Web Speech APIの初期化
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition
    recognition = new SpeechRecognition()
    recognition.lang = 'en-US'
    recognition.continuous = false
    recognition.interimResults = false

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript
      transcription.value = transcript
      calculateAccuracy(transcript)
    }

    recognition.onerror = (event: any) => {
      console.error('Speech recognition error:', event.error)
    }
  }
})

const playAudio = () => {
  if (!currentPhrase.value) return
  
  // Web Speech APIで音声合成
  const utterance = new SpeechSynthesisUtterance(currentPhrase.value.english)
  utterance.lang = 'en-US'
  utterance.rate = 0.9
  window.speechSynthesis.speak(utterance)
}

const toggleRecording = () => {
  if (!recognition) {
    alert('お使いのブラウザは音声認識をサポートしていません。')
    return
  }

  if (isRecording.value) {
    recognition.stop()
    isRecording.value = false
  } else {
    transcription.value = ''
    accuracy.value = null
    recognition.start()
    isRecording.value = true
  }
}

const calculateAccuracy = (transcript: string) => {
  if (!currentPhrase.value) return
  
  const expected = currentPhrase.value.english.toLowerCase().trim()
  const actual = transcript.toLowerCase().trim()
  
  // 簡単な類似度計算（レーベンシュタイン距離ベースの簡易版）
  const wordsExpected = expected.split(/\s+/)
  const wordsActual = actual.split(/\s+/)
  
  let matches = 0
  wordsExpected.forEach(word => {
    if (wordsActual.some(actualWord => actualWord.includes(word) || word.includes(actualWord))) {
      matches++
    }
  })
  
  accuracy.value = Math.round((matches / wordsExpected.length) * 100)
  isRecording.value = false
  
  // 正確度が80%以上の場合、進捗を保存
  if (accuracy.value >= 80) {
    saveProgress(props.situation.id, currentIndex.value)
  }
}

const nextPhrase = () => {
  if (currentIndex.value < props.situation.phrases.length - 1) {
    currentIndex.value++
    transcription.value = ''
    accuracy.value = null
  }
}

const previousPhrase = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
    transcription.value = ''
    accuracy.value = null
  }
}
</script>

