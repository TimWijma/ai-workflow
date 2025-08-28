<script setup lang="ts">
import { ref } from 'vue'
import { type Node } from '@vue-flow/core'
import Header from './components/Header.vue'
import StepSidebar from './components/StepSidebar.vue'
import WorkflowEditor from './components/WorkflowEditor.vue'
import ConfigSidebar from './components/ConfigSidebar.vue'
import LoadWorkflowDialog from './components/LoadWorkflowDialog.vue'
import SaveWorkflowDialog from './components/SaveWorkflowDialog.vue'
import RunResultDialog from './components/RunResultDialog.vue'
import Splitter from 'primevue/splitter'
import SplitterPanel from 'primevue/splitterpanel'
import { type Flow } from './types/workflow'

const selectedNode = ref<Node | null>(null)
const workflowEditor = ref<InstanceType<typeof WorkflowEditor> | null>(null)
const isLoadDialogVisible = ref(false)
const isSaveDialogVisible = ref(false)
const isRunResultDialogVisible = ref(false)
const runResult = ref<any>(null)

function handleNodeSelected(node: Node) {
  selectedNode.value = node
}

function saveConfig() {
  selectedNode.value = null
}

function newWorkflow() {
  if (workflowEditor.value) {
    workflowEditor.value.setFlow({ name: '', description: '', steps: [], connections: [] })
  }
}

async function saveWorkflow(payload: { name: string; description: string }) {
  if (workflowEditor.value) {
    const flow: Flow = workflowEditor.value.getFlow()
    flow.name = payload.name
    flow.description = payload.description

    const response = await fetch('http://127.0.0.1:8000/api/v1/flows', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(flow),
    })
    const data = await response.json()
    console.log('Workflow saved:', data)
    isSaveDialogVisible.value = false
  }
}

function showLoadDialog() {
  isLoadDialogVisible.value = true
}

function closeLoadDialog() {
  isLoadDialogVisible.value = false
}

function loadWorkflow(flow: Flow) {
  if (workflowEditor.value) {
    workflowEditor.value.setFlow(flow)
  }
  isLoadDialogVisible.value = false
}

async function runWorkflow() {
  if (workflowEditor.value) {
    const flow = workflowEditor.value.getFlow()
    if (flow.id) {
      const response = await fetch(`http://127.0.0.1:8000/api/v1/flows/${flow.id}/run`, {
        method: 'POST',
      })
      const data = await response.json()
      runResult.value = data
      isRunResultDialogVisible.value = true
    }
  }
}

function closeRunResultDialog() {
  isRunResultDialogVisible.value = false
}
</script>

<template>
  <div class="app-container">
    <Header
      @new="newWorkflow"
      @save="isSaveDialogVisible = true"
      @load="isLoadDialogVisible = true"
      @run="runWorkflow"
    />
    <Splitter style="height: calc(100vh - 5rem)">
      <SplitterPanel :size="20">
        <StepSidebar />
      </SplitterPanel>
      <SplitterPanel :size="80">
        <WorkflowEditor ref="workflowEditor" @node:selected="handleNodeSelected" />
      </SplitterPanel>
    </Splitter>
    <ConfigSidebar
      :_selectedNode="selectedNode"
      @update:selectedNode="selectedNode = $event"
      @save="saveConfig"
    />
    <LoadWorkflowDialog v-model:visible="isLoadDialogVisible" @load="loadWorkflow" />
    <SaveWorkflowDialog v-model:visible="isSaveDialogVisible" @save="saveWorkflow" />
    <RunResultDialog
      v-if="isRunResultDialogVisible"
      :result="runResult"
      @close="closeRunResultDialog"
    />
  </div>
</template>

<style>
html,
body {
  margin: 0;
  height: 100%;
  font-family:
    -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif,
    'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol';
}

.app-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
