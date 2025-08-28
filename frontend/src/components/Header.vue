<script setup lang="ts">
import Toolbar from 'primevue/toolbar';
import Button from 'primevue/button';

const emit = defineEmits(['save', 'load', 'run']);
</script>

<template>
  <Toolbar>
    <template #start>
      <h1>AI Workflow Builder</h1>
    </template>
    <template #end>
        <Button label="Save" icon="pi pi-save" class="mr-2" @click="$emit('save')" />
        <Button label="Load" icon="pi pi-folder-open" class="mr-2" @click="$emit('load')" />
        <Button label="Run" icon="pi pi-play" @click="$emit('run')" />
    </template>
  </Toolbar>
</template>

<style scoped>
h1 {
  font-size: 1.5rem;
}
.mr-2 {
    margin-right: 0.5rem;
}
</style>