<template>
  <div class="flow-sidebar">
    <div class="sidebar-header">
      <h3>Tools</h3>
      <Button
        icon="pi pi-save"
        label="Save Flow"
        :loading="flowStore.loading"
        :disabled="!flowStore.dirty"
        @click="saveFlow"
        class="save-button"
      />
    </div>

    <Accordion :activeIndex="0" class="sidebar-accordion">
      <AccordionTab header="Steps">
        <div class="step-palette">
          <div
            class="palette-item api-item"
            draggable="true"
            @dragstart="startDrag($event, 'api_call')"
            @click="addStep('api_call')"
          >
            <i class="pi pi-globe"></i>
            <span>API Call</span>
          </div>

          <div
            class="palette-item llm-item"
            draggable="true"
            @dragstart="startDrag($event, 'llm_call')"
            @click="addStep('llm_call')"
          >
            <i class="pi pi-brain"></i>
            <span>LLM Call</span>
          </div>
        </div>
      </AccordionTab>

      <AccordionTab header="Flow Info">
        <div class="flow-info">
          <div class="info-item">
            <label>Flow ID:</label>
            <span>{{ flowStore.flowId || 'None' }}</span>
          </div>
          <div class="info-item">
            <label>Steps:</label>
            <span>{{ flowStore.steps.length }}</span>
          </div>
          <div class="info-item">
            <label>Connections:</label>
            <span>{{ flowStore.stepConnections.length }}</span>
          </div>
          <div class="info-item">
            <label>Status:</label>
            <Tag
              :value="flowStore.dirty ? 'Modified' : 'Saved'"
              :severity="flowStore.dirty ? 'warning' : 'success'"
            />
          </div>
        </div>
      </AccordionTab>
    </Accordion>

    <!-- Error Display -->
    <Message
      v-if="flowStore.error"
      severity="error"
      :closable="true"
      @close="flowStore.clearError"
      class="sidebar-error"
    >
      {{ flowStore.error }}
    </Message>
  </div>
</template>

<script setup lang="ts">
import { useFlowStore } from '@/stores/useFlowStore'
import type { StepCreate } from '@/types'
import Accordion from 'primevue/accordion'
import AccordionTab from 'primevue/accordiontab'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import Message from 'primevue/message'

const flowStore = useFlowStore()

const saveFlow = async () => {
  await flowStore.saveFlow()
}

const addStep = async (type: 'api_call' | 'llm_call') => {
  if (!flowStore.flowId) return

  const stepData: StepCreate = {
    flow_id: flowStore.flowId,
    type,
    pos_x: Math.random() * 400 + 100, // Random position
    pos_y: Math.random() * 300 + 100,
    config: type === 'api_call' ? { apiUrl: '' } : { prompt: '' },
  }

  await flowStore.addStep(stepData)
}

const startDrag = (event: DragEvent, stepType: 'api_call' | 'llm_call') => {
  if (event.dataTransfer) {
    event.dataTransfer.setData(
      'application/vueflow',
      JSON.stringify({
        type: stepType,
      }),
    )
    event.dataTransfer.effectAllowed = 'move'
  }
}
</script>

<style scoped>
.flow-sidebar {
  width: 300px;
  background: var(--p-surface-0);
  border-left: 1px solid var(--p-surface-border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-header {
  padding: 1rem;
  border-bottom: 1px solid var(--p-surface-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
}

.save-button {
  font-size: 0.875rem;
}

.sidebar-accordion {
  flex: 1;
  overflow-y: auto;
}

.step-palette {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.palette-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
  border: 2px dashed var(--p-surface-border);
  border-radius: 6px;
  cursor: move;
  transition: all 0.2s ease;
  background: var(--p-surface-50);
}

.palette-item:hover {
  background: var(--p-surface-100);
  border-color: var(--p-primary-color);
}

.api-item:hover {
  border-color: #3b82f6;
}

.llm-item:hover {
  border-color: #8b5cf6;
}

.palette-item i {
  font-size: 1.2rem;
}

.flow-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-item label {
  font-weight: 600;
  color: var(--p-text-color-secondary);
}

.sidebar-error {
  margin: 1rem;
}
</style>
