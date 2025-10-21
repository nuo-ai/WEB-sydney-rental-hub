<script setup lang="ts">
import { ref } from 'vue'
import { Calendar } from '@sydney-rental-hub/ui/src/components/ui/calendar/index'

const selectedDate = ref<Date | undefined>(new Date())
</script>

<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">Calendar Test</h2>
    <Calendar v-model="selectedDate" />
    <p class="mt-4">Selected date: {{ selectedDate }}</p>
  </div>
</template>
