<script setup lang="ts">
import CalendarTest from '@/components/CalendarTest.vue'
import RangeCalendarTest from '@/components/RangeCalendarTest.vue'
</script>

<template>
  <div class="p-4 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Calendar Components Showcase</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-2xl font-semibold mb-4">Single Date Selection</h2>
        <CalendarTest />
      </div>
      
      <div class="bg-white rounded-lg shadow p-6">
        <h2 class="text-2xl font-semibold mb-4">Range Date Selection</h2>
        <RangeCalendarTest />
      </div>
    </div>
    
    <div class="mt-8 bg-blue-50 rounded-lg p-6">
      <h2 class="text-xl font-semibold mb-3">Usage Notes</h2>
      <ul class="list-disc pl-5 space-y-2">
        <li>Calendar components are built using shadcn-vue patterns</li>
        <li>Supports both single date and range selection</li>
        <li>Fully accessible with keyboard navigation</li>
        <li>Responsive design works on all screen sizes</li>
        <li>Integrated with Vue 3 Composition API</li>
      </ul>
    </div>
  </div>
</template>
