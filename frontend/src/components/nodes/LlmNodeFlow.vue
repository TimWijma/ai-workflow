<template>
  <BaseNode title="LLM Call" icon="pi pi-brain" node-class="llm-node">
    <Textarea
      v-model="localConfig.prompt"
      placeholder="Enter prompt..."
      rows="3"
      class="node-input"
      disabled
    />
    <InputText
      v-if="localConfig.model"
      v-model="localConfig.model"
      placeholder="Model"
      class="node-input"
      disabled
    />
    <InputText
      v-if="localConfig.temperature !== undefined"
      :model-value="`Temperature: ${localConfig.temperature}`"
      class="node-input"
      disabled
    />
  </BaseNode>
</template>

<script setup lang="ts">
import { ref, watch, type Ref } from 'vue'
import Textarea from 'primevue/textarea'
import InputText from 'primevue/inputtext'
import BaseNode from './BaseNodeFlow.vue'
import type { Step } from '@/types'
import type { LlmNodeConfig } from '@/types/Step'

interface Props {
  nodeData: {
    step: Step
    config: any
  }
  nodeId: string
}

const props = defineProps<Props>()

const localConfig: Ref<LlmNodeConfig> = ref(
  props.nodeData.config || {
    prompt: '',
    model: '',
    temperature: undefined as number | undefined,
  },
)

watch(
  () => props.nodeData.config,
  (newConfig) => {
    if (newConfig) {
      localConfig.value = newConfig
    }
  },
  { deep: true },
)
</script>

<style scoped>
.node-input {
  resize: none;
}
</style>
