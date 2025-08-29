<template>
  <div class="api-node">
    <div class="node-header">
      <i class="pi pi-globe"></i>
      <span>API Call</span>
    </div>
    <div class="node-content">
      <InputText
        v-model="localApiUrl"
        placeholder="API URL"
        class="node-input"
        @update:modelValue="onUrlChange"
      />
    </div>
    <Handle type="target" :position="Position.Top" />
    <Handle type="source" :position="Position.Bottom" />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { Handle, Position } from '@vue-flow/core'
import { useFlowStore } from '@/stores/useFlowStore'
import InputText from 'primevue/inputtext'
import type { Step } from '@/types'

interface Props {
  nodeData: {
    step: Step
    config: any
  }
  nodeId: string
}

const props = defineProps<Props>()
const flowStore = useFlowStore()

const localApiUrl = ref(props.nodeData.config?.apiUrl || '')

// Watch for external changes to the step
watch(
  () => props.nodeData.config?.apiUrl,
  (newUrl) => {
    if (newUrl !== localApiUrl.value) {
      localApiUrl.value = newUrl || ''
    }
  },
)

const onUrlChange = (newUrl: string | undefined) => {
  // Just update local state, don't save to backend
  // The dialog will handle saving when user clicks "Save"
}
</script>

<style scoped>
.api-node {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  padding: 12px;
  min-width: 200px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.api-node:hover {
  border-color: #3b82f6;
}

.node-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-weight: 600;
  color: #374151;
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
