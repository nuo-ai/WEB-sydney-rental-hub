<template>
  <div class="container mx-auto p-8 bg-gray-50 min-h-screen">
    <h1 class="text-3xl font-bold mb-8">BaseCard & Card Components Test</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <!-- Test 1: Simple BaseCard -->
      <div>
        <h2 class="text-xl font-semibold mb-4">1. Simple BaseCard</h2>
        <BaseCard class="p-6">
          This is a simple BaseCard acting as a wrapper.
        </BaseCard>
      </div>

      <!-- Test 2: Composed Card a la shadcn -->
      <div>
        <h2 class="text-xl font-semibold mb-4">2. Composed Card</h2>
        <BaseCard>
          <CardHeader>
            <CardTitle>Meeting Notes</CardTitle>
            <CardDescription>Transcript from the meeting.</CardDescription>
          </CardHeader>
          <CardContent>
            <p>Client requested dashboard redesign.</p>
          </CardContent>
          <CardFooter>
            <p>Follow-up next week.</p>
          </CardFooter>
        </BaseCard>
      </div>
      
      <!-- Test 3: Login Card from Demo -->
      <div class="md:col-span-2 lg:col-span-1">
        <h2 class="text-xl font-semibold mb-4">3. Login Form Example</h2>
        <BaseCard>
          <CardHeader>
            <CardTitle>Login</CardTitle>
            <CardDescription>Enter your email below.</CardDescription>
          </CardHeader>
          <CardContent class="space-y-4">
            <div class="space-y-2">
              <label for="email">Email</label>
              <BaseInput id="email" type="email" placeholder="m@example.com" />
            </div>
            <div class="space-y-2">
              <label for="password">Password</label>
              <BaseInput id="password" type="password" />
            </div>
          </CardContent>
          <CardFooter class="flex flex-col gap-2">
            <BaseButton class="w-full">Login</BaseButton>
            <BaseButton variant="outline" class="w-full">Login with Google</BaseButton>
          </CardFooter>
        </BaseCard>
      </div>

    </div>
  </div>
</template>

<script setup>
import { BaseCard, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@sydney-rental-hub/ui'
import { BaseButton, BaseInput } from '@sydney-rental-hub/ui'
</script>
