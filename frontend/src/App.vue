<template>
  <div id="app">
    <div class="sidebar">
      <AppSidebar />
    </div>
    <div class="body">
      <FlowEditor v-if="flowStore.currentPage === 'editor'" />
      <template v-else>
        <h1>Settings Page</h1>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppSidebar from './components/AppSidebar.vue'
import FlowEditor from './components/FlowEditor.vue'
import { useFlowStore } from './stores/useFlowStore'

const flowStore = useFlowStore()
</script>

<style scoped>
#app {
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: row;
}

.body {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>
