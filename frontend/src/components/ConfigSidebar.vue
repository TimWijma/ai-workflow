<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from 'vue'
import { Node } from '@vue-flow/core'
import Sidebar from 'primevue/sidebar'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Button from 'primevue/button'
import { Step } from '../types/workflow';

const props = defineProps<{_selectedNode: Node<Step> | null}>();
const emit = defineEmits(['update:selectedNode', 'save']);

const selectedNode = ref<Node<Step> | null>(null);

watch(() => props._selectedNode, (newNode) => {
    selectedNode.value = newNode;
});

function save() {
    emit('save');
}

</script>

<template>
  <Sidebar :visible="selectedNode !== null" @update:visible="(value) => { if (!value) $emit('update:selectedNode', null) }" header="Configuration" position="right">
    <div v-if="selectedNode">
      <h3>{{ selectedNode.label }}</h3>
      
      <div v-if="selectedNode.type === 'api'">
        <div class="p-fluid">
          <div class="p-field">
            <label for="apiUrl">API URL</label>
            <InputText id="apiUrl" v-model="selectedNode.data.config.url" />
          </div>
        </div>
      </div>

      <div v-if="selectedNode.type === 'llm'">
        <div class="p-fluid">
          <div class="p-field">
            <label for="prompt">Prompt</label>
            <Textarea id="prompt" v-model="selectedNode.data.config.prompt" rows="5" />
          </div>
        </div>
      </div>

      <Button label="Save" @click="save" class="mt-4" />
    </div>
  </Sidebar>
</template>

<style scoped>
.p-sidebar-content {
    padding: 1rem;
}

.p-field > label {
    display: block;
    margin-bottom: 0.5rem;
}

.mt-4 {
    margin-top: 1rem;
}
</style>