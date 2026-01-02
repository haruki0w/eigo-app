<template>
  <div class="mt-2">
    <div class="flex items-center justify-between text-xs text-gray-500 mb-1">
      <span>進捗</span>
      <span>{{ completedCount }} / {{ totalCount }}</span>
    </div>
    <div class="w-full bg-gray-200 rounded-full h-2">
      <div
        :style="{ width: percentage + '%' }"
        :class="[
          'h-2 rounded-full transition-all',
          percentage === 100 ? 'bg-green-500' : 'bg-indigo-500'
        ]"
      ></div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  situationId: string
}>()

const { getProgress } = useProgress()
const progress = computed(() => getProgress(props.situationId))
const completedCount = computed(() => progress.value?.completedPhrases.length || 0)

// 実データ件数で合計を表示（バックエンド優先、失敗時は既定値）
const totalCount = ref<number>(7)
onMounted(async () => {
  try {
    const res = await $fetch<{ data: { english: string; japanese: string }[] }>(
      `/api/situations/${props.situationId}`
    )
    totalCount.value = Array.isArray(res?.data) ? res.data.length : 7
  } catch {
    totalCount.value = 7
  }
})

const percentage = computed(() => {
  if (totalCount.value === 0) return 0
  return Math.round((completedCount.value / totalCount.value) * 100)
})
</script>

