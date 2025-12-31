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

        <!-- 音声設定＆再生 -->
        <div class="flex flex-col items-center gap-3 mb-4">
          <div class="flex items-center gap-2">
            <label class="text-sm text-gray-600">ボイス</label>
            <select
              v-model="selectedVoiceName"
              class="border border-gray-300 rounded-md px-2 py-1 text-sm"
            >
              <option
                v-for="v in englishVoices"
                :key="v.name"
                :value="v.name"
              >
                {{ v.name }}
              </option>
            </select>
          </div>
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

        <!-- 録音の再生（最新のみ保持） -->
        <div v-if="recordedUrl" class="mt-4 p-4 bg-white rounded flex items-center gap-3">
          <button
            @click="playRecording"
            class="px-4 py-2 rounded-md text-white"
            :class="isPlayingRecording ? 'bg-gray-500 cursor-not-allowed' : 'bg-emerald-600 hover:bg-emerald-700'"
            :disabled="isPlayingRecording"
          >
            {{ isPlayingRecording ? '再生中...' : '🎧 自分の声を再生' }}
          </button>
          <span class="text-xs text-gray-500">最新の録音のみ再生できます</span>
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
let mediaStream: MediaStream | null = null
let playbackAudio: HTMLAudioElement | null = null
const recordedChunks: BlobPart[] = []
const recordedUrl = ref<string | null>(null)
const isPlayingRecording = ref(false)
const voices = ref<SpeechSynthesisVoice[]>([])
const englishVoices = computed(() =>
  voices.value.filter(v => (v.lang || '').toLowerCase().startsWith('en'))
)
const selectedVoiceName = ref<string>('')

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

    // 自動終了時にも録音を確実に止めて保存
    recognition.onend = () => {
      // isRecordingの状態に関わらず、録音が動いていれば確実に確定させる
      if (mediaRecorder) {
        try { mediaRecorder.requestData() } catch {}
        if (mediaRecorder.state === 'recording') {
          mediaRecorder.stop()
        }
      }
      isRecording.value = false
    }
  }

  // 音声合成ボイスの読み込み
  const saved = typeof window !== 'undefined' ? localStorage.getItem('selectedVoiceName') : null
  if (saved) selectedVoiceName.value = saved

  const loadVoices = () => {
    voices.value = window.speechSynthesis.getVoices()
    if (!selectedVoiceName.value && voices.value.length) {
      const def = pickDefaultMaleVoice(voices.value) || englishVoices.value[0] || voices.value[0]
      selectedVoiceName.value = def?.name || ''
    }
  }
  loadVoices()
  if (typeof window !== 'undefined') {
    window.speechSynthesis.onvoiceschanged = loadVoices
  }
})

const playAudio = () => {
  if (!currentPhrase.value) return
  
  // Web Speech APIで音声合成
  const utterance = new SpeechSynthesisUtterance(currentPhrase.value.english)
  utterance.lang = 'en-US'
  utterance.rate = 0.9
  const chosen =
    voices.value.find(v => v.name === selectedVoiceName.value) ||
    pickDefaultMaleVoice(voices.value)
  if (chosen) {
    utterance.voice = chosen
  }
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
    if (mediaRecorder) {
      try { mediaRecorder.requestData() } catch {}
      if (mediaRecorder.state === 'recording') {
        mediaRecorder.stop()
      }
    }
  } else {
    transcription.value = ''
    accuracy.value = null
    recognition.start()
    isRecording.value = true
    // マイク録音開始
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        mediaStream = stream
        const options: MediaRecorderOptions = {}
        if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
          options.mimeType = 'audio/webm;codecs=opus'
        } else if (MediaRecorder.isTypeSupported('audio/webm')) {
          options.mimeType = 'audio/webm'
        }
        mediaRecorder = new MediaRecorder(stream, options)
        recordedChunks.length = 0
        mediaRecorder.ondataavailable = (e: BlobEvent) => {
          if (e.data && e.data.size > 0) recordedChunks.push(e.data)
        }
        mediaRecorder.onstop = () => {
          // 最終dataavailableが届くのを少し待ってからBlob化
          setTimeout(() => {
            const blobType = (options.mimeType as string) || 'audio/webm'
            const blob = new Blob(recordedChunks, { type: blobType })
            if (recordedUrl.value) URL.revokeObjectURL(recordedUrl.value)
            recordedUrl.value = URL.createObjectURL(blob)
            recordedChunks.length = 0
            // データ確定後にトラック停止
            if (mediaStream) {
              mediaStream.getTracks().forEach(t => t.stop())
              mediaStream = null
            }
          }, 50)
        }
        // timeslice指定で定期的にdataavailableを発火させる
        mediaRecorder.start(250)
      })
      .catch(err => {
        console.error('Microphone access denied:', err)
        alert('マイクへのアクセスが拒否されました。ブラウザの権限設定を確認してください。')
      })
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

watch(selectedVoiceName, (v) => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('selectedVoiceName', v || '')
  }
})

function pickDefaultMaleVoice(list: SpeechSynthesisVoice[]) {
  // 男性ボイス名のヒント（環境に依存）
  const maleHints = [
    'male',
    'david',
    'daniel',
    'alex',
    'fred',
    'george',
    'james',
    'john',
    'google uk english male',
    'microsoft david'
  ]
  const enList = list.filter(v => (v.lang || '').toLowerCase().startsWith('en'))
  const found = enList.find(v => maleHints.some(h => v.name.toLowerCase().includes(h)))
  return found || enList[0] || null
}

function playRecording() {
  if (!recordedUrl.value) return
  if (playbackAudio) {
    playbackAudio.pause()
    playbackAudio = null
  }
  playbackAudio = new Audio(recordedUrl.value)
  isPlayingRecording.value = true
  playbackAudio.onended = () => {
    isPlayingRecording.value = false
  }
  playbackAudio.play().catch(() => {
    isPlayingRecording.value = false
  })
}

onBeforeUnmount(() => {
  if (recordedUrl.value) URL.revokeObjectURL(recordedUrl.value)
  if (mediaStream) {
    mediaStream.getTracks().forEach(t => t.stop())
    mediaStream = null
  }
  if (playbackAudio) {
    playbackAudio.pause()
    playbackAudio = null
  }
})
</script>

