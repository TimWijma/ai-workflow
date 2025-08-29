<template>
  <div class="node" :class="nodeClass">
    <div class="node-header">
      <i :class="icon"></i>
      <span>{{ title }}</span>
    </div>
    <div class="node-content">
      <slot />
    </div>
    <Handle type="target" :position="Position.Top" />
    <Handle type="source" :position="Position.Bottom" />
  </div>
</template>

<script setup lang="ts">
import { Handle, Position } from '@vue-flow/core'

interface Props {
  title: string
  icon: string
  nodeClass?: string
}

defineProps<Props>()
</script>

<style scoped>
.node {
  border-radius: 8px;
  padding: 12px;
  min-width: 200px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  color: var(--p-text-color);
  background: var(--p-content-background);
  border: 2px solid var(--p-input-border-color);
}

.node-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-weight: 600;
}

.node-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.node-input {
  font-size: 12px;
}
</style>
