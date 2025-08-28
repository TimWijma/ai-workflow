<script setup lang="ts">
import { defineProps } from 'vue';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';

const props = defineProps<{result: any}>();

</script>

<template>
  <Dialog header="Workflow Result" :modal="true" :visible="true">
    <pre>{{ props.result }}</pre>
    <template #footer>
      <Button label="Close" icon="pi pi-times" @click="$emit('close')" class="p-button-text"/>
    </template>
  </Dialog>
</template>
