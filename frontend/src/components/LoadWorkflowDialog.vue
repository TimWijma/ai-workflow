<script setup lang="ts">
import { ref, onMounted, defineEmits } from 'vue';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import Listbox from 'primevue/listbox';
import { Flow } from '../types/workflow';

const emit = defineEmits(['load']);
const flows = ref<Flow[]>([]);
const selectedFlow = ref<Flow | null>(null);

async function fetchFlows() {
  const response = await fetch('/api/v1/flows');
  flows.value = await response.json();
}

function loadFlow() {
  if (selectedFlow.value) {
    emit('load', selectedFlow.value);
  }
}

onMounted(fetchFlows);

</script>

<template>
  <Dialog header="Load Workflow" :modal="true" :visible="true">
    <Listbox v-model="selectedFlow" :options="flows" optionLabel="name" />
    <template #footer>
      <Button label="Cancel" icon="pi pi-times" @click="$emit('close')" class="p-button-text"/>
      <Button label="Load" icon="pi pi-check" @click="loadFlow" autofocus />
    </template>
  </Dialog>
</template>
