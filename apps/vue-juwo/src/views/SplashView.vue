<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 3 秒兜底自动跳转到列表页（移动端常见品牌页行为）
onMounted(() => {
  const timer = setTimeout(() => {
    // 若用户未点击“进入”，则自动进入列表页
    router.push('/listings')
  }, 3000)

  // 组件卸载安全清理
  return () => clearTimeout(timer)
})

// 点击“进入”按钮的显式跳转
function enter() {
  router.push('/listings')
}
</script>

<template>
  <main class="min-h-dvh flex flex-col items-center justify-between bg-black text-white">
    <!-- 顶部占位（如状态栏安全距离） -->
    <div class="h-6 w-full"></div>

    <!-- 品牌Logo与标语 -->
    <section class="flex flex-col items-center gap-4 px-6 text-center">
      <div class="size-20 rounded-full bg-white/10 ring-1 ring-white/20 grid place-items-center">
        <!-- 简易占位 Logo，后续可换为品牌 SVG -->
        <span class="text-2xl font-bold">JUWO</span>
      </div>
      <h1 class="text-3xl font-semibold tracking-wide">桔屋找房</h1>
      <p class="text-white/70 text-sm leading-relaxed">
        悉尼租房更简单。用事实和数据，帮你快速筛选靠谱房源。
      </p>
    </section>

    <!-- 进入按钮 -->
    <section class="w-full px-6 pb-10">
      <button
        class="w-full h-12 rounded-xl bg-white text-black font-medium active:scale-[0.99] transition"
        @click="enter"
        aria-label="进入房源列表"
      >
        进入
      </button>
      <p class="mt-3 text-center text-xs text-white/50">3 秒后将自动进入</p>
    </section>
  </main>
</template>

<style scoped>
/* TODO: 后续可接入品牌渐变/插画动画 */
</style>
