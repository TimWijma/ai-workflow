<template>
  <div class="flow-header">
    <div class="flow-header-left">
      <InputText
        v-model="localFlowName"
        placeholder="Flow Name"
        class="flow-name-input"
        :class="{ 'p-invalid': !localFlowName.trim() }"
        @update:modelValue="onFlowNameChange"
      />
    </div>

    <div class="flow-header-center">
      <Select
        v-model="selectedFlowId"
        :options="flowStore.flows"
        optionLabel="name"
        optionValue="id"
        placeholder="Select a Flow"
        class="flow-selector"
        @update:modelValue="onFlowChange"
      />
    </div>

    <div class="flow-header-right">
      <Button icon="pi pi-cog" severity="secondary" text @click="showSettings" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { useFlowStore } from '@/stores/useFlowStore'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import Button from 'primevue/button'

const flowStore = useFlowStore()

// Local state for the flow name input
const localFlowName = ref('')
const selectedFlowId = ref<string | null>(null)
let debounceTimer: number | null = null

// Watch for changes in the store's flow name
watch(
  () => flowStore.flowName,
  (newName) => {
    if (newName !== localFlowName.value) {
      localFlowName.value = newName
    }
  },
  { immediate: true },
)

// Watch for changes in the store's flow ID
watch(
  () => flowStore.flowId,
  (newId) => {
    if (newId !== selectedFlowId.value) {
      selectedFlowId.value = newId
    }
  },
  { immediate: true },
)

const onFlowNameChange = (newName: string | undefined) => {
  if (newName === undefined) return

  flowStore.flowName = newName
  flowStore.markDirty()

  // Debounced save
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }

  debounceTimer = setTimeout(async () => {
    if (!newName.trim()) return

    if (flowStore.flowId) {
      await flowStore.saveFlow()
    } else {
      await flowStore.createFlow({
        name: newName,
      })
      selectedFlowId.value = flowStore.flowId
      localFlowName.value = newName
    }
  }, 1000) // 1 second debounce
}

const onFlowChange = async (flowId: string) => {
  if (flowId && flowId !== flowStore.flowId) {
    await flowStore.loadFlow(flowId)
  }
}

const showSettings = () => {
  // TODO: Implement settings dialog
  console.log('Settings clicked')
}
</script>

<style scoped>
.flow-header {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid var(--p-surface-border);
  gap: 1rem;
}

.flow-header-left,
.flow-header-center,
.flow-header-right {
  display: flex;
  align-items: center;
}

.flow-header-left {
  flex: 1;
}

.flow-header-center {
  flex: 1;
  justify-content: center;
}

.flow-header-right {
  flex: 1;
  justify-content: flex-end;
}

.flow-name-input {
  width: 100%;
  max-width: 300px;
}

.flow-selector {
  min-width: 200px;
}
</style>
