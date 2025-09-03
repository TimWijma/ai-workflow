<template>
  <BaseNode title="API Call" icon="pi pi-globe" node-class="api-node">
    <InputText v-model="localApiUrl" placeholder="API URL" class="node-input" disabled />
    <Select
      v-model="localMethod"
      :options="['GET', 'POST', 'PUT', 'DELETE']"
      placeholder="HTTP Method"
      class="node-select"
      disabled
    />
    <InputText v-model="localData" placeholder="Request Body (JSON)" class="node-input" disabled />
  </BaseNode>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import BaseNode from './BaseNodeFlow.vue'
import type { Step } from '@/types'
import type { ApiNodeConfig } from '@/types/Step'

interface Props {
  nodeData: {
    step: Step
    config: ApiNodeConfig
  }
  nodeId: string
}

const props = defineProps<Props>()

const localApiUrl = ref(props.nodeData.config?.apiUrl || '')
const localMethod = ref(props.nodeData.config?.method || 'GET')
const localData = ref(
  props.nodeData.config?.data ? JSON.stringify(props.nodeData.config.data, null, 2) : '',
)

watch(
  () => props.nodeData.config,
  (newConfig) => {
    if (newConfig) {
      localApiUrl.value = newConfig.apiUrl || ''
      localMethod.value = newConfig.method || 'GET'
      localData.value = newConfig.data ? JSON.stringify(newConfig.data, null, 2) : ''
    }
  },
  { deep: true },
)
</script>
