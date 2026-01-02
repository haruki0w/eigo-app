import { ref } from "vue";

interface Progress {
  situationId: string;
  completedPhrases: number[];
  lastPracticed: string;
  totalPracticeCount: number;
}

export const useProgress = () => {
  const progressVersion = ref(0);
  const getProgress = (situationId: string): Progress | null => {
    if (typeof window === "undefined") return null;

    // establish reactive dependency
    // eslint-disable-next-line @typescript-eslint/no-unused-expressions
    progressVersion.value;

    const stored = localStorage.getItem(`progress_${situationId}`);
    if (!stored) return null;

    try {
      return JSON.parse(stored);
    } catch {
      return null;
    }
  };

  const saveProgress = (situationId: string, phraseIndex: number) => {
    if (typeof window === "undefined") return;

    const existing = getProgress(situationId);
    const progress: Progress = {
      situationId,
      completedPhrases: existing
        ? [...new Set([...existing.completedPhrases, phraseIndex])]
        : [phraseIndex],
      lastPracticed: new Date().toISOString(),
      totalPracticeCount: existing ? existing.totalPracticeCount + 1 : 1,
    };

    localStorage.setItem(`progress_${situationId}`, JSON.stringify(progress));
    progressVersion.value++;
  };

  const getOverallProgress = () => {
    if (typeof window === "undefined") return { total: 0, completed: 0 };

    // establish reactive dependency
    // eslint-disable-next-line @typescript-eslint/no-unused-expressions
    progressVersion.value;

    const situationIds = [
      "meeting-friend",
      "self-introduction",
      "recent-update",
      "asked-opinion",
      "ask-opinion",
      "ordering",
    ];

    let total = 0;
    let completed = 0;

    situationIds.forEach((id) => {
      const progress = getProgress(id);
      if (progress) {
        total += 7; // 各シチュエーションのフレーズ数（平均）
        completed += progress.completedPhrases.length;
      }
    });

    return { total, completed };
  };

  const clearProgress = (situationId?: string) => {
    if (typeof window === "undefined") return;

    if (situationId) {
      localStorage.removeItem(`progress_${situationId}`);
      progressVersion.value++;
    } else {
      const situationIds = [
        "meeting-friend",
        "self-introduction",
        "recent-update",
        "asked-opinion",
        "ask-opinion",
        "ordering",
      ];
      situationIds.forEach((id) => {
        localStorage.removeItem(`progress_${id}`);
      });
      progressVersion.value++;
    }
  };

  return {
    getProgress,
    saveProgress,
    getOverallProgress,
    clearProgress,
  };
};
