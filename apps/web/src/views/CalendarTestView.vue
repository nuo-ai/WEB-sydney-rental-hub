<script setup>
import { ref } from 'vue'
import { Calendar } from '@sydney-rental-hub/ui/src/components/ui/calendar/index'

const selectedDate = ref(new Date())
</script>

<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">Calendar Component Test</h1>
    <Calendar v-model="selectedDate" />
    <p class="mt-4">Selected Date: {{ selectedDate }}</p>
  </div>
</template>
