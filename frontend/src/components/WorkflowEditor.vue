<script setup lang="ts">
import { ref, defineExpose } from 'vue'
import { VueFlow, useVueFlow, type Node, type Edge } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import { type Step, type Flow } from '../types/workflow'

const {
  onConnect,
  addEdges,
  addNodes,
  project,
  onNodeClick,
  getNodes,
  getEdges,
  setNodes,
  setEdges,
} = useVueFlow()

const elements = ref<(Node | Edge)[]>([])

const emit = defineEmits(['node:selected'])

onConnect((params) => addEdges([params]))

let nodeId = 0
function onDragOver(event: DragEvent) {
  event.preventDefault()
  if (event.dataTransfer) {
    event.dataTransfer.dropEffect = 'move'
  }
}

function onDrop(event: DragEvent) {
  const type = event.dataTransfer?.getData('application/vueflow')
  if (!type) return

  const { x, y } = project({ x: event.clientX, y: event.clientY - 50 })
  const id = nodeId++
  const newNode: Node<Step> = {
    id: `node-${id}`,
    type,
    label: `${type} node`,
    position: { x, y },
    data: { id, type, label: `${type} node`, config: {}, pos_x: x, pos_y: y },
  }
  addNodes([newNode])
}

onNodeClick((event) => {
  emit('node:selected', event.node)
})

function getFlow(): Flow {
  const nodes = getNodes.value
  const edges = getEdges.value

  const flow: Flow = {
    name: 'My Workflow',
    description: 'A sample workflow',
    steps: nodes.map((node) => node.data),
    connections: edges.map((edge) => {
      const sourceNode = getNodes.value.find((n) => n.id === edge.source)
      const targetNode = getNodes.value.find((n) => n.id === edge.target)
      if (!sourceNode || !targetNode) {
        throw new Error('Invalid connection')
      }
      return {
        from_step_id: sourceNode.data.id,
        to_step_id: targetNode.data.id,
      }
    }),
  }

  return flow
}

function setFlow(flow: Flow) {
  const nodes: Node<Step>[] = flow.steps.map((step) => ({
    id: `node-${step.id}`,
    type: step.type,
    label: step.label,
    position: { x: step.pos_x, y: step.pos_y },
    data: step,
  }))

  const edges: Edge[] = flow.connections.map((conn) => ({
    id: `edge-${conn.id}`,
    source: `node-${conn.from_step_id}`,
    target: `node-${conn.to_step_id}`,
  }))

  setNodes(nodes)
  setEdges(edges)
}

defineExpose({
  getFlow,
  setFlow,
})
</script>

<template>
  <div style="height: 100%" @dragover="onDragOver" @drop="onDrop">
    <VueFlow v-model="elements">
      <Background />
      <MiniMap />
      <Controls />
    </VueFlow>
  </div>
</template>

<style>
@import '@vue-flow/core/dist/style.css';
@import '@vue-flow/core/dist/theme-default.css';
</style>
