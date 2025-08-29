<template>
  <BaseNodeEdit
    :visible="visible"
    title="Edit API Call"
    :step="step"
    @update:visible="$emit('update:visible', $event)"
    @save="handleSave"
    @cancel="$emit('cancel')"
    @delete="$emit('delete')"
  >
    <div class="field">
      <label for="apiUrl">API URL</label>
      <InputText
        id="apiUrl"
        v-model="editForm.apiUrl"
        placeholder="https://api.example.com/endpoint"
        class="w-full"
      />
    </div>

    <div class="field">
      <label for="method">HTTP Method</label>
      <Select
        id="method"
        v-model="editForm.method"
        :options="httpMethods"
        optionLabel="label"
        optionValue="value"
        class="w-full"
      />
    </div>

    <div class="field">
      <label for="requestBody">Request Body (JSON)</label>
      <Textarea
        id="requestBody"
        v-model="editForm.data"
        placeholder='{"key": "value"}'
        rows="4"
        class="w-full"
      />
    </div>
  </BaseNodeEdit>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import BaseNodeEdit from './BaseNodeEdit.vue'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Select from 'primevue/select'
import type { Step } from '@/types'

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
  type: 'api_call' as 'api_call' | 'llm_call',
  apiUrl: '',
  method: 'GET',
  data: '',
})

const stepTypes = [
  { label: 'API Call', value: 'api_call' },
  { label: 'LLM Call', value: 'llm_call' },
]

const httpMethods = [
  { label: 'GET', value: 'GET' },
  { label: 'POST', value: 'POST' },
  { label: 'PUT', value: 'PUT' },
  { label: 'DELETE', value: 'DELETE' },
]

// Watch for step changes to update form
watch(
  () => props.step,
  (newStep) => {
    if (newStep) {
      editForm.value = {
        type: newStep.type,
        apiUrl: newStep.config?.apiUrl || '',
        method: newStep.config?.method || 'GET',
        data: newStep.config?.data ? JSON.stringify(newStep.config.data, null, 2) : '',
      }
    }
  },
  { immediate: true },
)

const handleSave = () => {
  let parsedData = null

  // Try to parse JSON data if provided
  if (editForm.value.data.trim()) {
    try {
      parsedData = JSON.parse(editForm.value.data)
    } catch (error) {
      alert('Invalid JSON in Request Body')
      return
    }
  }

  const config = {
    apiUrl: editForm.value.apiUrl,
    method: editForm.value.method,
    data: parsedData,
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
