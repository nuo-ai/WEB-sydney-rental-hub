<template>
  <div class="saved-searches-manager">
    <!-- 已保存搜索列表 -->
    <div v-if="savedSearches.length > 0" class="saved-searches-list">
      <div
        v-for="search in savedSearches"
        :key="search.id"
        class="saved-search-item"
      >
        <!-- 搜索信息 -->
        <div class="search-info">
          <h3 class="search-name typo-body">{{ search.name }}</h3>
          <div class="search-meta">
            <span class="search-date typo-small">
              保存于 {{ formatDate(search.createdAt) }}
            </span>
            <span class="search-frequency typo-small">
              邮件通知：{{ getFrequencyText(search.emailFrequency) }}
            </span>
          </div>
          <!-- 搜索条件预览 -->
          <div class="search-conditions typo-small">
            {{ generateConditionsText(search.conditions) }}
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="search-actions">
          <BaseButton
            variant="primary"
            size="small"
            @click="applySearch(search)"
            :loading="applyingSearchId === search.id"
          >
            应用搜索
          </BaseButton>

          <BaseButton
            variant="ghost"
            size="small"
            @click="startRename(search)"
          >
            <Edit2 class="action-icon" />
          </BaseButton>

          <BaseButton
            variant="ghost"
            size="small"
            @click="deleteSearch(search.id)"
            :loading="deletingSearchId === search.id"
          >
            <Trash2 class="action-icon" />
          </BaseButton>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <Search class="empty-icon" />
      <h3 class="typo-h3">还没有保存的搜索</h3>
      <p class="typo-body text-secondary">
        在筛选房源时点击"保存搜索"，即可在这里管理您的搜索条件
      </p>
      <router-link to="/">
        <BaseButton variant="primary">开始搜索房源</BaseButton>
      </router-link>
    </div>

    <!-- 重命名弹窗 -->
    <div v-if="renameModalVisible" class="rename-modal-wrapper">
      <div class="rename-modal">
        <div class="modal-header">
          <h3 class="typo-h3">重命名搜索</h3>
          <BaseButton variant="ghost" @click="cancelRename">
            <X class="action-icon" />
          </BaseButton>
        </div>

        <div class="modal-body">
          <label class="input-label typo-body">搜索名称</label>
          <input
            v-model="newSearchName"
            type="text"
            class="search-name-input"
            placeholder="请输入搜索名称"
            maxlength="50"
            @keyup.enter="confirmRename"
            @keyup.escape="cancelRename"
            ref="renameInput"
          />
        </div>

        <div class="modal-footer">
          <BaseButton variant="secondary" @click="cancelRename">
            取消
          </BaseButton>
          <BaseButton
            variant="primary"
            @click="confirmRename"
            :disabled="!newSearchName.trim()"
            :loading="renamingSearchId !== null"
          >
            确认
          </BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, Edit2, Trash2, X } from 'lucide-vue-next'
import { useFilterWizard } from '@/composables/useFilterWizard'
import { BaseButton } from '@sydney-rental-hub/ui'

defineOptions({ name: 'SavedSearchesManager' })

const router = useRouter()
const { getSavedSearches, deleteSavedSearch, applySavedSearch } = useFilterWizard()

const emit = defineEmits(['updated'])

// 响应式状态
const savedSearches = ref([])
const applyingSearchId = ref(null)
const deletingSearchId = ref(null)

// 重命名相关状态
const renameModalVisible = ref(false)
const renamingSearch = ref(null)
const renamingSearchId = ref(null)
const newSearchName = ref('')
const renameInput = ref(null)

// 加载已保存的搜索
const loadSavedSearches = () => {
  try {
    savedSearches.value = getSavedSearches()
    emit('updated', savedSearches.value.slice())
  } catch (error) {
    console.error('加载已保存搜索失败:', error)
    ElMessage.error('加载搜索列表失败')
  }
}

// 应用搜索
const applySearch = async (search) => {
  applyingSearchId.value = search.id

  try {
    const appliedQuery = await applySavedSearch(search)
    if (appliedQuery) {
      ElMessage.success(`已应用搜索"${search.name}"`)
      await router.push({ name: 'home', query: appliedQuery })
    } else {
      ElMessage.error('应用搜索失败，请重试')
    }
  } catch (error) {
    console.error('应用搜索失败:', error)
    ElMessage.error('应用搜索时出现错误')
  } finally {
    applyingSearchId.value = null
  }
}

// 删除搜索
const deleteSearch = async (searchId) => {
  if (!confirm('确定要删除这个搜索吗？此操作无法撤销。')) {
    return
  }

  deletingSearchId.value = searchId

  try {
    const success = deleteSavedSearch(searchId)
    if (success) {
      ElMessage.success('搜索已删除')
      loadSavedSearches() // 重新加载列表
    } else {
      ElMessage.error('删除搜索失败')
    }
  } catch (error) {
    console.error('删除搜索失败:', error)
    ElMessage.error('删除搜索时出现错误')
  } finally {
    deletingSearchId.value = null
  }
}

// 开始重命名
const startRename = (search) => {
  renamingSearch.value = search
  newSearchName.value = search.name
  renameModalVisible.value = true

  nextTick(() => {
    if (renameInput.value) {
      renameInput.value.focus()
      renameInput.value.select()
    }
  })
}

// 确认重命名
const confirmRename = async () => {
  if (!newSearchName.value.trim()) {
    ElMessage.warning('请输入搜索名称')
    return
  }

  renamingSearchId.value = renamingSearch.value.id

  try {
    // 更新本地存储中的搜索名称
    const searches = getSavedSearches()
    const searchIndex = searches.findIndex((s) => s.id === renamingSearch.value.id)

    if (searchIndex !== -1) {
      searches[searchIndex].name = newSearchName.value.trim()
      localStorage.setItem('savedSearches', JSON.stringify(searches))

      ElMessage.success('搜索名称已更新')
      loadSavedSearches() // 重新加载列表
      cancelRename()
    } else {
      ElMessage.error('找不到要重命名的搜索')
    }
  } catch (error) {
    console.error('重命名搜索失败:', error)
    ElMessage.error('重命名失败，请重试')
  } finally {
    renamingSearchId.value = null
  }
}

// 取消重命名
const cancelRename = () => {
  renameModalVisible.value = false
  renamingSearch.value = null
  newSearchName.value = ''
  renamingSearchId.value = null
}

// 格式化日期
const formatDate = (dateString) => {
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  } catch {
    return '未知日期'
  }
}

// 获取邮件频率文本
const getFrequencyText = (frequency) => {
  const frequencyMap = {
    'instant': '即时通知',
    'daily': '每日汇总',
    'weekly': '每周汇总',
    'none': '不接收'
  }
  return frequencyMap[frequency] || '未设置'
}

// 生成搜索条件文本
const generateConditionsText = (conditions) => {
  if (!conditions) return '无条件'

  const parts = []

  // 区域
  if (conditions.areas && conditions.areas.length > 0) {
    const areaNames = conditions.areas.map((area) => area.name || area.suburb).filter(Boolean)
    if (areaNames.length > 0) {
      const areaText = areaNames.length > 2
        ? `${areaNames.slice(0, 2).join('、')} 等 ${areaNames.length} 个区域`
        : areaNames.join('、')
      parts.push(areaText)
    }
  }

  // 房型
  if (conditions.bedrooms) {
    const bedroomText = conditions.bedrooms === '0' ? 'Studio'
      : conditions.bedrooms === '4+' ? '4房及以上'
      : `${conditions.bedrooms}房`
    parts.push(bedroomText)
  }

  // 价格
  if (conditions.priceRange && Array.isArray(conditions.priceRange)) {
    const [min, max] = conditions.priceRange
    if (min > 0 || max < 5000) {
      const priceText = min > 0 && max < 5000
        ? `$${min}-${max}`
        : min > 0 ? `≥$${min}` : `≤$${max}`
      parts.push(priceText)
    }
  }

  // 家具
  if (conditions.furnished) {
    parts.push('有家具')
  }

  return parts.length > 0 ? parts.join(' · ') : '无特定条件'
}

// 初始化加载
loadSavedSearches()
</script>

<style scoped>
.saved-searches-manager {
  width: 100%;
}

.saved-searches-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.saved-search-item {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
  padding: var(--space-4);
  background-color: var(--color-bg-card);
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-md);
  transition: border-color 0.2s ease;
}

.saved-search-item:hover {
  border-color: var(--juwo-primary);
}

.search-info {
  flex: 1;
  min-width: 0;
}

.search-name {
  margin: 0 0 var(--space-2) 0;
  font-weight: 500;
  color: var(--color-text-primary);
}

.search-meta {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  margin-bottom: var(--space-2);
}

.search-date,
.search-frequency {
  color: var(--color-text-secondary);
}

.search-conditions {
  color: var(--color-text-secondary);
  line-height: 1.4;
}

.search-actions {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  flex-shrink: 0;
}

.action-icon {
  width: 16px;
  height: 16px;
}

/* 空状态样式 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-12) var(--space-4);
  text-align: center;
  background-color: var(--color-bg-card);
  border: 1px dashed var(--color-border-default);
  border-radius: var(--radius-md);
}

.empty-icon {
  width: 48px;
  height: 48px;
  color: var(--color-text-secondary);
  margin-bottom: var(--space-4);
}

.empty-state h3 {
  margin: 0 0 var(--space-2) 0;
  color: var(--color-text-primary);
}

.empty-state p {
  margin: 0 0 var(--space-6) 0;
  max-width: 400px;
}

.text-secondary {
  color: var(--color-text-secondary);
}

/* 重命名弹窗样式 */
.rename-modal-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: var(--space-4);
}

.rename-modal {
  background-color: var(--color-bg-card);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-level-3);
  width: 100%;
  max-width: 400px;
  max-height: 90vh;
  overflow: hidden;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4);
  border-bottom: 1px solid var(--color-border-default);
}

.modal-header h3 {
  margin: 0;
  color: var(--color-text-primary);
}

.modal-body {
  padding: var(--space-4);
}

.input-label {
  display: block;
  margin-bottom: var(--space-2);
  color: var(--color-text-primary);
  font-weight: 500;
}

.search-name-input {
  width: 100%;
  padding: var(--space-3);
  border: 1px solid var(--color-border-default);
  border-radius: var(--radius-md);
  font-size: 14px;
  background-color: var(--color-bg-card);
  color: var(--color-text-primary);
  transition: border-color 0.2s ease;
}

.search-name-input:focus {
  outline: none;
  border-color: var(--juwo-primary);
}

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: var(--space-3);
  padding: var(--space-4);
  border-top: 1px solid var(--color-border-default);
}

/* 移动端适配 */
@media (max-width: 768px) {
  .saved-search-item {
    flex-direction: column;
    align-items: stretch;
  }

  .search-actions {
    justify-content: flex-end;
    margin-top: var(--space-2);
  }

  .search-meta {
    flex-direction: row;
    gap: var(--space-3);
  }

  .rename-modal-wrapper {
    padding: var(--space-2);
  }

  .modal-footer {
    flex-direction: column-reverse;
    gap: var(--space-2);
  }

  .modal-footer .base-button {
    width: 100%;
  }
}
</style>
