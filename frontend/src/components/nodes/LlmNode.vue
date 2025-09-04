<template>
  <BaseNode
    :visible="visible"
    title="Edit LLM Call"
    :step="step"
    @update:visible="$emit('update:visible', $event)"
    @save="handleBaseSave"
    @cancel="$emit('cancel')"
    @delete="$emit('delete')"
  >
    <div class="field">
      <label for="prompt">Prompt</label>
      <Textarea
        id="prompt"
        v-model="editForm.config.prompt"
        placeholder="Enter your LLM prompt here..."
        rows="6"
        class="w-full"
      />
    </div>

    <div class="field">
      <label for="model">Model (Optional)</label>
      <InputText
        id="model"
        v-model="editForm.config.model"
        placeholder="gpt-4, claude-3, etc."
        class="w-full"
      />
    </div>

    <div class="field">
      <label for="temperature">Temperature (Optional)</label>
      <InputNumber
        id="temperature"
        v-model="editForm.config.temperature"
        placeholder="0.0 - 1.0"
        :min="0"
        :max="1"
        :step="0.1"
        class="w-full"
      />
    </div>
  </BaseNode>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import BaseNode from './BaseNode.vue'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Textarea from 'primevue/textarea'
import type { Step } from '@/types'
import { StepType, type LlmNodeConfig } from '@/types/Step'

interface Props {
  visible: boolean
  step: Step | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:visible': [value: boolean]
  save: [data: any]
  cancel: []
  delete: []
}>()

const editForm = ref({
  type: StepType.LLM_CALL,
  config: {
    prompt: '',
    model: '',
    temperature: undefined,
  } as LlmNodeConfig,
})

watch(
  () => props.step,
  (newStep) => {
    if (newStep) {
      const newConfig = newStep.config as LlmNodeConfig
      editForm.value = {
        type: newStep.type,
        config: newConfig,
      }
    }
  },
  { immediate: true },
)

const handleBaseSave = (commonData: { name: string; is_start: boolean; variables: string[] }) => {
  emit('save', {
    name: commonData.name,
    type: editForm.value.type,
    config: editForm.value.config,
    is_start: commonData.is_start,
    variables: commonData.variables,
  })
}
</script>

<style scoped>
.w-full {
  width: 100%;
}
</style>
