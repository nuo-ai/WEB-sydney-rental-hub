<template>
  <div class="transport-modes">
    <button
      v-for="mode in modes"
      :key="mode.value"
      :class="['mode-btn', { active: modelValue === mode.value }]"
      @click="selectMode(mode.value)"
      :title="mode.label"
    >
      <i :class="mode.icon"></i>
    </button>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: 'DRIVING'
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const modes = [
  {
    value: 'DRIVING',
    icon: 'fas fa-car',
    label: 'Driving'
  },
  {
    value: 'TRANSIT',
    icon: 'fas fa-bus',
    label: 'Public transport'
  },
  {
    value: 'WALKING',
    icon: 'fas fa-walking',
    label: 'Walking'
  }
]

const selectMode = (value) => {
  emit('update:modelValue', value)
  emit('change', value)
}
</script>

<style scoped>
.transport-modes {
  display: flex;
  gap: 12px;
  margin: 20px 0;
}

.mode-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: none;
  background: #f5f5f5;
  color: #666;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.mode-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.1);
  transform: translate(-50%, -50%);
  transition: width 0.3s, height 0.3s;
}

.mode-btn:hover::before {
  width: 100%;
  height: 100%;
}

.mode-btn:hover {
  background: #ebebeb;
}

.mode-btn:active {
  transform: scale(0.95);
}

.mode-btn.active {
  background: #333;
  color: white;
}

.mode-btn.active:hover {
  background: #222;
}

/* 触摸设备优化 */
@media (hover: none) {
  .mode-btn:hover::before {
    width: 0;
    height: 0;
  }

  .mode-btn:hover {
    background: #f5f5f5;
  }

  .mode-btn.active:hover {
    background: #333;
  }
}
</style>
