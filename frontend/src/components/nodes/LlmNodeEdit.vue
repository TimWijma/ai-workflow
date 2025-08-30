<template>
  <BaseNodeEdit
    :visible="visible"
    title="Edit LLM Call"
    :step="step"
    @update:visible="$emit('update:visible', $event)"
    @save="handleSave"
    @cancel="$emit('cancel')"
    @delete="$emit('delete')"
  >
    <div class="field">
      <label for="prompt">Prompt</label>
      <Textarea
        id="prompt"
        v-model="editForm.prompt"
        placeholder="Enter your LLM prompt here..."
        rows="6"
        class="w-full"
      />
    </div>

    <div class="field">
      <label for="model">Model (Optional)</label>
      <InputText
        id="model"
        v-model="editForm.model"
        placeholder="gpt-4, claude-3, etc."
        class="w-full"
      />
    </div>

    <div class="field">
      <label for="temperature">Temperature (Optional)</label>
      <InputNumber
        id="temperature"
        v-model="editForm.temperature"
        placeholder="0.0 - 1.0"
        :min="0"
        :max="1"
        :step="0.1"
        class="w-full"
      />
    </div>

    <div class="field">
      <label for="isStart">Is Start Step</label>
      <ToggleSwitch v-model="editForm.is_start" />
    </div>
  </BaseNodeEdit>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import BaseNodeEdit from './BaseNodeEdit.vue'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Textarea from 'primevue/textarea'
import ToggleSwitch from 'primevue/toggleswitch'
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
  prompt: '',
  model: '',
  temperature: null as number | null,
  is_start: false,
})

// Watch for step changes to update form
watch(
  () => props.step,
  (newStep) => {
    if (newStep) {
      const config = newStep.config as LlmNodeConfig
      editForm.value = {
        type: newStep.type,
        prompt: config.prompt || '',
        model: config.model || '',
        temperature: config.temperature || null,
        is_start: newStep.is_start || false,
      }
    }
  },
  { immediate: true },
)

const handleSave = () => {
  const config: any = {
    prompt: editForm.value.prompt,
  }

  // Only include optional fields if they have values
  if (editForm.value.model) {
    config.model = editForm.value.model
  }

  if (editForm.value.temperature !== null) {
    config.temperature = editForm.value.temperature
  }

  emit('save', {
    type: editForm.value.type,
    config,
  })
}
</script>

<style scoped>
.field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.field label {
  font-weight: 600;
  color: var(--p-text-color);
}

.w-full {
  width: 100%;
}
</style>
