<script setup lang="ts">
import { Card, CardContent, CardHeader, CardTitle } from './card'

defineProps({
  description: {
    type: String,
    default: '',
  },
});
</script>

<template>
  <Card>
    <CardHeader>
      <CardTitle>About this property</CardTitle>
    </CardHeader>
    <CardContent>
      <p class="text-muted-foreground">
        {{ description }}
      </p>
    </CardContent>
  </Card>
</template>
