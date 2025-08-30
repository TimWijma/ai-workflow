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
      <Select id="method" v-model="editForm.method" :options="httpMethods" class="w-full" />
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
    <div class="field">
      <label for="isStart">Is Start Step</label>
      <ToggleSwitch v-model="editForm.is_start" />
    </div>

    <div class="field">
      <label for="variables">Variables</label>
      <div class="variable-input">
        <InputText type="text" v-model="tempVariable" />
        <Button icon="pi pi-plus" @click="addVariable">Add</Button>
      </div>
      <div class="variable-chips">
        <Chip
          v-for="name in editForm.variables"
          :key="name"
          :label="name"
          removable
          @remove="removeVariable(name)"
        />
      </div>
    </div>
  </BaseNodeEdit>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import BaseNodeEdit from './BaseNodeEdit.vue'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Select from 'primevue/select'
import Chip from 'primevue/chip'
import Button from 'primevue/button'
import { ToggleSwitch } from 'primevue'
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
  is_start: false,
  variables: [] as string[],
})

const tempVariable = ref('')

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
        is_start: newStep.is_start || false,
        variables: newStep.variables || [],
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
    is_start: editForm.value.is_start,
    variables: editForm.value.variables,
  })
}

const addVariable = () => {
  if (!tempVariable.value) return
  if (editForm.value.variables.includes(tempVariable.value)) {
    tempVariable.value = ''
    return
  }

  editForm.value.variables.push(tempVariable.value)
  tempVariable.value = ''
}

const removeVariable = (name: string) => {
  console.log('Removing variable:', name)

  if (editForm.value.variables) {
    editForm.value.variables = editForm.value.variables.filter((varName) => varName !== name)
  }
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
