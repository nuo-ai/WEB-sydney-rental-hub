<template>
  <div class="p-10 space-y-4">
    <h1 class="text-2xl font-bold">BaseBadge Test View</h1>

    <div>
      <h2 class="text-lg font-semibold mb-2">Standard Badges</h2>
      <div class="flex items-center space-x-4">
        <BaseBadge variant="brand">Brand</BaseBadge>
        <BaseBadge variant="neutral">Neutral</BaseBadge>
        <BaseBadge variant="success">Success</BaseBadge>
        <BaseBadge variant="warning">Warning</BaseBadge>
        <BaseBadge variant="danger">Danger</BaseBadge>
        <BaseBadge variant="info">Info</BaseBadge>
      </div>
    </div>

    <div>
      <h2 class="text-lg font-semibold mb-2">Pill Badges (default)</h2>
      <div class="flex items-center space-x-4">
        <BaseBadge variant="brand" :pill="true">Brand</BaseBadge>
        <BaseBadge variant="neutral" :pill="true">Neutral</BaseBadge>
        <BaseBadge variant="success" :pill="true">Success</BaseBadge>
      </div>
    </div>

    <div>
      <h2 class="text-lg font-semibold mb-2">Square Badges</h2>
      <div class="flex items-center space-x-4">
        <BaseBadge variant="brand" :pill="false">Brand</BaseBadge>
        <BaseBadge variant="neutral" :pill="false">Neutral</BaseBadge>
        <BaseBadge variant="danger" :pill="false">Danger</BaseBadge>
      </div>
    </div>
  </div>
</template>

<script setup>
import { BaseBadge } from '@sydney-rental-hub/ui'
</script>
