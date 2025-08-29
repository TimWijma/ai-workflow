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
    <component
      :is="currentEditComponent"
      v-model:visible="showEditDialog"
      :step="flowStore.selectedStep"
      @save="saveEditedStep"
      @cancel="closeEditDialog"
      @delete="removeStep"
    />
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
import ApiNode from './nodes/ApiNode.vue'
import LlmNode from './nodes/LlmNode.vue'
import ApiNodeEdit from './nodes/ApiNodeEdit.vue'
import LlmNodeEdit from './nodes/LlmNodeEdit.vue'

const flowStore = useFlowStore()

// Dialog state
const showEditDialog = ref(false)

// Position update debouncing
let positionUpdateTimer: number | null = null
const pendingPositionUpdates = new Map<string, { x: number; y: number }>()

// Component mapping for edit dialogs
const editComponentMap = {
  api_call: ApiNodeEdit,
  llm_call: LlmNodeEdit,
}

// Computed property to determine which edit component to show
const currentEditComponent = computed(() => {
  if (!flowStore.selectedStep) return null
  return editComponentMap[flowStore.selectedStep.type] || null
})

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
  flowStore.setSelectedStep(step)
  showEditDialog.value = true
}

const closeEditDialog = () => {
  showEditDialog.value = false
  flowStore.setSelectedStep(null)
}

const saveEditedStep = async (data: any) => {
  if (!flowStore.selectedStep) return

  const updateData: StepUpdate = {
    type: data.type,
    config: data.config,
    pos_x: flowStore.selectedStep.pos_x,
    pos_y: flowStore.selectedStep.pos_y,
  }

  try {
    await flowStore.updateStep(flowStore.selectedStep.id, updateData)

    // If the type changed, we need to close and reopen the dialog with the new component
    if (data.type !== flowStore.selectedStep.type) {
      closeEditDialog()
      // Small delay to allow the component to update
      setTimeout(() => {
        const updatedStep = flowStore.steps.find((s) => s.id === flowStore.selectedStep?.id)
        if (updatedStep) {
          openEditDialog(updatedStep)
        }
      }, 100)
    } else {
      closeEditDialog()
    }
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
</style>
