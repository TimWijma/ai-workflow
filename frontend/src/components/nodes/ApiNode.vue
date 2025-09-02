<template>
  <BaseNodeEdit
    :visible="visible"
    :step="step"
    @update:visible="$emit('update:visible', $event)"
    @save="handleBaseSave"
    @cancel="$emit('cancel')"
    @delete="$emit('delete')"
  >
    <div class="field">
      <label for="apiUrl">API URL</label>
      <InputText
        id="apiUrl"
        v-model="editForm.apiUrl"
        placeholder="https://api.example.com/endpoint"
      />
    </div>

    <div class="field">
      <label for="method">HTTP Method</label>
      <Select id="method" v-model="editForm.method" :options="httpMethods" />
    </div>

    <div class="field">
      <label for="requestBody">Request Body (JSON)</label>
      <Textarea id="requestBody" v-model="editForm.data" placeholder='{"key": "value"}' rows="4" />
    </div>
  </BaseNodeEdit>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import BaseNodeEdit from './BaseNode.vue'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Select from 'primevue/select'
import type { Step } from '@/types'
import { StepType, type ApiNodeConfig } from '@/types/Step'

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
  type: StepType.API_CALL,
  apiUrl: '',
  method: 'GET',
  data: '',
})

const httpMethods = ['GET', 'POST', 'PUT', 'DELETE']

watch(
  () => props.step,
  (newStep) => {
    if (newStep) {
      const config = newStep.config as ApiNodeConfig
      editForm.value = {
        type: newStep.type,
        apiUrl: config.apiUrl || '',
        method: config.method || 'GET',
        data: config.data ? JSON.stringify(config.data, null, 2) : '',
      }
    }
  },
  { immediate: true },
)

const handleBaseSave = (commonData: { is_start: boolean; variables: string[] }) => {
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
    is_start: commonData.is_start,
    variables: commonData.variables,
  })
}
</script>
