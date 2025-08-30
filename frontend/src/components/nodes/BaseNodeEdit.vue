<template>
  <Dialog
    :visible="visible"
    modal
    :header="title"
    :style="{ width: '500px' }"
    @update:visible="$emit('update:visible', $event)"
  >
    <template #header>
      <div class="edit-header">
        <span class="edit-title">{{ title }}</span>
        <div>
          <span class="edit-id">{{ step?.id }}</span>
          <Button
            icon="pi pi-copy"
            size="small"
            variant="text"
            rounded
            aria-label="Filter"
            @click="copyStepId"
          />
        </div>
      </div>
    </template>

    <div class="edit-dialog-content">
      <!-- Node-specific fields -->
      <slot />

      <!-- Common fields section -->
      <Divider />
      <h4>Common Settings</h4>

      <div class="field">
        <label for="isStart">Is Start Step</label>
        <ToggleSwitch v-model="commonFields.is_start" />
      </div>

      <div class="field">
        <label for="variables">Output Variables</label>
        <div class="variable-input">
          <InputText
            type="text"
            v-model="tempVariable"
            placeholder="Enter variable name"
            @keyup.enter="addVariable"
          />
          <Button label="Add" icon="pi pi-plus" @click="addVariable" />
        </div>
        <div class="variable-chips" v-if="commonFields.variables.length > 0">
          <Chip
            v-for="name in commonFields.variables"
            :key="name"
            :label="name"
            removable
            @remove="removeVariable(name)"
          />
        </div>
      </div>
    </div>

    <template #footer>
      <Button label="Delete" severity="danger" @click="$emit('delete')" />
      <Button label="Cancel" severity="secondary" @click="$emit('cancel')" />
      <Button label="Save" @click="handleSave" />
    </template>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import ToggleSwitch from 'primevue/toggleswitch'
import InputText from 'primevue/inputtext'
import Chip from 'primevue/chip'
import Divider from 'primevue/divider'
import type { Step } from '@/types'

interface Props {
  visible: boolean
  title: string
  step: Step | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:visible': [value: boolean]
  save: [commonData: { is_start: boolean; variables: string[] }]
  cancel: []
  delete: []
}>()

const commonFields = ref({
  is_start: false,
  variables: [] as string[],
})

const tempVariable = ref('')

watch(
  () => props.step,
  (newStep) => {
    if (newStep) {
      commonFields.value = {
        is_start: newStep.is_start || false,
        variables: newStep.variables || [],
      }
    }
  },
  { immediate: true },
)

const copyStepId = () => {
  if (props.step) {
    navigator.clipboard.writeText(props.step.id)
  }
}

const addVariable = () => {
  if (!tempVariable.value.trim()) return
  if (commonFields.value.variables.includes(tempVariable.value)) {
    tempVariable.value = ''
    return
  }

  commonFields.value.variables.push(tempVariable.value.trim())
  tempVariable.value = ''
}

const removeVariable = (name: string) => {
  commonFields.value.variables = commonFields.value.variables.filter((varName) => varName !== name)
}

const handleSave = () => {
  emit('save', {
    is_start: commonFields.value.is_start,
    variables: commonFields.value.variables,
  })
}
</script>

<style scoped>
.edit-dialog-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.edit-header {
  display: flex;
  flex-direction: column;
  font-weight: var(--p-dialog-title-font-weight);
  font-size: var(--p-dialog-title-font-size);
}

.edit-id {
  font-size: 0.8rem;
  opacity: 0.7;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.field label {
  font-weight: 600;
  color: var(--p-text-color);
}

.variable-input {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.variable-input input {
  flex: 1;
}

.variable-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

h4 {
  margin: 0;
  color: var(--p-text-color);
  font-size: 1rem;
  font-weight: 600;
}
</style>
