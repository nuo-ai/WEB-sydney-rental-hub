<script setup lang="ts">
import { Card, CardContent, CardHeader } from './card'
import Avatar from './Avatar.vue'
import Button from './Button.vue'

defineProps({
  agent: {
    type: Object,
    default: () => ({
      name: 'John Doe',
      agency: 'Real Estate Agency',
      avatarUrl: 'https://i.pravatar.cc/150?u=a042581f4e29026024d',
    }),
  },
});
</script>

<template>
  <Card>
    <CardHeader class="items-center">
      <Avatar
        :src="agent.avatarUrl"
        :fallback="agent.name.charAt(0)"
        class="h-24 w-24"
      />
    </CardHeader>
    <CardContent class="text-center">
      <p class="font-semibold">{{ agent.name }}</p>
      <p class="text-sm text-muted-foreground">{{ agent.agency }}</p>
      <div class="mt-4 flex flex-col space-y-2">
        <Button>Request a tour</Button>
        <Button variant="outline">Send a message</Button>
      </div>
    </CardContent>
  </Card>
</template>
