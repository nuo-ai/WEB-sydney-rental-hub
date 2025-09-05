<template>
  <div class="commute-calculator-container">
    <h3 class="section-title">通勤时间查询</h3>

    <div class="commute-form">
        <div class="destination-input-group">
            <el-input
              id="commute-address-input-vue"
              v-model="newDestinationAddress"
              placeholder="输入大学、车站或地址"
              clearable
              size="large"
            >
                <template #prepend>
                    <i class="fas fa-map-marker-alt"></i>
                </template>
            </el-input>
             <el-input
                v-model="newDestinationName"
                placeholder="目的地别名 (可选)"
                size="large"
                clearable
            />
            <el-button
              type="primary"
              size="large"
              @click="handleAddLocation"
              :disabled="!newDestinationAddress.trim()"
            >
              添加
            </el-button>
        </div>

        <div v-if="commonDestinations.length > 0" class="preset-destinations">
            <el-button
                v-for="dest in commonDestinations"
                :key="dest.name"
                size="small"
                round
                @click="handlePresetClick(dest)"
            >
                {{ dest.name }}
            </el-button>
        </div>
    </div>

    <el-tabs v-model="activeCommuteMode" @tab-change="handleTabChange" class="commute-tabs">
      <el-tab-pane name="DRIVING">
        <template #label><i class="fas fa-car el-icon--left"></i> 驾车</template>
      </el-tab-pane>
      <el-tab-pane name="TRANSIT">
        <template #label><i class="fas fa-bus el-icon--left"></i> 公交</template>
      </el-tab-pane>
      <el-tab-pane name="WALKING">
         <template #label><i class="fas fa-walking el-icon--left"></i> 步行</template>
      </el-tab-pane>
      <el-tab-pane name="BICYCLING">
        <template #label><i class="fas fa-bicycle el-icon--left"></i> 自行车</template>
      </el-tab-pane>
    </el-tabs>

    <div class="commute-results">
        <div v-if="commuteDestinations.length === 0" class="no-results">
            <p>添加一个目的地来计算通勤时间。</p>
        </div>
        <div v-else>
            <transition-group name="list" tag="div">
                <div
                    v-for="dest in commuteDestinations"
                    :key="dest.id"
                    class="commute-result-item"
                >
                    <div class="destination-info">
                        <p class="destination-name">{{ dest.name }}</p>
                        <p class="destination-address">{{ dest.address }}</p>
                    </div>
                    <div class="commute-time">
                        <div v-if="dest.isLoading" class="loading-state">
                            <el-icon class="is-loading"><Loading /></el-icon>
                            <span>计算中...</span>
                        </div>
                        <div v-else-if="dest.results[activeCommuteMode]?.error" class="error-state">
                             <p class="duration-text error">{{ dest.results[activeCommuteMode]?.duration || '计算失败' }}</p>
                        </div>
                        <div v-else-if="dest.results[activeCommuteMode]">
                            <p class="duration-text">{{ dest.results[activeCommuteMode].duration }}</p>
                            <p class="distance-text">{{ dest.results[activeCommuteMode].distance }}</p>
                        </div>
                         <div v-else class="no-data-state">
                            <p class="duration-text">--</p>
                        </div>
                    </div>
                    <el-button
                        type="danger"
                        text
                        circle
                        :icon="Delete"
                        @click="removeDestination(dest.id)"
                        class="remove-btn"
                    />
                </div>
            </transition-group>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue';
import { transportAPI } from '@/services/api';
import { ElMessage } from 'element-plus';
import { Delete, Loading } from '@element-plus/icons-vue';

const props = defineProps({
  property: {
    type: Object,
    required: true
  }
});

const newDestinationAddress = ref('');
const newDestinationName = ref('');
const activeCommuteMode = ref('DRIVING');
const commuteDestinations = reactive([]);

const commonDestinations = reactive([
    { name: 'USYD', address: 'University of Sydney, Camperdown NSW, Australia' },
    { name: 'UNSW', address: 'UNSW Sydney, High Street, Kensington NSW, Australia' },
    { name: 'UTS', address: 'University of Technology Sydney, Broadway, Ultimo NSW, Australia' },
    { name: 'Central Station', address: 'Central Station, Sydney NSW, Australia' },
]);

let autocomplete;
let autocompleteListener;


const loadGoogleMapsScript = (callback) => {
    if (window.google && window.google.maps) {
        callback();
        return;
    }
    const scriptId = 'google-maps-script';
    if (document.getElementById(scriptId)) return;

    const script = document.createElement('script');
    script.id = scriptId;
    // Replace with your actual API key stored securely
    const apiKey = 'YOUR_GOOGLE_MAPS_API_KEY';
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places&callback=initVueGoogleMaps`;
    script.async = true;
    script.defer = true;

    window.initVueGoogleMaps = () => {
        callback();
    };

    document.head.appendChild(script);
};

const initAutocomplete = () => {
    if (!window.google || !window.google.maps || !window.google.maps.places) {
        console.warn("Google Maps Places library not ready.");
        return;
    }

    // It's better to get the element in a way that is scoped to the component if possible
    const input = document.getElementById('commute-address-input-vue');
    if (!input) {
        console.error("Commute address input not found");
        return;
    }

    autocomplete = new google.maps.places.Autocomplete(input, {
        types: ['address'],
        componentRestrictions: { 'country': 'au' }
    });

    autocompleteListener = autocomplete.addListener('place_changed', () => {
        const place = autocomplete.getPlace();
        if (place && place.formatted_address) {
            newDestinationAddress.value = place.formatted_address;
        }
    });
};

onMounted(() => {
    loadGoogleMapsScript(initAutocomplete);
});

onUnmounted(() => {
    if (autocompleteListener) {
        autocompleteListener.remove();
    }
});

const fetchCommuteTime = async (destination, mode) => {
    destination.isLoading = true;
    const origin = `${props.property.latitude},${props.property.longitude}`;
    try {
        const result = await transportAPI.getDirections(origin, destination.address, mode);
        if (result.error) throw new Error(result.error);
        destination.results[mode] = result;
    } catch (error) {
        console.error("Commute calculation failed:", error);
        destination.results[mode] = { error: true, duration: '计算失败', distance: '' };
        ElMessage.error(`无法计算到 ${destination.name} 的通勤时间`);
    } finally {
        destination.isLoading = false;
    }
};

const handleAddLocation = () => {
    const address = newDestinationAddress.value.trim();
    if (!address) return;

    if (commuteDestinations.some(d => d.address === address)) {
        ElMessage.warning('该目的地已存在。');
        return;
    }

    const newDest = reactive({
        id: `dest_${Date.now()}`,
        name: newDestinationName.value.trim() || address,
        address: address,
        results: {},
        isLoading: false
    });
    commuteDestinations.push(newDest);

    fetchCommuteTime(newDest, activeCommuteMode.value);

    newDestinationAddress.value = '';
    newDestinationName.value = '';
};

const handlePresetClick = (dest) => {
    if (commuteDestinations.some(d => d.address === dest.address)) {
        ElMessage.info(`目的地 "${dest.name}" 已在列表中。`);
        return;
    }
     const newDest = reactive({
        id: `dest_${Date.now()}`,
        name: dest.name,
        address: dest.address,
        results: {},
        isLoading: false
    });
    commuteDestinations.push(newDest);
    fetchCommuteTime(newDest, activeCommuteMode.value);
};

const handleTabChange = (newMode) => {
    // newMode is the name of the tab pane, which is the mode string.
    commuteDestinations.forEach(dest => {
        // 无条件重新获取，确保数据刷新
        fetchCommuteTime(dest, newMode);
    });
};

const removeDestination = (destinationId) => {
    const index = commuteDestinations.findIndex(d => d.id === destinationId);
    if (index !== -1) {
        commuteDestinations.splice(index, 1);
    }
};

</script>

<style scoped>
.commute-calculator-container {
    border-top: 1px solid #e3e3e3;
    padding-top: 24px;
}

.section-title {
  font-size: 20px;
  font-weight: 700;
  color: #2d2d2d;
  margin: 0 0 16px 0;
}

.commute-form {
    margin-bottom: 24px;
}

.destination-input-group {
    display: flex;
    gap: 12px;
    margin-bottom: 12px;
}

.preset-destinations {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}
.commute-tabs {
    margin-bottom: 16px;
}
.commute-tabs .el-tabs__item {
    display: flex;
    align-items: center;
    gap: 8px;
}

.commute-results {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.no-results {
    text-align: center;
    color: #999;
    padding: 24px 0;
    font-size: 14px;
}

.commute-result-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 12px;
    background-color: #f8f9fa;
    border-radius: 6px;
    transition: all 0.3s ease;
}

.destination-info {
    flex-grow: 1;
    min-width: 0;
}

.destination-name {
    font-weight: 600;
    color: #2d2d2d;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.destination-address {
    font-size: 12px;
    color: #595959;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.commute-time {
    flex-shrink: 0;
    width: 100px;
    text-align: right;
}

.loading-state {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 8px;
    color: #999;
    font-size: 14px;
}

.duration-text {
    font-weight: 700;
    font-size: 16px;
}
.duration-text.error {
    color: #f56c6c;
}

.distance-text {
    font-size: 12px;
    color: #595959;
}

.remove-btn {
    margin-left: auto;
}

/* Transition for list items */
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
