<template>
  <div class="bg-white rounded-lg p-4 shadow-md max-w-md mx-auto">
    <div class="flex items-center justify-between mb-2">
      <span class="text-sm font-semibold text-gray-700">学習進捗</span>
      <span class="text-sm text-gray-600">
        {{ completed }} / {{ total }} フレーズ
      </span>
    </div>
    <div class="w-full bg-gray-200 rounded-full h-3">
      <div
        :style="{ width: progressPercentage + '%' }"
        class="bg-gradient-to-r from-indigo-500 to-purple-500 h-3 rounded-full transition-all duration-300"
      ></div>
    </div>
    <p class="text-xs text-gray-500 mt-2 text-center">
      {{ progressPercentage }}% 完了
    </p>
  </div>
</template>

<script setup lang="ts">
const { getOverallProgress } = useProgress()
const progress = computed(() => getOverallProgress())
const total = computed(() => progress.value.total || 42) // 6シチュエーション × 7フレーズ
const completed = computed(() => progress.value.completed)
const progressPercentage = computed(() => {
  if (total.value === 0) return 0
  return Math.round((completed.value / total.value) * 100)
})
</script>

