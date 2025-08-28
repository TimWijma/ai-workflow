<script setup lang="ts">
import { ref, onMounted, defineEmits } from 'vue'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import Listbox from 'primevue/listbox'
import { type Flow } from '../types/workflow'

const props = defineProps<{
  visible: boolean
}>()
const emit = defineEmits(['load', 'update:visible'])
const flows = ref<Flow[]>([])
const selectedFlow = ref<Flow | null>(null)

async function fetchFlows() {
  const response = await fetch('http://127.0.0.1:8000/api/v1/flows')
  flows.value = await response.json()
}

function loadFlow() {
  if (selectedFlow.value) {
    emit('load', selectedFlow.value)
  }
}

onMounted(fetchFlows)
</script>

<template>
  <Dialog
    :visible="visible"
    @update:visible="$emit('update:visible', $event)"
    header="Load Workflow"
    :modal="true"
  >
    <Listbox v-model="selectedFlow" :options="flows" optionLabel="name" />
    <template #footer>
      <Button
        label="Cancel"
        icon="pi pi-times"
        @click="$emit('update:visible', false)"
        class="p-button-text"
      />
      <Button label="Load" icon="pi pi-check" @click="loadFlow" autofocus />
    </template>
  </Dialog>
</template>
