<template>
  <div class="llm-node">
    <div class="node-header">
      <i class="pi pi-brain"></i>
      <span>LLM Call</span>
    </div>
    <div class="node-content">
      <Textarea
        v-model="localPrompt"
        placeholder="Enter prompt..."
        rows="3"
        class="node-textarea"
        @update:modelValue="onPromptChange"
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
import Textarea from 'primevue/textarea'
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

const localPrompt = ref(props.nodeData.config?.prompt || '')

// Watch for external changes to the step
watch(
  () => props.nodeData.config?.prompt,
  (newPrompt) => {
    if (newPrompt !== localPrompt.value) {
      localPrompt.value = newPrompt || ''
    }
  },
)

const onPromptChange = (newPrompt: string | undefined) => {
  // Just update local state, don't save to backend
  // The dialog will handle saving when user clicks "Save"
}
</script>

<style scoped>
.llm-node {
  border-radius: 8px;
  padding: 12px;
  min-width: 200px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  color: var(--p-text-color);
  background: var(--p-content-background);
}

.llm-node:hover {
  border-color: #8b5cf6;
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

.node-textarea {
  font-size: 12px;
  resize: none;
}
</style>
