<template>
  <Dialog
    :visible="visible"
    modal
    :style="{ width: '90%', height: '90%' }"
    @update:visible="$emit('update:visible', $event)"
    pt:content:style="flex: 1;"
  >
    <template #header>
      <div class="edit-header">
        <!-- <span class="edit-title">{{ title }}</span> -->
        <InputText v-model="commonFields.name" class="edit-title" />
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

    <Tabs value="0">
      <TabList>
        <Tab value="0">Settings</Tab>
        <Tab value="1">Results</Tab>
      </TabList>
      <TabPanels style="height: 100%">
        <TabPanel value="0">
          <div class="edit-dialog-content">
            <slot />

            <Divider />
            <h4>Common Settings</h4>

            <div class="field">
              <label for="isStart">Is Start Step</label>
              <ToggleSwitch v-model="commonFields.is_start" />
            </div>

            <!-- <div class="field">
              <label for="variables">Input Variables</label>
              <InputText
                type="text"
                v-model="tempVariable"
                placeholder="Enter variable name"
                @keyup.enter="addVariable"
              />
              <div class="variable-chips" v-if="commonFields.variables.length > 0">
                <Chip
                  v-for="name in commonFields.variables"
            </div> -->

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
        </TabPanel>
        <TabPanel value="1">
          <p>Results configuration coming soon...</p>
        </TabPanel>
      </TabPanels>
    </Tabs>

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
import Tabs from 'primevue/tabs'
import TabList from 'primevue/tablist'
import Tab from 'primevue/tab'
import TabPanels from 'primevue/tabpanels'
import TabPanel from 'primevue/tabpanel'

import type { Step } from '@/types'

interface Props {
  visible: boolean
  step: Step | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:visible': [value: boolean]
  save: [commonData: { name: string; is_start: boolean; variables: string[] }]
  cancel: []
  delete: []
}>()

const commonFields = ref({
  name: 'New Step',
  is_start: false,
  variables: [] as string[],
})

const tempVariable = ref('')

watch(
  () => props.step,
  (newStep) => {
    if (newStep) {
      commonFields.value = {
        name: newStep.name || 'New Step',
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
    name: commonFields.value.name,
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
