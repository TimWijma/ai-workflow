<template>
  <BaseNode title="API Call" icon="pi pi-globe" node-class="api-node">
    <InputText
      v-model="localApiUrl"
      placeholder="API URL"
      class="node-input"
      readonly
      @update:modelValue="onUrlChange"
    />
  </BaseNode>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useFlowStore } from '@/stores/useFlowStore'
import InputText from 'primevue/inputtext'
import BaseNode from './BaseNode.vue'
import type { Step } from '@/types'

interface Props {
  nodeData: {
    step: Step
    config: any
  }
  nodeId: string
}

const props = defineProps<Props>()
const flowStore = useFlowStore()

const localApiUrl = ref(props.nodeData.config?.apiUrl || '')

// Watch for external changes to the step
watch(
  () => props.nodeData.config?.apiUrl,
  (newUrl) => {
    if (newUrl !== localApiUrl.value) {
      localApiUrl.value = newUrl || ''
    }
  },
)

const onUrlChange = (newUrl: string | undefined) => {
  // Just update local state, don't save to backend
  // The dialog will handle saving when user clicks "Save"
}
</script>

<style scoped>
/* Additional API-specific styling can go here if needed */
</style>
