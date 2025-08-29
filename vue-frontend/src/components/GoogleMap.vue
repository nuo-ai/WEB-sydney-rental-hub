<template>
  <div class="google-map-container">
    <div ref="mapRef" class="google-map" :id="mapId">
      <!-- 加载占位符 -->
      <div v-if="!mapLoaded" class="map-loading">
        <el-icon class="is-loading" :size="24"><Loading /></el-icon>
        <span>Loading map...</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { Loading } from '@element-plus/icons-vue'

const props = defineProps({
  latitude: {
    type: Number,
    required: true
  },
  longitude: {
    type: Number,
    required: true
  },
  zoom: {
    type: Number,
    default: 14
  },
  height: {
    type: String,
    default: '200px'
  },
  showMarker: {
    type: Boolean,
    default: true
  },
  markerTitle: {
    type: String,
    default: 'Property Location'
  }
})

const mapRef = ref(null)
const mapId = `map-${Math.random().toString(36).substr(2, 9)}`
const mapLoaded = ref(false)
let map = null
let marker = null
let googleMapsLoaded = false
let isInitializing = false

// Check if Google Maps is already loaded
const isGoogleMapsLoaded = () => {
  return typeof google !== 'undefined' && google.maps
}

// Load Google Maps script
const loadGoogleMaps = () => {
  return new Promise((resolve, reject) => {
    if (isGoogleMapsLoaded()) {
      googleMapsLoaded = true
      resolve()
      return
    }

    // Check if script is already being loaded
    if (window.googleMapsLoadPromise) {
      window.googleMapsLoadPromise.then(resolve).catch(reject)
      return
    }

    // Create a new promise for loading
    window.googleMapsLoadPromise = new Promise((resolveLoad, rejectLoad) => {
      const script = document.createElement('script')
      const apiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || 'AIzaSyDR-IqWUXtp64-Pfp09FwGvFHnbKjMNuqU'
      script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places`
      script.async = true
      script.defer = true
      
      script.onload = () => {
        googleMapsLoaded = true
        resolveLoad()
      }
      
      script.onerror = () => {
        const error = new Error('Failed to load Google Maps')
        rejectLoad(error)
      }
      
      document.head.appendChild(script)
    })

    window.googleMapsLoadPromise.then(resolve).catch(reject)
  })
}

// Initialize the map
const initMap = async () => {
  // Prevent multiple initializations
  if (isInitializing || mapLoaded.value) {
    return
  }
  
  isInitializing = true
  
  try {
    console.log('Initializing map with coords:', props.latitude, props.longitude)
    await loadGoogleMaps()
    
    // Wait for DOM to be ready
    await nextTick()
    
    if (!mapRef.value) {
      console.error('Map ref not found')
      isInitializing = false
      return
    }
    
    const mapOptions = {
      center: { lat: props.latitude, lng: props.longitude },
      zoom: props.zoom,
      mapTypeControl: false,
      streetViewControl: false,
      fullscreenControl: false,
      styles: [
        {
          featureType: 'poi',
          elementType: 'labels',
          stylers: [{ visibility: 'off' }]
        }
      ]
    }
    
    console.log('Creating map with options:', mapOptions)
    map = new google.maps.Map(mapRef.value, mapOptions)
    
    if (props.showMarker) {
      marker = new google.maps.Marker({
        position: { lat: props.latitude, lng: props.longitude },
        map: map,
        title: props.markerTitle,
        animation: google.maps.Animation.DROP
      })
      console.log('Marker added to map')
    }
    
    mapLoaded.value = true
  } catch (error) {
    console.error('Error initializing Google Map:', error)
  } finally {
    isInitializing = false
  }
}

// Update map center when coordinates change
watch(() => [props.latitude, props.longitude], ([newLat, newLng]) => {
  if (map && googleMapsLoaded) {
    const newCenter = { lat: newLat, lng: newLng }
    map.setCenter(newCenter)
    
    if (marker) {
      marker.setPosition(newCenter)
    }
  }
})

onMounted(() => {
  initMap()
})

onUnmounted(() => {
  if (marker) {
    marker.setMap(null)
    marker = null
  }
  map = null
})
</script>

<style scoped>
.google-map-container {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
}

.google-map {
  width: 100%;
  height: v-bind(height);
  background-color: #f5f5f5;
  position: relative;
}

.map-loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #999;
}

.map-loading span {
  font-size: 14px;
}
</style>