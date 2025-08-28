<script setup lang="ts">
import Panel from 'primevue/panel';

function onDragStart(event: DragEvent, nodeType: string) {
  if (event.dataTransfer) {
    event.dataTransfer.setData('application/vueflow', nodeType)
    event.dataTransfer.effectAllowed = 'move'
  }
}
</script>

<template>
  <Panel header="Steps">
    <div class="p-4">
      <div class="step-item" :draggable="true" @dragstart="onDragStart($event, 'api')">Get Data from API</div>
      <div class="step-item" :draggable="true" @dragstart="onDragStart($event, 'llm')">Call LLM</div>
    </div>
  </Panel>
</template>

<style scoped>
.sidebar .p-panel-content {
  padding: 0;
}

.step-item {
  padding: 1rem;
  border: 1px solid #ccc;
  background: #f9f9f9;
  cursor: grab;
  margin-bottom: 1rem;
  text-align: center;
}
</style>