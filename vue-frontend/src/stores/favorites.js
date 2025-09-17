import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useFavoritesStore = defineStore('favorites', () => {
  // 收藏列表（存储房源ID）
  const favoritesList = ref([])

  // 初始化：从localStorage加载
  const initFavorites = () => {
    const stored = localStorage.getItem('juwo-favorites')
    if (stored) {
      try {
        favoritesList.value = JSON.parse(stored)
      } catch (e) {
        console.error('Failed to load favorites:', e)
        favoritesList.value = []
      }
    }
  }

  // 添加收藏
  const addFavorite = (propertyId) => {
    if (!favoritesList.value.includes(propertyId)) {
      favoritesList.value.push(propertyId)
      saveFavorites()
    }
  }

  // 移除收藏
  const removeFavorite = (propertyId) => {
    const index = favoritesList.value.indexOf(propertyId)
    if (index > -1) {
      favoritesList.value.splice(index, 1)
      saveFavorites()
    }
  }

  // 切换收藏状态
  const toggleFavorite = (propertyId) => {
    if (isFavorite(propertyId)) {
      removeFavorite(propertyId)
    } else {
      addFavorite(propertyId)
    }
  }

  // 检查是否收藏
  const isFavorite = (propertyId) => {
    return favoritesList.value.includes(propertyId)
  }

  // 保存到localStorage
  const saveFavorites = () => {
    localStorage.setItem('juwo-favorites', JSON.stringify(favoritesList.value))
  }

  // 清空收藏
  const clearFavorites = () => {
    favoritesList.value = []
    saveFavorites()
  }

  // 获取收藏数量
  const favoritesCount = computed(() => favoritesList.value.length)

  // 初始化
  initFavorites()

  return {
    favoritesList,
    favoritesCount,
    addFavorite,
    removeFavorite,
    toggleFavorite,
    isFavorite,
    clearFavorites,
  }
})
