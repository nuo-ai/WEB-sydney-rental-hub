<template>
  <div class="more-filter-panel">
    <!-- 面板头部 -->
    <div class="panel-header">
      <h3 class="panel-title chinese-text">{{ moreLabel }}</h3>
      <button class="close-btn" @click="$emit('close')" aria-label="关闭更多筛选面板">
        <svg class="spec-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M18 6 6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>

    <!-- 面板内容 -->
    <div class="panel-content">
      <!-- 是否带家具 -->
      <div class="form-row">
        <el-checkbox v-model="furnished">
          {{ furnishedLabel }}
        </el-checkbox>
      </div>

      <!-- 最少浴室数 -->
      <div class="form-row">
        <label class="form-label" :for="bathroomsId">{{ bathroomsLabel }}</label>
        <el-select
          :id="bathroomsId"
          ref="firstFocusableRef"
          v-model="bathrooms"
          placeholder="不限"
          class="w-full"
        >
          <el-option :label="anyLabel" value="any" />
          <el-option label="1+" value="1+" />
          <el-option label="2+" value="2+" />
          <el-option label="3+" value="3+" />
          <el-option label="4+" value="4+" />
        </el-select>
      </div>

      <!-- 最少车位数 -->
      <div class="form-row">
        <label class="form-label" :for="parkingId">{{ parkingLabel }}</label>
        <el-select
          :id="parkingId"
          v-model="parking"
          placeholder="不限"
          class="w-full"
        >
          <el-option :label="anyLabel" value="any" />
          <el-option label="0" value="0" />
          <el-option label="1+" value="1+" />
          <el-option label="2+" value="2+" />
          <el-option label="3+" value="3+" />
        </el-select>
      </div>

      <!-- 底部操作按钮 -->
      <div class="panel-footer">
        <el-button class="cancel-btn" size="default" @click="$emit('close')">
          {{ $t('filter.cancel') }}
        </el-button>
        <el-button type="primary" class="apply-btn" size="default" @click="apply">
          {{ $t('filter.apply') }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, inject, nextTick, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usePropertiesStore } from '@/stores/properties'

// 中文注释：更多（高级）筛选面板。仅在“应用”时提交到 store；与其它分离式面板一致。

const emit = defineEmits(['close'])
const router = useRouter()
const t = inject('t') || ((k) => k)

// 本地状态（默认值：不限/未勾选）
const furnished = ref(false)           // 是否带家具（true 才透传）
const bathrooms = ref('any')           // 'any' | '1+' | '2+' | '3+' | '4+'
const parking = ref('any')             // 'any' | '0' | '1+' | '2+' | '3+'

// 可达性：首个可交互控件（打开时尝试聚焦）
const firstFocusableRef = ref(null)
onMounted(() => {
  nextTick(() => {
    // element-plus 的 el-select 支持 focus()
    firstFocusableRef.value?.focus?.()
  })
})

// i18n 文案（带回退）
const moreLabel = computed(() => {
  const v = t('filter.more')
  return v && v !== 'filter.more' ? v : '更多'
})
const furnishedLabel = computed(() => {
  const v = t('filter.furnished')
  return v && v !== 'filter.furnished' ? v : '带家具'
})
const bathroomsLabel = computed(() => {
  const v = t('filter.bathroomsMin')
  return v && v !== 'filter.bathroomsMin' ? v : '最少浴室数'
})
const parkingLabel = computed(() => {
  const v = t('filter.parkingMin')
  return v && v !== 'filter.parkingMin' ? v : '最少车位数'
})
const anyLabel = computed(() => {
  const v = t('filter.any')
  return v && v !== 'filter.any' ? v : '不限'
})

// 唯一 id（简化处理）
const bathroomsId = `bathrooms-${Math.random().toString(36).slice(2, 7)}`
const parkingId = `parking-${Math.random().toString(36).slice(2, 7)}`

const propertiesStore = usePropertiesStore()

// 同步 URL（仅写入非空/有效参数）
const updateUrlQuery = async (filterParams) => {
  try {
    const currentQuery = { ...router.currentRoute.value.query }
    const newQuery = { ...currentQuery }

    // 带家具：仅当为 true 时写入
    if (filterParams.isFurnished === true) {
      newQuery.isFurnished = '1'
    } else {
      delete newQuery.isFurnished
    }

    // 浴室：'any' 不写入，其它写入原始表达（如 '3+')
    if (filterParams.bathrooms && filterParams.bathrooms !== 'any') {
      newQuery.bathrooms = filterParams.bathrooms
    } else {
      delete newQuery.bathrooms
    }

    // 车位：'any' 不写入；'0' 允许写入（有效）
    if (filterParams.parking && filterParams.parking !== 'any') {
      newQuery.parking = filterParams.parking
    } else {
      delete newQuery.parking
    }

    // 幂等比对
    if (JSON.stringify(newQuery) !== JSON.stringify(currentQuery)) {
      await router.replace({ query: newQuery })
    }
  } catch (e) {
    console.warn('同步 URL 查询参数失败（more）：', e)
  }
}

// 应用筛选（提交到 store）
const apply = async () => {
  try {
    // 构造最小参数集（遵循“仅非空写入”）
    const filterParams = {}
    if (furnished.value === true) filterParams.isFurnished = true
    if (bathrooms.value && bathrooms.value !== 'any') filterParams.bathrooms = bathrooms.value
    if (parking.value && parking.value !== 'any') filterParams.parking = parking.value

    // 说明（为什么）：Store 的 mapFilterStateToApiParams 会在 V2 下将其映射为
    // furnished/bathrooms_min/parking_min；V1 下则透传原键（后端可忽略）。
    await propertiesStore.applyFilters(filterParams)

    // URL 同步：仅写入非空（保持可复现）
    await updateUrlQuery(filterParams)

    emit('close')
  } catch (err) {
    console.error('应用更多筛选失败:', err)
  }
}
</script>

<style scoped>
.more-filter-panel {
  width: 100%;
  background: #fff;
  border-radius: 8px;
}

/* 头部 */
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid var(--color-border-default);
}
.panel-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}
.close-btn {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.close-btn:hover {
  background: #f5f5f5;
  color: var(--color-text-primary);
}
.spec-icon {
  width: 20px;
  height: 20px;
}

/* 内容 */
.panel-content {
  padding: 16px;
}
.form-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}
.form-label {
  font-size: 13px;
  color: var(--color-text-secondary);
}

/* 底部操作 */
.panel-footer {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}
.cancel-btn {
  flex: 1;
  background: white;
  border: 1px solid var(--color-border-default);
  color: var(--color-text-secondary);
}
.cancel-btn:hover {
  border-color: var(--color-border-strong);
  color: var(--color-text-primary);
}
.apply-btn {
  flex: 2;
  background-color: var(--juwo-primary);
  border-color: var(--juwo-primary);
}
.apply-btn:hover {
  background-color: var(--juwo-primary-light);
  border-color: var(--juwo-primary-light);
}

/* 细节 */
.w-full { width: 100%; }
</style>
