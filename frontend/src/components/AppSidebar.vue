<template>
  <div class="sidebar">
    <Button
      icon="pi pi-sitemap"
      severity="secondary"
      text
      @click="flowStore.setCurrentPage('editor')"
    />
    <Button
      icon="pi pi-cog"
      severity="secondary"
      text
      @click="flowStore.setCurrentPage('settings')"
    />
  </div>
</template>

<script setup lang="ts">
import { useFlowStore } from '@/stores/useFlowStore'
import { Button } from 'primevue'

const flowStore = useFlowStore()
</script>

<style scoped>
.sidebar {
  height: 100%;
  padding: 0.5rem;

  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
</style>
