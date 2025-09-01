<template>
  <BaseNode title="LLM Call" icon="pi pi-brain" node-class="llm-node">
    <Textarea
      v-model="localPrompt"
      placeholder="Enter prompt..."
      rows="3"
      class="node-input"
      disabled
      @update:modelValue="onPromptChange"
    />
    <InputText
      v-if="localModel"
      v-model="localModel"
      placeholder="Model"
      class="node-input"
      disabled
    />
    <InputText
      v-if="localTemperature !== null"
      :model-value="`Temperature: ${localTemperature}`"
      class="node-input"
      disabled
    />
  </BaseNode>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useFlowStore } from '@/stores/useFlowStore'
import Textarea from 'primevue/textarea'
import InputText from 'primevue/inputtext'
import BaseNode from './BaseNodeFlow.vue'
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
const localModel = ref(props.nodeData.config?.model || '')
const localTemperature = ref(props.nodeData.config?.temperature || null)

// Watch for external changes to the step
watch(
  () => props.nodeData.config,
  (newConfig) => {
    if (newConfig) {
      localPrompt.value = newConfig.prompt || ''
      localModel.value = newConfig.model || ''
      localTemperature.value = newConfig.temperature || null
    }
  },
  { deep: true },
)

const onPromptChange = (newPrompt: string | undefined) => {
  // Just update local state, don't save to backend
  // The dialog will handle saving when user clicks "Save"
}
</script>

<style scoped>
/* Additional LLM-specific styling can go here if needed */
.node-input {
  resize: none;
}
</style>
