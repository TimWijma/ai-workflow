<template>
  <div class="flow-editor">
    <FlowHeader />
    <div class="flow-content">
      <FlowFlow />
      <FlowSidebar />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useFlowStore } from '@/stores/useFlowStore'
import FlowHeader from './FlowHeader.vue'
import FlowFlow from './FlowFlow.vue'
import FlowSidebar from './FlowSidebar.vue'

const flowStore = useFlowStore()

onMounted(async () => {
  // Load available flows on component mount
  await flowStore.loadFlows()

  // If there are flows, load the first one
  if (flowStore.flows.length > 0) {
    await flowStore.loadFlow(flowStore.flows[0].id)
  }
})
</script>

<style scoped>
.flow-editor {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.flow-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}
</style>
