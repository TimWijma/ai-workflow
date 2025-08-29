<template>
  <div class="flow-container">
    <VueFlow
      v-model:nodes="vueFlowNodes"
      v-model:edges="vueFlowEdges"
      @nodes-change="onNodesChange"
      @edges-change="onEdgesChange"
      @connect="onConnect"
      @node-click="onNodeClick"
      class="vue-flow"
      :default-viewport="{ zoom: 1 }"
    >
      <Background />
      <Controls />
      <MiniMap />

      <template #node-api_call="{ data, id }">
        <ApiNode :node-data="data" :node-id="id" />
      </template>

      <template #node-llm_call="{ data, id }">
        <LlmNode :node-data="data" :node-id="id" />
      </template>
    </VueFlow>

    <!-- Node Edit Dialog -->
    <Dialog v-model:visible="showEditDialog" modal header="Edit Step" :style="{ width: '500px' }">
      <div v-if="flowStore.selectedStep" class="edit-dialog-content">
        <div class="field">
          <label for="stepType">Step Type</label>
          <Select
            id="stepType"
            v-model="editForm.type"
            :options="stepTypes"
            optionLabel="label"
            optionValue="value"
            class="w-full"
          />
        </div>

        <div v-if="editForm.type === 'api_call'" class="field">
          <label for="apiUrl">API URL</label>
          <InputText
            id="apiUrl"
            v-model="editForm.apiUrl"
            placeholder="https://api.example.com/endpoint"
            class="w-full"
          />
        </div>

        <div v-if="editForm.type === 'llm_call'" class="field">
          <label for="prompt">Prompt</label>
          <Textarea
            id="prompt"
            v-model="editForm.prompt"
            placeholder="Enter your LLM prompt here..."
            rows="4"
            class="w-full"
          />
        </div>
      </div>

      <template #footer>
        <Button label="Delete" severity="danger" @click="removeStep" />
        <Button label="Cancel" severity="secondary" @click="closeEditDialog" />
        <Button label="Save" @click="saveEditedStep" />
      </template>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { VueFlow } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import { useFlowStore } from '@/stores/useFlowStore'
import type { Step, StepUpdate, StepConnectionCreate } from '@/types'
import Dialog from 'primevue/dialog'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Select from 'primevue/select'
import ApiNode from './nodes/ApiNode.vue'
import LlmNode from './nodes/LlmNode.vue'

const flowStore = useFlowStore()

// Dialog state
const showEditDialog = ref(false)
const editForm = ref({
  type: 'api_call' as 'api_call' | 'llm_call',
  apiUrl: '',
  prompt: '',
})

// Position update debouncing
let positionUpdateTimer: number | null = null
const pendingPositionUpdates = new Map<string, { x: number; y: number }>()

const stepTypes = [
  { label: 'API Call', value: 'api_call' },
  { label: 'LLM Call', value: 'llm_call' },
]

// Convert steps to Vue Flow nodes
const vueFlowNodes = computed(() => {
  return flowStore.steps.map((step) => ({
    id: step.id,
    type: step.type,
    position: { x: step.pos_x, y: step.pos_y },
    data: {
      step,
      config: step.config || {},
    },
  }))
})

// Convert step connections to Vue Flow edges
const vueFlowEdges = computed(() => {
  return flowStore.stepConnections.map((connection) => ({
    id: connection.id,
    source: connection.from_step_id,
    target: connection.to_step_id,
  }))
})

// Handle node position changes with debouncing
const onNodesChange = (changes: any[]) => {
  for (const change of changes) {
    if (change.type === 'position' && change.position && change.id) {
      // Store the position update in pending updates
      pendingPositionUpdates.set(change.id, {
        x: change.position.x,
        y: change.position.y,
      })

      // Clear existing timer and set a new one
      if (positionUpdateTimer) {
        clearTimeout(positionUpdateTimer)
      }

      positionUpdateTimer = setTimeout(async () => {
        // Process all pending position updates
        const updates = Array.from(pendingPositionUpdates.entries())
        pendingPositionUpdates.clear()

        for (const [stepId, position] of updates) {
          const step = flowStore.steps.find((s) => s.id === stepId)
          if (step) {
            // Send complete step data, not just position
            const updateData: StepUpdate = {
              type: step.type,
              config: step.config,
              pos_x: position.x,
              pos_y: position.y,
            }
            try {
              await flowStore.updateStep(stepId, updateData)
            } catch (error) {
              console.error('Error updating step position:', error)
            }
          }
        }
      }, 500) // 500ms debounce
    }
  }
}

// Handle edge changes
const onEdgesChange = async (changes: any[]) => {
  for (const change of changes) {
    if (change.type === 'remove') {
      const connection = flowStore.stepConnections.find((c) => c.id === change.id)
      if (connection) {
        await flowStore.removeStepConnection(connection.id)
      }
    }
  }
}

// Handle new connections
const onConnect = async (connection: any) => {
  const connectionData: StepConnectionCreate = {
    from_step_id: connection.source,
    to_step_id: connection.target,
  }
  await flowStore.addStepConnection(connectionData)
}

// Handle node clicks
const onNodeClick = (event: any) => {
  const step = flowStore.steps.find((s) => s.id === event.node.id)
  if (step) {
    flowStore.setSelectedStep(step)
    openEditDialog(step)
  }
}

// Dialog methods
const openEditDialog = (step: Step) => {
  editForm.value = {
    type: step.type,
    apiUrl: step.config?.apiUrl || '',
    prompt: step.config?.prompt || '',
  }
  showEditDialog.value = true
}

const closeEditDialog = () => {
  showEditDialog.value = false
  flowStore.setSelectedStep(null)
}

const saveEditedStep = async () => {
  if (!flowStore.selectedStep) return

  const config: any = {}
  if (editForm.value.type === 'api_call') {
    config.apiUrl = editForm.value.apiUrl
  } else if (editForm.value.type === 'llm_call') {
    config.prompt = editForm.value.prompt
  }

  const updateData: StepUpdate = {
    type: editForm.value.type,
    config,
    pos_x: flowStore.selectedStep.pos_x,
    pos_y: flowStore.selectedStep.pos_y,
  }

  try {
    await flowStore.updateStep(flowStore.selectedStep.id, updateData)
    closeEditDialog()
  } catch (error) {
    console.error('Error saving step:', error)
  }
}

const removeStep = async () => {
  if (!flowStore.selectedStep) return

  try {
    await flowStore.removeStep(flowStore.selectedStep.id)
    closeEditDialog()
  } catch (error) {
    console.error('Error deleting step:', error)
  }
}
</script>

<style scoped>
.flow-container {
  flex: 1;
  position: relative;
}

.vue-flow {
  height: 100%;
  width: 100%;
}

.edit-dialog-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
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

.w-full {
  width: 100%;
}
</style>
