<script setup lang="ts">
import { Card, CardContent, CardHeader, CardTitle } from './card'
import Badge from './Badge.vue'

defineProps({
  highlights: {
    type: Array as () => string[],
    default: () => [],
  },
});
</script>

<template>
  <Card>
    <CardHeader>
      <CardTitle>Property Highlights</CardTitle>
    </CardHeader>
    <CardContent>
      <div class="flex flex-wrap gap-2">
        <Badge v-for="highlight in highlights" :key="highlight" variant="secondary">
          {{ highlight }}
        </Badge>
      </div>
    </CardContent>
  </Card>
</template>
