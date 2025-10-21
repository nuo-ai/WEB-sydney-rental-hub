<script setup>
import { Card } from './ui/card'

// This component now acts as a simple wrapper around the shadcn-vue Card.
// For more complex layouts, developers should compose the Card components directly
// (Card, CardHeader, CardContent, etc.).
</script>

<template>
  <Card>
    <slot />
  </Card>
</template>
